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
    너는 서울의 가장 힙한 성수동과 한남동의 맛집을 기록하는 20대 여성 블로거야. 
    오늘 방문한 '{restaurant_info['name']}'에 대해 감각적이고 세련된 말투(~해요, ~했어요)로 블로그 포스트를 써줘. 
    블로그 이름은 '오늘의 성수랑 한남 사이'야.

    식당명: {restaurant_info['name']}
    설명: {restaurant_info['description']}
    식당 이미지: {restaurant_info['og_image_url']}
    
    아래 마크다운 형식을 엄격히 지켜서 작성해줘.
    ---
    layout: post
    title: "✨ {restaurant_info['region']} | 취향 저격 식당 '{restaurant_info['name']}' 후기 (feat. 주차 걱정 끝)"
    date: {date_now}
    categories: 맛집 탐방
    ---

    ![{restaurant_info['name']}]({restaurant_info['og_image_url']})

    ### 🥂 오늘의 공간: {restaurant_info['name']}
    드디어 가본 **{restaurant_info['name']}**! {restaurant_info['description']} 인테리어부터 분위기까지 제 마음에 쏙 들었어요. 소중한 사람과 함께라면 더 행복해질 수 있는 그런 공간이었답니다. ✨

    ### 📱 방문 전 필수 체크
    여기 방문하실 분들은 미리 캐치테이블 예약이랑 인스타 확인하고 가시는 거 추천드려요! :)
    - **Catch Table**: [간편하게 예약하기](https://app.catchtable.co.kr/search?keyword={restaurant_info['name']})
    - **Instagram**: [무드 가득한 사진 미리보기](https://www.instagram.com/explore/tags/{restaurant_info['name']}/)

    ### 🅿️ 주차 스트레스 없이 우아하게 즐기는 법!
    성수랑 한남동 쪽은 주차 자리가 정말 귀하잖아요. :( 저도 주차 때문에 차를 가져갈지 말지 늘 망설였는데, 이번엔 **블루스퀘어**라는 앱 덕분에 진짜 편하게 해결했어요! 

    앱에서 **'{restaurant_info['name']}'**을 검색하면, 근처에 바로 주차할 수 있는 모든 제휴 주차장을 순식간에 알려줘요. 최저가 정보부터 무료 주차권 유무까지 한눈에 확인 가능하니까, 이제 주차 걱정은 그만하고 우아하게 음식만 즐기면 돼요! 👗

    [주차 걱정 지워주는 블루스퀘어 앱 바로가기](https://bluesquare.example.com/install)

    주차 부담 없이 기분 좋은 시간 되시길 바랄게요! 다음에 또 예쁜 곳으로 찾아올게요. 안녕! 🤍
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    print("🚀 블루스퀘어 마케팅 자동화 파이프라인 시작...\n")
    
    # 1. 정보 수집 단계
    hotplace = scrape_catchtable_hotplaces("성수")
    
    # 2. 콘텐츠 생성 단계 (Gemini)
    markdown_post = generate_blog_post(hotplace)
    
    # 3. 파일 저장 (스크립트가 있는 폴더의 _posts 디렉토리)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_dir = os.path.join(script_dir, "_posts")
    
    if not os.path.exists(posts_dir):
        os.makedirs(posts_dir)
        
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_name = hotplace['name'].replace(" ", "-")
    filename = os.path.join(posts_dir, f"{date_str}-{safe_name}.md")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_post)
        
    print(f"\n✅ 새 포스팅 생성 완료: {filename}")
    print("GitHub Actions에 의해 자동으로 커밋 및 배포될 예정입니다.")

if __name__ == "__main__":
    main()
