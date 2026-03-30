import os
import datetime
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# [1. 데이터 수집 가이드]
def scrape_catchtable_hotplaces(region="성수"):
    """
    검색 엔진, 뉴스 API 또는 웹 스크래핑을 통해 특정 지역의 '캐치테이블 예약 인기 식당' 데이터를 수집.
    """
    print(f"[{datetime.datetime.now().time()}] {region} 지역 인기 식당 데이터 수집 중...")
    
    # 예시(Mock) 데이터 반환. 실제 환경에서는 BeautifulSoup 등으로 크롤링 로직 구현 가능.
    return {
        "name": "성수다락",
        "region": region,
        "description": "매콤 크림 파스타와 다락 오므라이스가 유명한 아늑한 분위기의 양식당.",
        "og_image_url": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
    }

# [2. 콘텐츠 생성 규칙]
def generate_blog_post(restaurant_info):
    """
    Gemini 1.5 Flash를 활용하여 요구된 가이드에 맞는 Jekyll 포스트 마크다운 생성.
    """
    print(f"[{datetime.datetime.now().time()}] Gemini 1.5 Flash로 블로그 콘텐츠 생성 중...")
    
    # GitHub Actions 환경변수 또는 직접 입력된 키 사용
    api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyC1pyObXol9oOd4juyHPH529KsN6VRotmw")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    date_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S +0900")
    
    prompt = f"""
    식당명: {restaurant_info['name']}
    설명: {restaurant_info['description']}
    식당 이미지: {restaurant_info['og_image_url']}
    
    아래 마크다운 형식을 엄격히 지켜서 작성해줘. 한국어로 작성해.
    ---
    layout: post
    title: "[{restaurant_info['region']} 맛집] '{restaurant_info['name']}' 방문 가이드 및 현실적 주차 꿀팁"
    date: {date_now}
    categories: 맛집 주차
    ---

    ![{restaurant_info['name']}]({restaurant_info['og_image_url']})

    ### [맛집 소개]
    (여기에 식당의 대표 메뉴와 분위기를 2~3문장으로 담백하게 요약)

    ### [주차 정보]
    (여기에 서울 주차의 불편함, 비싼 요금 등에 대해 공감하며 설명)

    ### [솔루션 제안]
    '블루스퀘어 앱'을 설치하고 '{restaurant_info['name']}'을 검색하면, 근처 제휴 주차장의 무료 주차권과 저렴한 주차 공간을 바로 확인할 수 있습니다.

    ### CTA
    [블루스퀘어 앱 설치하고 무료 주차 혜택 받기](https://bluesquare.example.com/install)

    ---
    **BlueSquare Info:** 블루스퀘어는 글로벌 AI 주차 솔루션 제공업체입니다. 유휴지, 자투리 공간을 QR페이와 AI주차 관제 기기로 차단기 없이 무비용으로 유료주차장으로 운영해주고, 건물주와 수익을 쉐어합니다. 그 외에 정기권, 일주차 등 편리한 주차장 서비스를 저렴한 가격에 제공하는 것이 핵심 서비스입니다.
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    print("🚀 블루스퀘어 마케팅 자동화 파이프라인 시작...\n")
    
    # 1. 정보 수집 단계
    hotplace = scrape_catchtable_hotplaces("성수")
    
    # 2. 콘텐츠 생성 단계 (Gemini)
    markdown_post = generate_blog_post(hotplace)
    
    # 3. 파일 저장 (_posts 디렉토리)
    if not os.path.exists("_posts"):
        os.makedirs("_posts")
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_name = hotplace['name'].replace(" ", "-")
    filename = f"_posts/{date_str}-{safe_name}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_post)
        
    print(f"\n✅ 새 포스팅 생성 완료: {filename}")
    print("GitHub Actions에 의해 자동으로 커밋 및 배포될 예정입니다.")

if __name__ == "__main__":
    main()
