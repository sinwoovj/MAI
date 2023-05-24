import pyaudio
import wave
import time

def save_wav_file(data, filename, sample_rate):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data)

# 스트리밍 입력을 받는 코드
CHUNK = 1024  # 버퍼 크기
FORMAT = pyaudio.paInt16  # 16-bit 형식
CHANNELS = 1  # Mono 오디오
RATE = 44100  # 샘플링 속도
SILENCE_THRESHOLD = 0.01  # 음성이 아닌 정적 소음 임계값
SILENCE_DURATION = 5  # 종료되기 위한 정적 소음 지속 시간 (초)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# 오디오 데이터를 WAV 파일로 저장하는 코드
output_file = 'audio.wav'

print("Recording started...")

frames = []  # 오디오 프레임 저장을 위한 빈 리스트
silence_counter = 0  # 정적 소음 지속 시간을 계산하기 위한 카운터

# 스트리밍 입력을 받고 프레임을 저장
while True:
    data = stream.read(CHUNK)
    frames.append(data)

    # 입력된 데이터의 에너지를 계산하여 음성/정적 소음을 구분합니다.
    energy = sum(abs(sample) for sample in data) / len(data)
    if energy < SILENCE_THRESHOLD:
        silence_counter += 1
    else:
        silence_counter = 0

    # 종료 조건: 정적 소음 지속 시간이 SILENCE_DURATION 이상인 경우 종료합니다.
    if silence_counter > (SILENCE_DURATION * RATE / CHUNK):
        break

print("Recording finished.")

# 스트리밍 입력을 받은 오디오 데이터를 WAV 파일로 저장
audio_data = b''.join(frames)
save_wav_file(audio_data, output_file, RATE)

# 스트리밍 입력 스트림을 닫고 Pyaudio 세션을 종료합니다.
stream.stop_stream()
stream.close()
p.terminate()
