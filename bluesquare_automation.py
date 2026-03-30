import os
import sys
import datetime
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import hmac
import hashlib
import time
import json

# Windows 환경에서 특수문자(이모지 등) 출력을 위한 UTF-8 설정
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# [1. 데이터 수집 및 확장]
def scrape_catchtable_hotplaces(region="성수"):
    print(f"[{datetime.datetime.now().time()}] {region} 지역 핫플레이스 정밀 분석 중...")
    
    # 실제 마케팅을 위해 더 구체적인 정보 제공 (추후 크롤링 로직 확장 가능)
    return {
        "name": "성수다락",
        "region": region,
        "address": "서울 성동구 성수이로7길 24 2층",
        "menu_theme": "이탈리안/양식",
        "description": "매콤 크림 파스타와 다락 오므라이스로 이미 너무나 유명한 성수의 랜드마크 같은 곳이죠. 웨이팅이 조금 길어도 그 맛과 분위기는 정말 보증해요!",
        "tags": ["성수맛집", "성수데이트", "성수핫플", "성수다락", "주차꿀팁"],
        # 5장의 고퀄리티 이미지 매핑 (미리 생성해둔 assets 경로 활용)
        "images": [
            "/assets/images/2026-03-30-seongsu-darak/1.png",
            "/assets/images/2026-03-30-seongsu-darak/2.png",
            "/assets/images/2026-03-30-seongsu-darak/3.png",
            "/assets/images/2026-03-30-seongsu-darak/4.png",
            "/assets/images/2026-03-30-seongsu-darak/5.png"
        ],
        "naver_map_url": "https://map.naver.com/v5/search/성수다락",
        "insta_search_url": "https://www.instagram.com/explore/tags/성수다락/"
    }

# [2. 쿠팡 파트너스 실전 API 연동]
def generate_coupang_deeplink(target_url):
    """
    쿠팡 파트너스 API를 사용하여 수익 트래킹 딥링크 생성 (HMAC-SHA256 인증)
    """
    ACCESS_KEY = "6a4514a0-568b-47b9-a7b5-95a015ec1d4f"
    SECRET_KEY = "7d1cebf107a83ed44720d17e504aca9a77563dd8"
    
    REQUEST_METHOD = "POST"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
    
    # HMAC 서명 생성
    timestamp = time.strftime('%y%m%dT%H%M%SZ', time.gmtime())
    message = timestamp + REQUEST_METHOD + URL
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    authorization = f"CEA algorithm=HMAC-SHA256, access-key={ACCESS_KEY}, signed-timestamp={timestamp}, signature={signature}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization
    }
    
    payload = {
        "coupangUrls": [target_url]
    }
    
    try:
        response = requests.post(DOMAIN + URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            data = response.json()
            return data['data'][0]['shortenUrl']
    except Exception as e:
        print(f"⚠️ 쿠팡 API 호출 실패: {e}")
    
    # 실패 시 기본 링크 반환
    return "https://link.coupang.com/a/sample_default_profit"

def generate_coupang_box(theme):
    """
    포스팅 테마에 맞는 쿠팡 파트너스 추천 박스 (실제 수익 링크 포함)
    """
    recommendations = {
        "이탈리안/양식": ("집에서도 맛있는 파스타를?", "https://www.coupang.com/np/search?q=파스타키트"),
        "카페/디저트": ("홈카페의 완성! 프리미엄 원두", "https://www.coupang.com/np/search?q=원두커피"),
        "한식/고기": ("레스토랑 퀄리티의 한우 세트", "https://www.coupang.com/np/search?q=한우선물세트")
    }
    
    title, raw_url = recommendations.get(theme, ("지니가 추천하는 꿀템 보러가기", "https://www.coupang.com"))
    
    # 실전 수익 링크로 변환
    profit_link = generate_coupang_deeplink(raw_url)
    
    return f"""
<div class="coupang-box" style="background: #FFF9F9; border: 1px solid #FFEDED; border-radius: 12px; padding: 20px; text-align: center; margin: 40px 0;">
    <p style="margin: 0; color: #FF4D4D; font-weight: 700; font-size: 0.9rem;">🎁 지니의 취향 추천</p>
    <h5 style="margin: 10px 0; font-size: 1.1rem; color: #333;">{title}</h5>
    <a href="{profit_link}" target="_blank" style="background: #333; color: white; text-decoration: none; padding: 10px 20px; border-radius: 25px; font-size: 0.9rem; font-weight: 600; display: inline-block; margin-top: 5px;">쿠팡에서 최저가 확인하기</a>
    <p style="margin-top: 15px; font-size: 0.75rem; color: #999;">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
</div>
"""

# [3. 고도화된 콘텐츠 생성]
def generate_blog_post(info):
    print(f"[{datetime.datetime.now().time()}] 네이버 블로거 '지니'의 영양가 있는 글쓰기 중...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 필요합니다.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    date_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S +0900")
    coupang_box = generate_coupang_box(info['menu_theme'])
    
    # 블루스퀘어 앱 다운로드 중심 마케팅
    BLUESQUARE_APP_STORE_LINK = "https://bluesquare.app/users/app/"
    
    prompt = f"""
    너는 서울의 가장 트렌디한 곳을 다니며 기록하는 네이버 인기 블로거이자 인플루언서 '지니'야. 
    오늘 방문한 '{info['name']}'에 대해 정보력이 넘치면서도 세련된 말투(~해요, ~했어요)로 정말 친구에게 강추하는 블로그 포스트를 써줘. 
    
    [핵심 미션]
    1. 인스타그램 사회적 증거(Social Proof) 강조: 
       - 글 시작 부분에 "인스타그램 인기 피드 실시간 반응"을 인용하며 핫플임을 인증해.
    2. 블루스퀘어 앱 설치 전환: 
       - 주차 고민 해결책으로 블루스퀘어를 '필수'로 제안해.
    3. 인컨텍스트 링크 카드: 
       - 글 중간에 자연스럽게 "네이버 지도 길찾기"와 "인스타그램 핫피드" 링크 카드를 배치해. [LINK_CARD_NAVER], [LINK_CARD_INSTA] 마커를 사용해줘.
    
    [필수 포함 내용]
    - 제목: "{info['name']} 방문 후기 (+ {info['name']} 방문 주차 꿀팁)"
    - 사진 5장 배치: ![분위기]({info['images'][0]}), ![음식]({info['images'][1]}), ![외관]({info['images'][2]}), ![디테일]({info['images'][3]}), ![거리풍경]({info['images'][4]})
    - 🅿️ 주차 가이드 섹션: "블루스퀘어 주차는 도착해서 코드만 입력하면 끝!" 강조.
    
    아래 마크다운 형식을 엄격히 지켜줘.
    ---
    layout: post
    title: "{info['name']} 방문 후기 (+ {info['name']} 방문 주차 꿀팁)"
    date: {date_now}
    categories: 맛집 탐방
    naver_map_url: "{info['naver_map_url']}"
    insta_search_url: "{info['insta_search_url']}"
    bluesquare_app_link: "{BLUESQUARE_APP_STORE_LINK}"
    ---
    
    ![인스타그램 리얼 반응](/assets/images/bluesquare/insta_grid.png)
    
    본문은 여기에... (여기에 쿠팡 광고 섹션을 중간 지점에 삽입해줘: {coupang_box})
    
    [주차 가이드 마커: PARKING_GUIDE]
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    print("🚀 지니의 프리미엄 마케팅 블로그 파이프라인 가동...\n")
    
    # 1. 정보 수집 (Mock but Detailed)
    info = scrape_catchtable_hotplaces("성수")
    
    # 2. 콘텐츠 생성 (Gemini)
    markdown_post = generate_blog_post(info)
    
    # 3. 렌더링 후 마커 치환 (Link Cards & Guide)
    parking_guide_html = """
<div class="parking-guide-container" style="background: #F8F9FA; border-radius: 12px; padding: 25px; margin: 40px 0; border: 1px solid #EEE;">
    <h4 style="margin-top: 0; color: #333; display: flex; align-items: center;">🅿️ 블루스퀘어 주차 가이드</h4>
    <p style="font-size: 0.95rem; color: #666; margin-bottom: 20px;">도착해서 주차장 코드만 입력하면 주차 끝! 정말 쉽죠? :)</p>
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
        <img src="/assets/images/bluesquare/guide_map.png" style="width: 48%; border-radius: 8px; border: 1px solid #DDD;">
        <img src="/assets/images/bluesquare/guide_input.png" style="width: 48%; border-radius: 8px; border: 1px solid #DDD;">
    </div>
</div>
"""
    naver_card_html = f'<div class="link-card naver-card"><a href="{info["naver_map_url"]}" target="_blank">📍 네이버 지도에서 위치 & 길찾기</a></div>'
    insta_card_html = f'<div class="link-card insta-card"><a href="{info["insta_search_url"]}" target="_blank">📸 인스타그램에서 실시간 무드 확인</a></div>'
    
    markdown_post = markdown_post.replace("[LINK_CARD_NAVER]", naver_card_html)
    markdown_post = markdown_post.replace("[LINK_CARD_INSTA]", insta_card_html)
    markdown_post = markdown_post.replace("[PARKING_GUIDE]", parking_guide_html)

    # 4. 파일 저장 (순번 P001, P002... 부여 및 식당 이름 대신 포스팅 제목을 파일명으로 활용)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_dir = os.path.join(script_dir, "_posts")
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
    
    # 기존 포스트 개수 확인하여 다음 순번 결정
    existing_posts = [f for f in os.listdir(posts_dir) if f.endswith(".md")]
    next_num = len(existing_posts) + 1
    post_id = f"P{next_num:03d}"
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 제목에서 특수문자 제거 및 공백을 대시(-)로 변환하여 안전한 파일명 생성
    title_raw = f"{info['name']} 방문 후기 (+ {info['name']} 방문 주차 꿀팁)"
    import re
    # 한글, 영문, 숫자만 남기고 나머지는 제거
    clean_title = re.sub(r'[^\w\s-]', '', title_raw).strip()
    # 공백을 대시로 변환
    safe_title = re.sub(r'[-\s]+', '-', clean_title)
    
    # 순번(P001)을 포함한 최종 파일명
    filename = os.path.join(posts_dir, f"{date_str}-{post_id}-{safe_title}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_post)
        
    print(f"\n✅ 고퀄리티 프리미엄 포스팅 생성 완료: {filename}")
    print("GitHub Actions에 의해 모든 수익화 요소가 포함되어 배포됩니다.")

if __name__ == "__main__":
    main()
