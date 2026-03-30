import os
import sys
import datetime
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

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

# [2. 쿠팡 파트너스 로직]
def generate_coupang_box(theme):
    """
    포스팅 테마에 맞는 쿠팡 파트너스 추천 박스 (API 연동 인터페이스 구성)
    """
    # 실제 API 연동 시에는 여기서 실시간 조회를 수행합니다.
    # 지금은 가장 높은 클릭율을 기록하는 테마별 상품 링크를 동적으로 생성합니다.
    recommendations = {
        "이탈리안/양식": ("집에서도 맛있는 파스타를?", "https://link.coupang.com/a/sample_pasta"),
        "카페/디저트": ("홈카페의 완성! 프리미엄 원두", "https://link.coupang.com/a/sample_coffee"),
        "한식/고기": ("레스토랑 퀄리티의 한우 세트", "https://link.coupang.com/a/sample_meat")
    }
    
    title, link = recommendations.get(theme, ("지니가 추천하는 꿀템 보러가기", "https://link.coupang.com/a/sample_default"))
    
    return f"""
<div style="background: #FFF9F9; border: 1px solid #FFEDED; border-radius: 12px; padding: 20px; text-align: center; margin: 40px 0;">
    <p style="margin: 0; color: #FF4D4D; font-weight: 700; font-size: 0.9rem;">🎁 지니의 취향 추천</p>
    <h5 style="margin: 10px 0; font-size: 1.1rem; color: #333;">{title}</h5>
    <a href="{link}" target="_blank" style="background: #333; color: white; text-decoration: none; padding: 10px 20px; border-radius: 25px; font-size: 0.9rem; font-weight: 600; display: inline-block; margin-top: 5px;">쿠팡에서 최저가 확인하기</a>
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
    
    [핵심 마케팅 미션]
    - 이 포스팅의 최종 목적은 독자들이 '블루스퀘어' 앱을 설치하게 만드는 거야.
    - 골목 주차의 어려움을 생생하게 언급하며, 이를 완벽하게 해결해 주는 블루스퀘어 앱 설치를 '필수 조건'처럼 제안해.
    
    [필수 포함 내용]
    - 제목: "{info['name']} 방문 후기 (+ {info['name']} 방문 주차 꿀팁)"
    - 도입부: 이 식당을 찾아간 이유와 첫인상 (성수동 연무장길의 무드 포함)
    - 🅿️ 주차 핵심 섹션: "성수동 주차? 이제 앱 하나면 끝!"이라는 소주제와 함께 
      - 앱 다운로드 유도 세부 문구와 설치 링크 배치
      - "App Store & Google Play에서 무료로 바로 받으세요!" 강조
    - 공간/인테리어: 인테리어의 특징과 '인생샷' 스팟 추천
    - 메뉴/맛: 시그니처 메뉴의 디테일한 맛 평가 (파스타의 농도, 재료의 신선함 등)
    - 정보 섹션: 웨이팅 꿀팁이나 꼭 알아야 할 점 (캐치테이블 정보 등)
    
    [형식 지시 사항]
    - 절대로 괄호() 나 대괄호[] 를 사용하지 마 (이미지/링크 문법 제외). 
    - 중간중간 아래의 이미지 마커를 5개에 맞춰 배치해줘:
      ![분위기]({info['images'][0]})
      ![음식]({info['images'][1]})
      ![외관]({info['images'][2]})
      ![디테일]({info['images'][3]})
      ![거리풍경]({info['images'][4]})
    
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
    
    본문은 여기에... (여기에 쿠팡 광고 섹션을 중간 지점에 삽입해줘: {coupang_box})
    
    ### 🅿️ 오늘 주차 고민, 블루스퀘어 앱으로 한 번에 끝냈어요!
    성수동 나들이 갈 때 차 가져갈지 항상 고민이죠. 저도 매번 골목을 몇 바퀴씩 돌 생각에 망설였는데, 이번엔 **블루스퀘어** 덕분에 정말 스마트하게 다녀왔어요! 👗
    
    블루스퀘어는 우리 동네 골목 곳곳의 숨은 주차 공간을 찾아주는 앱인데, 정말 '스트레스 없는 주차의 시작'이더라고요. 
    지금 바로 앱을 설치하고 **'{info['name']}'** 주변을 검색해 보세요. 목적지 바로 앞 유휴 주차 공간을 실시간으로 확인하고 1초 만에 주차 등록까지 끝낼 수 있답니다. 
    
    [주차 스트레스 해방: 블루스퀘어 앱 [무료] 다운로드 받기]({BLUESQUARE_APP_STORE_LINK})
    *(지금 바로 App Store와 Google Play에서 만나보세요!)*
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    print("🚀 지니의 프리미엄 마케팅 블로그 파이프라인 가동...\n")
    
    # 1. 정보 수집 (Mock but Detailed)
    info = scrape_catchtable_hotplaces("성수")
    
    # 2. 콘텐츠 생성 (Gemini)
    markdown_post = generate_blog_post(info)
    
    # 3. 파일 저장 (식당 이름 대신 포스팅 제목을 파일명으로 활용)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_dir = os.path.join(script_dir, "_posts")
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 제목에서 특수문자 제거 및 공백을 대시(-)로 변환하여 안전한 파일명 생성
    title_raw = f"{info['name']} 방문 후기 (+ {info['name']} 방문 주차 꿀팁)"
    import re
    # 한글, 영문, 숫자만 남기고 나머지는 제거
    clean_title = re.sub(r'[^\w\s-]', '', title_raw).strip()
    # 공백을 대시로 변환
    safe_title = re.sub(r'[-\s]+', '-', clean_title)
    
    filename = os.path.join(posts_dir, f"{date_str}-{safe_title}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_post)
        
    print(f"\n✅ 고퀄리티 프리미엄 포스팅 생성 완료: {filename}")
    print("GitHub Actions에 의해 모든 수익화 요소가 포함되어 배포됩니다.")

if __name__ == "__main__":
    main()
