import argparse
import pyaudio
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--sample_rate", type=int, default=44100, help="Sample rate of the input audio")
    parser.add_argument("--encoding", type=str, default="pcm_s16le", help="Encoding of the input audio")
    args = parser.parse_args()

    # config = MyConfig()
    # config.sample_rate = args.sample_rate
    # config.encoding = args.encoding
    # config.use_itn = True
    # config.use_disfluency_filter = False
    # config.use_profanity_filter = False
    
    # config = pb.DecoderConfig(
    #     sample_rate=args.sample_rate,
    #     encoding=args.encoding,
    #     use_itn=True,
    #     use_disfluency_filter=False,
    #     use_profanity_filter=False,
    # )

    # 마이크로 입력 스트림 설정
    p = pyaudio.PyAudio()
    stream = p.open(format=args.encoding,
                    channels=1,
                    rate=args.sample_rate,
                    input=True,
                    frames_per_buffer=1024)

    # 실시간 입력 처리
    try:
        while True:
            # 버퍼에서 데이터 읽기
            audio_data = stream.read(1024)
            audio_samples = np.frombuffer(audio_data, dtype=np.int16)
            print("오디오 데이터 : " + audio_data + "\n오디오 샘플(원시데이터) : " + audio_samples)
            # API로 데이터 스트리밍
            # 여기에 데이터를 API로 전송하는 코드를 작성하면 됩니다.
            # config 및 audio_samples를 사용하여 API 호출을 수행합니다.

    except KeyboardInterrupt:
        pass

    # 스트림 종료
    stream.stop_stream()
    stream.close()
    p.terminate()
