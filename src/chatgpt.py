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
prompt_text = "From now on, you will tell your feelings about the product to someone you know. " \
              "The language is Korean, and the amount is 3 lines. " \
              "What you're going to talk about will include the name of the product, " \
              "its pros and cons, and how you feel. Once again, everything should be explained in the form of a sentence. " \
              "At the end, add, '끝입니다.'"
generated_review = generate_review(prompt_text)

# 생성된 리뷰 출력
print(generated_review)
