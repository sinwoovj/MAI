# vito_stt_normal.py

def vito_stt_normal(audio_file: str):
    # 필요한 패키지 및 파일을 import한다.
    import metadata.api_key as api_key # API 키의 보안을 위해 파일을 따로 저장한다.
    import json
    import requests
    import time

    """
    RUNTIME : 런타임 변수 초기화
    RUNTIME_MAX : 런타임 최대값
    POLLING_CYCLE : 서버에 GET할 주기
    """
    RUNTIME = 0
    RUNTIME_MAX = 300
    POLLING_CYCLE = 5

    AUDIO_FILE = audio_file # "audio.m4a"

    # GET TOKEN
    resp = requests.post(
        'https://openapi.vito.ai/v1/authenticate',
        data={'client_id': f'{api_key.VITO_API_KEY_CLIENT_ID}',
            'client_secret': f'{api_key.VITO_API_KEY_CLIENT_SECRET}'}
    )
    resp.raise_for_status()
    # print(resp.json())
    access_token = resp.json()['access_token']
    # print("Access Token : " + access_token)

    headers={'Authorization': 'Bearer ' + access_token}

    #POST
    config = {
    "diarization": {
        "use_verification": False
    },
    "use_multi_channel": False
    }
    resp = requests.post(
        'https://openapi.vito.ai/v1/transcribe',
        headers=headers,
        data={'config': json.dumps(config)},
        # 변환할 파일의 위치와 형식을 제대로 설정해야한다. 
        files={'file': open(AUDIO_FILE, 'rb')}
    )
    resp.raise_for_status()
    # print(resp.json())
    transcribe_id = resp.json()['id']

    # GET
    resp = requests.get(
        'https://openapi.vito.ai/v1/transcribe/'+transcribe_id,
        headers=headers,
    )
    resp.raise_for_status()
    # print(resp.json())

    # Long Polling : 서버에 요청을 보냈을 때 응답할 때까지 자동으로 요청함. + 예외처리
    while True:
        resp = requests.get(
            'https://openapi.vito.ai/v1/transcribe/'+transcribe_id,
            headers=headers,
        )
        resp.raise_for_status()

        # 변환 상태값 저장
        status = resp.json()['status']

        # 성공시
        if status == "completed":
            result = resp.json()["results"]["utterances"][0]["msg"]
            # print("결과값 : " + result)
            return result
        # 실패시
        elif status == "failed":
            error_message = resp.json()['code']
            raise Exception(f"STT 실패 원인 : {error_message}"); return ''
            
        # 변환중
        elif status == "transcribing":
            print("변환중...")
        print("런타임 : "+str(RUNTIME)+"초 경과")
        time.sleep(POLLING_CYCLE)
        if(RUNTIME>=RUNTIME_MAX):
            print("시간초과")
            return ''
        else:
            RUNTIME+=POLLING_CYCLE