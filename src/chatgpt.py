import openai

# OpenAI API 키 설정
openai.api_key = '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'

def generate_review(prompt):
    # GPT-3 API 호출
    response = openai.Completion.create(
        engine="text-davinci-002",  # 또는 "text-davinci-002" 사용 가능
        prompt=prompt,
        max_tokens=3500,  # 생성할 토큰의 최대 수
        temperature=0.7,  # 높은 값일수록 생성이 더 다양해집니다. (0.0 ~ 1.0)
        n=1,  # 생성할 리뷰의 수
        stop="끝입니다."  # 생성을 멈출 단어 목록
    )

    # API 응답에서 생성된 리뷰 추출
    generated_review = response.choices[0].text.strip()
    return generated_review

# 특정 프롬프트로 리뷰 생성
prompt_text = "너는 지금부터 아는 사람에게 상품에 대한 소감을 얘기할거야. " \
              "언어는 한국어이고, 분량은 3줄이야. " \
              "네가 얘기할 내용에는 상품의 이름, 장단점, 소감의 내용이 들어갈 거야. " \
              "다시 한 번 얘기하지만 모든 내용은 문장 형태로 설명하는 내용이어야 해." \
              "마지막 내용에는 '끝입니다.'라고 덧붙여줘."
generated_review = generate_review(prompt_text)

# 생성된 리뷰 출력
print(generated_review)
