# streamlit_app.py

import streamlit as st
import torch
import torchaudio
import tempfile
import os

from zonos.model import Zonos, DEFAULT_BACKBONE_CLS as ZonosBackbone
from zonos.conditioning import make_cond_dict, supported_language_codes
from zonos.utils import DEFAULT_DEVICE as device

# 버전 정보 (참고)
# torch >= 1.12.0, torchaudio >= 0.12.0, streamlit >= 1.18.0, zonos >= 0.1.0

# 페이지 설정
st.set_page_config(page_title="Zonos TTS (Streamlit)", layout="wide")

# 모델 캐시 로드
@st.cache_resource(show_spinner=False)
def load_model(model_name: str):
    model = Zonos.from_pretrained(model_name, device=device)
    model.requires_grad_(False).eval()
    return model

# 화자 오디오 임시 파일 저장 함수
def save_uploaded_audio(uploaded_file):
    if uploaded_file is None:
        return None
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

# 모델 선택 옵션 구성
supported_models = []
if "transformer" in ZonosBackbone.supported_architectures:
    supported_models.append("Zyphra/Zonos-v0.1-transformer")
if "hybrid" in ZonosBackbone.supported_architectures:
    supported_models.append("Zyphra/Zonos-v0.1-hybrid")

if len(supported_models) == 0:
    st.error("지원되는 Zonos 모델이 없습니다. zonos 패키지와 mamba-ssm 라이브러리가 올바르게 설치되었는지 확인하세요.")
    st.stop()

# 사이드바: 모델 및 기본 입력
st.sidebar.header("모델 및 입력 설정")
model_choice = st.sidebar.selectbox("모델 선택", supported_models)
text_input = st.sidebar.text_area("텍스트 입력", value="Zonos uses eSpeak for text to phoneme conversion!", height=120)
language = st.sidebar.selectbox("언어 코드", supported_language_codes, index=supported_language_codes.index("en-us") if "en-us" in supported_language_codes else 0)

prefix_audio_file = st.sidebar.file_uploader("Optional Prefix Audio (wav 파일)", type=["wav"], help="생성 시작을 위한 프리픽스 오디오", key="prefix")
speaker_audio_file = st.sidebar.file_uploader("Optional Speaker Audio (wav 파일)", type=["wav"], help="화자 클로닝용", key="speaker")
speaker_noised = st.sidebar.checkbox("화자 오디오 denoise 처리", value=False)

# 조절 가능한 파라미터
st.sidebar.markdown("### Conditioning Parameters")
dnsmos = st.sidebar.slider("DNSMOS Overall", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
fmax = st.sidebar.slider("Fmax (Hz)", min_value=0, max_value=24000, value=24000, step=1)
vqscore = st.sidebar.slider("VQ Score", min_value=0.5, max_value=0.8, value=0.78, step=0.01)
pitch_std = st.sidebar.slider("Pitch Std", min_value=0.0, max_value=300.0, value=45.0, step=1.0)
speaking_rate = st.sidebar.slider("Speaking Rate", min_value=5.0, max_value=30.0, value=15.0, step=0.5)

st.sidebar.markdown("### Generation Parameters")
cfg_scale = st.sidebar.slider("CFG Scale", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
seed = st.sidebar.number_input("Seed", value=420, step=1, format="%d")
randomize_seed = st.sidebar.checkbox("랜덤 시드 사용", value=True)

with st.sidebar.expander("Sampling Parameters"):
    linear = st.slider("Linear (0: 비활성)", min_value=-2.0, max_value=2.0, value=0.5, step=0.01)
    confidence = st.slider("Confidence", min_value=-2.0, max_value=2.0, value=0.40, step=0.01)
    quadratic = st.slider("Quadratic", min_value=-2.0, max_value=2.0, value=0.00, step=0.01)
    top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    top_k = st.slider("Top K", min_value=0, max_value=1024, value=0, step=1)
    min_p = st.slider("Min P", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

with st.sidebar.expander("Advanced (Unconditional Keys)"):
    unconditional_keys = st.multiselect(
        "Unconditional Keys",
        options=["speaker", "emotion", "vqscore_8", "fmax", "pitch_std", "speaking_rate", "dnsmos_ovrl", "speaker_noised"],
        default=["emotion"],
        help="체크된 키는 조건 없이 자동으로 채워집니다."
    )

with st.sidebar.expander("Emotion Sliders"):
    e1 = st.slider("Happiness", min_value=0.0, max_value=1.0, value=1.0, step=0.05)
    e2 = st.slider("Sadness", min_value=0.0, max_value=1.0, value=0.05, step=0.05)
    e3 = st.slider("Disgust", min_value=0.0, max_value=1.0, value=0.05, step=0.05)
    e4 = st.slider("Fear", min_value=0.0, max_value=1.0, value=0.05, step=0.05)
    e5 = st.slider("Surprise", min_value=0.0, max_value=1.0, value=0.05, step=0.05)
    e6 = st.slider("Anger", min_value=0.0, max_value=1.0, value=0.05, step=0.05)
    e7 = st.slider("Other", min_value=0.0, max_value=1.0, value=0.10, step=0.05)
    e8 = st.slider("Neutral", min_value=0.0, max_value=1.0, value=0.20, step=0.05)

# Generate 버튼
generate_button = st.button("Generate Audio")

# 버튼 클릭 시 오디오 생성
if generate_button:
    # 모델 로드
    model = load_model(model_choice)

    # 시드 설정
    if randomize_seed:
        seed = torch.randint(0, 2**32 - 1, (1,)).item()
    torch.manual_seed(int(seed))

    # 업로드 파일 저장
    prefix_path = save_uploaded_audio(prefix_audio_file)
    speaker_path = save_uploaded_audio(speaker_audio_file)

    # 화자 임베딩 처리
    SPEAKER_EMBEDDING = None
    if speaker_path is not None and "speaker" not in unconditional_keys:
        wav_spk, sr_spk = torchaudio.load(speaker_path)
        SPEAKER_EMBEDDING = model.make_speaker_embedding(wav_spk, sr_spk)
        SPEAKER_EMBEDDING = SPEAKER_EMBEDDING.to(device, dtype=torch.bfloat16)

    # audio prefix 처리
    audio_prefix_codes = None
    if prefix_path is not None:
        wav_pf, sr_pf = torchaudio.load(prefix_path)
        wav_pf = wav_pf.mean(0, keepdim=True)
        wav_pf = model.autoencoder.preprocess(wav_pf, sr_pf).to(device, dtype=torch.float32)
        audio_prefix_codes = model.autoencoder.encode(wav_pf.unsqueeze(0))

    # emotion, vq tensor 생성
    emotion_tensor = torch.tensor([e1, e2, e3, e4, e5, e6, e7, e8], device=device)
    vq_tensor = torch.tensor([vqscore] * 8, device=device).unsqueeze(0)

    # cond_dict 구성
    cond_dict = make_cond_dict(
        text=text_input,
        language=language,
        speaker=SPEAKER_EMBEDDING,
        emotion=emotion_tensor,
        vqscore_8=vq_tensor,
        fmax=float(fmax),
        pitch_std=float(pitch_std),
        speaking_rate=float(speaking_rate),
        dnsmos_ovrl=float(dnsmos),
        speaker_noised=bool(speaker_noised),
        device=device,
        unconditional_keys=unconditional_keys,
    )
    conditioning = model.prepare_conditioning(cond_dict)

    max_new_tokens = 86 * 30  # 약 30초 생성 기준
    estimated_steps = int((30 * len(text_input) / 400) * 86)

    # 진행률 표시
    progress_bar = st.progress(0)
    def progress_callback(_frame: torch.Tensor, step: int, total_steps: int) -> bool:
        progress_bar.progress(min(int(step / total_steps * 100), 100))
        return True

    # 음성 생성
    with st.spinner("Generating audio..."):
        codes = model.generate(
            prefix_conditioning=conditioning,
            audio_prefix_codes=audio_prefix_codes,
            max_new_tokens=max_new_tokens,
            cfg_scale=float(cfg_scale),
            batch_size=1,
            sampling_params=dict(
                top_p=float(top_p),
                top_k=int(top_k),
                min_p=float(min_p),
                linear=float(linear),
                conf=float(confidence),
                quad=float(quadratic),
            ),
            callback=lambda frame, step, total: progress_callback(frame, step, estimated_steps),
        )

    # 디코딩
    wav_out = model.autoencoder.decode(codes).cpu().detach()
    sr_out = model.autoencoder.sampling_rate
    if wav_out.dim() == 2 and wav_out.size(0) > 1:
        wav_out = wav_out[0:1, :]

    # 결과 출력
    st.success(f"Generation completed (Seed: {seed})")
    st.audio(wav_out.squeeze().numpy(), format="audio/wav", sample_rate=sr_out)

    # 임시 파일 정리
    if prefix_path:
        os.remove(prefix_path)
    if speaker_path:
        os.remove(speaker_path)
