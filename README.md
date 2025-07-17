# Lecture Video Generation

## Overview
이 프로젝트는 **Zonos**의 오픈소스 TTS 모델과 **OpenAI API**, **Streamlit UI**를 결합하여  
`.pptx` 또는 `.pdf` 문서로부터 자동으로 **멀티모달 강의 비디오**를 생성합니다.


## Requirements
- **OS**: Ubuntu 22.04/24.04 이상 제안 (다른 리눅스 배포판 사용 가능하나 미검증)
- **GPU**: NVIDIA GPU 권장 (최소 6GB VRAM), CPU 환경 실행 시 성능 저하 발생
- 
## Project Structure
```
Zonos/                          ← 프로젝트 최상위 폴더
├─ mmmaaaiiinnn.py              ← Streamlit 앱 진입점
├─ samples/                     ← 예제 PPT 및 영상 파일
│   ├─ 딥러닝.pptx
│   ├─ 미국의 역사.pptx
│   ├─ 딥러닝.mp4
│   └─ 미국의 역사.mp4
├─ .env                         ← API 키 보관 (Git 추적 제외)
├─ requirements.txt             ← Python 패키지 목록
└─ README.md                    ← 프로젝트 설명 파일
```

## Quick Start

아래 순서대로 한 줄씩 실행하면 프로젝트를 처음부터 끝까지 설정하고 실행할 수 있습니다.

1. **Zonos 저장소 클론**
   ```bash
   git clone https://github.com/Zyphra/Zonos.git
   cd Zonos
   ```
2. **시스템 의존성 설치 (Ubuntu)**
   ```bash
   sudo apt update
   sudo apt install -y espeak-ng libreoffice poppler-utils ffmpeg
   ```
3. **Zonos Python 모듈 설치**
   ```bash
   pip install -e .
   pip install --no-build-isolation -e .[compile]
   ```
4. **원본 위치로 이동 & Lecture Video Generation 저장소 클론**
   ```bash
   cd your_repo/
   git clone https://github.com/hyungyum/Lecture-video-generation.git
   cd Zonos
   ```
5. **앱 의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```
6. **환경 변수 설정**
   프로젝트 루트에 `.env` 파일 생성 후 다음을 추가하세요.
   ```text
   OPENAI_API_KEY=sk-...
   ```
   `.gitignore`에 `.env`를 추가하여 Git 추적에서 제외합니다.
7. **앱 실행**
   ```bash
   streamlit run mmmaaaiiinnn.py
   ```

## Project Structure
```
Zonos/                          ← 프로젝트 최상위 폴더
├─ mmmaaaiiinnn.py              ← Streamlit 앱 진입점
├─ samples/                     ← 예제 PPT 및 영상 파일
│   ├─ 딥러닝.pptx
│   ├─ 미국의 역사.pptx
│   ├─ 딥러닝.mp4
│   └─ 미국의 역사.mp4
├─ .env                         ← API 키 보관 (Git 추적 제외)
├─ requirements.txt             ← Python 패키지 목록
└─ README.md                    ← 프로젝트 설명 파일
```

## Modes
- **강의 자료 생성**: PDF 기반 슬라이드 텍스트 추출 및 PPTX 생성
- **강의 영상 생성**: PDF/PPTX 기반 멀티모달 강의 비디오 생성 (.mp4)

