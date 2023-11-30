import openai
from dotenv import load_dotenv
import os
import random
from src.utils.add_data_to_csvfile import add_data_to_csvfile

# OpenAI API 키 설정
# .env 파일 로드
load_dotenv()

# API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI API 키 설정
openai.api_key = api_key
def generate_review(prompt):
    # GPT-3 API 호출
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,  # 생성할 토큰의 최대 수
        temperature=0.7,  # 높은 값일수록 생성이 더 다양해집니다. (0.0 ~ 1.0)
        n=1,  # 생성할 리뷰의 수
        stop=""  # 생성을 멈출 단어 목록
    )

    # API 응답에서 생성된 리뷰 추출
    generated_review = response.choices[0].text.strip()
    return generated_review

# 각 카테고리를 담은 리스트
electronics = ["스마트폰", "노트북", "테블릿", "냉장고", "세탁기", "에어컨", "카메라", "드론", "스마트 워치", "이어폰", "게임 콘솔", "헤드폰 앰프", "모니터", "마우스", "키보드", "노이즈 캔슬링 이어폰"]
clothing = ["티셔츠", "청바지", "드레스", "자켓", "운동화", "모자", "가디건", "스웨터", "스커트", "후드티", "비치웨어", "트레이닝복", "수영복", "비올레인 코트", "한복"]
furniture = ["소파", "침대", "탁자", "의자", "장롱", "서랍장", "화장대", "식탁", "거울", "선반", "책상", "책장", "옷장", "화장실 세트", "침대 테이블"]
sports_equipment = ["런닝화", "요가 매트", "축구공", "농구공", "헬스 자전거", "등산 모자", "스케이트보드", "테니스 라켓", "골프 클럽", "스키 장비", "야구 글러브", "스노보드", "체육복", "수영 기구", "스쿼시 라켓"]
audio_devices = ["헤드폰", "스피커", "이어폰", "오디오 레코더", "사운드 바", "이퀄라이저", "음향 카드", "마이크", "턴테이블", "DJ 컨트롤러", "이어폰 케이스", "블루투스 스피커", "음악 플레이어", "오디오 인터페이스", "음향 프로세서"]
camping_gear = ["텐트", "취사도구", "침낭", "등산화", "캠핑 의자", "랜턴", "아이젠", "포터블 그릴", "햇빛 차단 우산", "손전등", "캠핑 테이블", "카약", "등산 지팡이", "캠핑 코티", "야외 매트"]
hair_products = ["샴푸", "린스", "헤어 드라이어", "헤어 스프레이", "헤어 컬러", "헤어 클리퍼", "헤어 롤", "헤어 브러시", "헤어 마스크", "헤어 오일", "헤어 밴드", "헤어 핀", "헤어 터번", "헤어 스트레이트너", "헤어 커버"]
golf_equipment = ["골프 클럽 세트", "골프 공", "골프 가방", "골프 슈즈", "골프 장갑", "골프 캡", "골프 트레이닝 에이드", "골프 티", "골프 우산", "골프 스탠드백", "골프 카트", "골프 풀종", "골프 스윙 트레이너", "골프 코스용 지폐 매트", "골프 퍼터"]
exercise_equipment = ["트레드밀", "사이클", "레그 프레스 머신", "덤벨", "바벨", "풀업 바", "평행봉", "플라이 박스", "스탭 박스", "헬스볼", "요가 매트", "폼 롤러", "키네시올로지 테이프", "밴드", "스텝 플랫폼"]
food_items = ["쌀", "밀가루", "설탕", "소금", "식용유", "우유", "계란", "닭고기", "소고기", "생선", "과일", "야채", "떡", "라면", "커피", "초콜릿"]

categories = [electronics, clothing, furniture, sports_equipment, audio_devices, camping_gear, hair_products, golf_equipment, exercise_equipment, food_items]

random_category = random.choice(categories)
random_product = random.choice(random_category)

# 특정 프롬프트로 리뷰 생성
prompt_text = "Q: 헤드셋 리뷰 A: 너무 잘샀어요.대만족입니다.	" \
              "A: 물건 검색하다 우연히 쿠팡에 접속했는데 5천원 할인 쿠폰을 줘서 가격도 싸고 괜찮아보여서 별 기대없이 주문했습니다." \
              "이틀 후 아침에 택배 도착하였는데 냉장고에 넣는다는걸 깜빡하고 받은채로 놔두었다가 저녁에 개봉하였는데 포장을 매우 꼼꼼히해서 같이 들어있는 얼음팩도 반이상 얼어있더라구요." \
              "✅ 총평: 곰곰 한돈 삼겹살 구이용은 집에서도 고급스러운 삼겹살을 즐길 수 있는 최적의 선택입니다. " \
              "품질과 맛에 대한 만족도가 높고, 다양한 조리 방법으로 즐길 수 있어 실용성도 뛰어납니다. " \
              "집에서 편안하게 고급 삼겹살을 즐기고 싶은 분들께 적극 추천드립니다!제 리뷰가 제품 선택에 조금이라도 도움이 되셨으면 좋겠습니다.즐거운 요리 시간 보내세요!" \
              "Q:주먹밥 리뷰 " \
              "A:아침마다 일어나서 밥챙겨 먹기가 힘이들더라구요!그래도 아침은 먹어야 하루가 힘이나서 찾다가 가성비 좋은 주먹밥을 발견했습니다!" \
              "소불2개 참치2개 불닭2개 로제2개 김치2개 까치2개로총 12개로 구비되어 있습니다!여러가지 맛이 있어서 아주 마음에 들었어요!" \
              "근데 너무 맛있어서 2주면 다먹더라구요!칼로리는 종류별로 다른데요 최소 170kcal~218kcal입니다!일반적인 즉석밥 칼로리라고 생각하시면 됩니다!여러가지 양념과 재료가 들어갔는데 이정도 " \
              "칼로리면굉장히 저 칼로리라고 생각이 들어요!간단하게 아침에 대용으로 먹기좋은 주먹밥이였구요!맛은 있었어요! 조리법도 간단하고!자주 구매해서 먹을것 같습니다 만족스러운 제품이에요!" \
              f"Q:{random_product} 리뷰" \
              "A:"

# 실행 1번->랜덤 상품 1개에 대한 리뷰 3개 생성

for i in range (3):
    generated_review = generate_review(prompt_text)
    # 생성된 리뷰 출력
    print(generated_review)

    # 리뷰 텍스트를 문장 단위로 분할
    sentences = generated_review.split(".")

    headline = sentences[0].strip()                       # 첫 번째 문장을 headline으로 저장
    review_content = ".".join(sentences[1:]).strip()      # 나머지 문장들을 review_content로 저장

    # 데이터 구성
    review_data = {"headline": headline, "review_content": review_content}

    # CSV
    add_data_to_csvfile(
        path='../result/chatgpt_reviews.csv',
        data=[review_data],
        sep='\t', encoding='UTF-8')
