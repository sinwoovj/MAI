import openai_ # openai_.py 파일
import vito_stt_normal # vito_stt_normal.py 파일
import google_cloud_tts # google_cloud_tts.py 파일
import create_google_service_key as cg # create_google_service_key.py 파일
import google_service as gs # google_service.py 파일
import metadata.api_key as ak # 여러 api 관련 정보가 담긴 파일

from playsound import playsound # 미디어 출력 패키지 >> pip install playsound
import cv2 # OpenCV 패키지 >> pip install cv2

AUDIO_FILE_NAME = "HTML" # 파일 이름
AUDIO_FILE_EXTENTION = ".m4a" # 파일 확장자

stt_res = vito_stt_normal.vito_stt_normal("./audio/input/"+AUDIO_FILE_NAME+AUDIO_FILE_EXTENTION)
print(stt_res)
if(stt_res != ''):
    answer = openai_.ai_res(stt_res)
    print(answer)
    google_cloud_tts.google_tts(answer, "./ audio/output/output.mp3")
    playsound('./audio/output/output.mp3')
    print("오디오 출력")