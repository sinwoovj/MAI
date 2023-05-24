import pyaudio
import numpy as np
import wave

def save_wav_file(data, filename, sample_rate):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data)

# 예시 오디오 데이터와 저장할 파일 경로
audio_data = b'\x00\x01\x02\x03\x04\x05'
output_file = 'audio.wav'

# 샘플레이트는 오디오 데이터의 샘플링 속도입니다 (예: 44100Hz).
sample_rate = 44100

input_device_id = 0

# 마이크로 입력 스트림 설정
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                input_device_index=input_device_id,
                frames_per_buffer=1024)

# 실시간 입력 처리
try:
    while True:
        # 버퍼에서 데이터 읽기
        audio_data = stream.read(1024)
        audio_samples = np.frombuffer(audio_data, dtype=np.int16)
        print("오디오 데이터 :", audio_data)
        print("오디오 샘플(원시 데이터) :", audio_samples)
        # API로 데이터 스트리밍
        # 여기에 데이터를 API로 전송하는 코드를 작성하면 됩니다.
        # config 및 audio_samples를 사용하여 API 호출을 수행합니다. 

        # WAV 파일로 저장
        save_wav_file(audio_data, output_file, sample_rate)
        

except KeyboardInterrupt:
    pass

# 스트림 종료
stream.stop_stream()
stream.close()
p.terminate()
