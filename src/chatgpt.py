import openai
from dotenv import load_dotenv
import os

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
        engine="text-davinci-002",  # 또는 "text-davinci-002" 사용 가능
        prompt=prompt,
        max_tokens=1000,  # 생성할 토큰의 최대 수
        temperature=0.7,  # 높은 값일수록 생성이 더 다양해집니다. (0.0 ~ 1.0)
        n=1,  # 생성할 리뷰의 수
        stop="끝입니다."  # 생성을 멈출 단어 목록
    )

    # API 응답에서 생성된 리뷰 추출
    generated_review = response.choices[0].text.strip()
    return generated_review

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
              "근데 너무 맛있어서 2주면 다먹더라구요!칼로리는 종류별로 다른데요 최소 170kcal~218kcal입니다!일반적이 즉석밥 칼로리라고 생각하시면 됩니다!여러가지 양념과 재료가 들어갔는데 이정도 " \
              "칼로리면굉장히 저 칼로리라고 생각이 들어요!간단하게 아침에 대용으로 먹기좋은 주먹밥이였구요!맛은 있었어요! 조리법도 간단하고!자주 구매해서 먹을것 같습니다 만족스러운 제품이에요!" \
              "Q:노트북 리뷰" \
              "A:"
generated_review = generate_review(prompt_text)

# 생성된 리뷰 출력
print(generated_review)
