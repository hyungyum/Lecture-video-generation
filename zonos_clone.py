import streamlit as st, torchaudio, io, torch
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

@st.cache_resource
def load():
    return Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer")

model = load()

ref = st.file_uploader("참조 음성(10–30초)", ["wav", "mp3"])
txt = st.text_input("합성 문장", "안녕하세요, Zonos 테스트입니다.")
lang = st.selectbox("언어 코드", ["ko", "en-us", "ja"], index=0)

def ensure_2d(x: torch.Tensor) -> torch.Tensor:
    if x.ndim == 3:
        x = x.squeeze(0)
    if x.ndim == 1:
        x = x.unsqueeze(0)
    return x

if st.button("Generate") and ref and txt:
    wav, sr = torchaudio.load(ref)                     # (C,T) or (T)
    spk = model.make_speaker_embedding(wav, sr)
    cond = make_cond_dict(text=txt, speaker=spk, language=lang)
    codes = model.generate(model.prepare_conditioning(cond))
    audio = ensure_2d(model.autoencoder.decode(codes).cpu()[0])

    buf = io.BytesIO()
    torchaudio.save(buf, audio, 44100, format="wav")   # Tensor now 2-D
    st.audio(buf.getvalue(), format="audio/wav")
