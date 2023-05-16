# 개요

사용자가 원하는 특정 단어를 설정하여 음성으로 호출할 수 있는 편리함과 가볍고 먹음직스러운 디자인으로 유동성과 시각적 만족감을 채울 수 있는 내 책상 위의 AI 비서, “MAI”를 만나보세요!

## 내용 및 재료

소프트웨어 : `opencv`, `VITO SST`(음성인식 및 TTS[Text Translate Sound]), `openai api`(chatGPT), 3D 모델링[인벤터, 또는 블렌더 + 3D 프린터 출력 프로그램(3DWOX)]
하드웨어 : 스피커, 마이크, 그래픽LCD(표정 및 글자), 3D 프린터, 배터리 케이스, 건전지

| 품명 | 사이트 | 가격 | 수량 |
| --- | --- | --- | --- |
| 스피커 | https://www.devicemart.co.kr/goods/view?no=1322046 | 4,600 | 1 |
| 마이크 | https://www.devicemart.co.kr/goods/view?no=12741849 | 7,500 | 1 |
| 그래픽LCD(표정 및 글자) | https://mecha.kr/9241 | 11,000 | 1 |
| 배터리 케이스 | 학교비품 |  | 1 |
| 건전지 | 개인지참 |  | 1 |

## 로직

- 특정 단어를 정하여 (ex.하이빅스비, 시리야) 오디오 스트리밍 입력을 텍스트로 변환했을 때 동일 시 시스템을 가동한다.
- 그래픽 LCD로 Assistant의 표정이나 얼굴을 디자인하여 모션그래픽을 나타낸다.
- openai(chatGPT)를 통해 오디오 스트리밍 입력을 통해 입력받은 텍스트를 쿼리로 사용하여 api통해 얻은 결과값을 VITO 스트리밍 SST를 사용해 스피커로 내보낸다.
- 특정 결과값이나 말할 때 등 여러 상황에 따른 글자나 표정(모션)을 그래픽 LCD로 나타낸다.
- 3D 모델링을 직접 만들고 3D 프린터를 통해 출력하여 외관을 구성하고 디자인한다.

## 스택

- Python, OpenCV, OpenAI API, VITO SST API
- AutoDesk Inventor 2023, 신도리코 FFF 3D프린터 2X + 3DWOX

## 프로토타입

디자인 → 푸딩 모양, 중간에 그래픽 LCD로 얼굴처럼 사용