# 참고 블로그 : https://wooiljeong.github.io/python/chatgpt-api/
# 패키지 다운로드 : pip install openai

def ai_res(q: str):
    import openai
    import metadata.api_key as api_key

    # 발급받은 API 키 설정
    OPENAI_API_KEY = api_key.OPENAI_API_KEY

    # openai API 키 인증
    openai.api_key = OPENAI_API_KEY

    # 모델 - GPT 3.5 Turbo 선택
    model = "gpt-3.5-turbo"

    # 질문 작성하기
    query = q

    # 메시지 설정하기
    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']

    return answer

"""
openai key : openai에서 받은 API key를 등록합니다. 이 Key는 노출되지 않도록 조심하셔야 합니다.
model : openai에서 제공해주는 모델을 입력합니다. 저는 gpt3.5를 활용할 수 있는 text-davinci-003을 활용합니다.
prompt : 제가 원하는 실행어를 입력합니다. 어떻게 하면 좋은 결과가 나오는지는 많은 테스트를 해보셔야합니다. 일단, 본 포스팅의 예제에서는 간단하게 이름이 뭔지 출력하도록 작성했습니다.
max_tokens :  입력 + 출력 값으로 잡을 수 있는 max_tokens 값입니다. 해당 길이가 넘어가면 에러가 나오면서 api 통신이 안 될 수 있습니다. 
stop : stop 지점을 설정합니다. 저는 개행문자(\n)으로 두었습니다.
"""