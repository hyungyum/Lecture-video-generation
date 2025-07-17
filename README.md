# Lecture-video-generation



```markdown
# Lecture Video Generation

## Overview
이 프로젝트는 **Zonos**의 오픈소스 TTS 모델과 **OpenAI API**, **Streamlit UI**를 결합하여  
`.pptx` 또는 `.pdf` 문서로부터 자동으로 **멀티모달 강의 비디오**를 생성합니다.

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

````

## Prerequisites

### 1. System Requirements
- Ubuntu 22.04/24.04 또는 macOS  
- (Hybrid) 3000-series 이상 NVIDIA GPU 권장, 최소 6GB VRAM  
- CPU 실행 가능하나 속도 저하 발생

### 2. System Dependencies (Zonos)  
Zonos는 **eSpeak** 기반 phonemization을 사용합니다.  
```bash
# Ubuntu
sudo apt update
sudo apt install -y espeak-ng

# macOS
brew install espeak-ng
````

강의 비디오 변환용 추가 도구:

```bash
sudo apt install -y libreoffice poppler-utils ffmpeg
```

### 3. Python Dependencies (Zonos & App)

Zonos 설치 권장 절차 (uv 환경 관리자):

```bash
pip install -U uv
uv sync
uv sync --extra compile
uv pip install -e .
```

앱 의존성은 `requirements.txt`로 관리:

```bash
pip install -r requirements.txt
```

환경 변수 설정:

```text
.env
├─ OPENAI_API_KEY=sk-...
└─ REPLICATE_API_TOKEN=rp-...
```

`.gitignore`에 `.env` 추가하여 커밋 제외

## Installation

1. **Zonos** 저장소 클론

   ```bash
   git clone https://github.com/Zyphra/Zonos.git
   cd Zonos
   ```
2. **Lecture Video Generation** 저장소 클론

   ```bash
   cd ~/Desktop/streamlit
   git clone https://github.com/hyungyum/Lecture-video-generation.git Zonos
   cd Zonos
   ```
3. 시스템 의존성 설치 (eSpeak, LibreOffice, Poppler, FFmpeg)
4. Python 패키지 설치

   ```bash
   pip install -r requirements.txt
   ```

## Usage

앱 실행:

```bash
streamlit run mmmaaaiiinnn.py
```

1. 사이드바에서 모드 선택
2. PPTX/PDF 파일 업로드 → **변환 시작** 클릭
3. 스크립트 생성 → 음성 합성 → 이미지 생성 → 비디오 합성
4. 완료 후 **비디오 다운로드**

## Contributing

1. Fork → `feature/YourFeature` 브랜치 생성
2. 수정 후 커밋 → PR 생성
3. 리뷰 후 Merge

## License

MIT License

```
::contentReference[oaicite:0]{index=0}
```
