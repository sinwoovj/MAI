"""
윈도우에서 wget 설치 (powershell에서 아래 코드 실행)
$ Invoke-WebRequest -Uri https://raw.github.com/vito-ai/openapi-grpc/main/protos/vito-stt-client.proto -OutFile vito-stt-client.proto

definition (.proto) file 다운로드는 코드 (콘솔에서)
$ wget https://raw.github.com/vito-ai/openapi-grpc/main/protos/vito-stt-client.proto

gRPC code 만드는 코드 (콘솔에서)
$ pip install grpcio-tools
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./vito-stt-client.proto

NOTE: 이 모듈에는 이하 종속성이 필요합니다 `grpcio`, `requests`.
아래 코드를 통해 설치
$ pip install grpcio
$ pip install requests
"""
import metadata.api_key as api_key
import argparse
import logging
import time
from io import DEFAULT_BUFFER_SIZE

import grpc
import vito_stt_client_pb2 as pb
import vito_stt_client_pb2_grpc as pb_grpc
from requests import Session

API_BASE = "https://openapi.vito.ai"
GRPC_SERVER_URL = "grpc-openapi.vito.ai:443"
CLIENT_ID = api_key.VITO_API_KEY_CLIENT_ID
CLIENT_SECRET = api_key.VITO_API_KEY_CLIENT_SECRET

SAMPLE_RATE = 8000
ENCODING = pb.DecoderConfig.AudioEncoding.LINEAR16


class VITOOpenAPIClient:
    def __init__(self, client_id, client_secret):
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self.client_id = client_id
        self.client_secret = client_secret
        self._sess = Session()
        self._token = None

    @property
    def token(self):
        if self._token is None or self._token["expire_at"] < time.time():
            resp = self._sess.post(
                API_BASE + "/v1/authenticate",
                data={"client_id": self.client_id, "client_secret": self.client_secret},
            )
            resp.raise_for_status()
            self._token = resp.json()
        return self._token["access_token"]

    def transcribe_streaming_grpc(self, filepath, config):
        base = GRPC_SERVER_URL
        with grpc.secure_channel(
            base, credentials=grpc.ssl_channel_credentials()
        ) as channel:
            stub = pb_grpc.OnlineDecoderStub(channel)
            cred = grpc.access_token_call_credentials(self.token)

            def req_iterator():
                # 스트리밍 설정을 보내는 요청을 첫 번째 요청으로 보냅니다.
                yield pb.DecoderRequest(streaming_config=config)
                # 오디오 파일을 바이너리 모드로 열어서 읽고,
                # 읽어진 내용을 버퍼 크기만큼 읽어서 요청 데이터에 담아서 yield 합니다.
                with open(filepath, "rb") as f:
                    while True:
                        buff = f.read(DEFAULT_BUFFER_SIZE)
                        if buff is None or len(buff) == 0:
                            break
                        yield pb.DecoderRequest(audio_content=buff)

                # req_iterator를 생성하고, 
                # 생성된 req_iterator를 stub.Decode() 함수로 전달합니다.
                # 반환된 응답을 출력합니다.
                req_iter = req_iterator()
                resp_iter = stub.Decode(req_iter, credentials=cred)
                for resp in resp_iter:
                    resp: pb.DecoderResponse
                    for res in resp.results:
                        print(
                            "[online-grpc] final:{}, text:{}".format(
                                res.is_final, res.alternatives[0].text
                            )
                        )

if __name__ == "main":
    # 파이썬 스크립트를 실행할 때 입력으로 받는 인자를 처리합니다.
    parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("stream", help="File to stream to the API")
    args = parser.parse_args()

    # 디코더 설정을 만듭니다.
    config = pb.DecoderConfig(
        sample_rate=SAMPLE_RATE,
        encoding=ENCODING,
        use_itn=True,
        use_disfluency_filter=False,
        use_profanity_filter=False,
    )

    # VITO Open API Client를 만들고, 스트리밍을 위한 인자를 전달합니다.
    client = VITOOpenAPIClient(CLIENT_ID, CLIENT_SECRET)
    client.transcribe_streaming_grpc(args.stream, config)