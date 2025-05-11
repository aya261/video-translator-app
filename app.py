import streamlit as st
import whisper
from googletrans import Translator
import tempfile

st.set_page_config(page_title="🎥 Video Translator", layout="centered")
st.title("🎥 Video Translator App")
st.write("Upload a video, transcribe its audio, and translate it into another language!")

# Language selection
target_lang = st.selectbox(
    "Choose the target translation language:",
    ["en", "fr", "es", "de", "ar", "zh-cn"],  # You can add more ISO language codes
    format_func=lambda x: {
        "en": "English",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "ar": "Arabic",
        "zh-cn": "Chinese (Simplified)"
    }[x]
)

# Upload video
uploaded_file = st.file_uploader("Upload a video file (MP4, MOV, MKV)", type=["mp4", "mov", "mkv"])

if uploaded_file:
    st.video(uploaded_file)

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        video_path = temp_video.name

    st.info("🔄 Transcribing audio from the video...")
    model = whisper.load_model("base")  # You can try 'small' or 'medium' for better accuracy
    result = model.transcribe(video_path)
    original_text = result["text"]
    st.success("✅ Transcription complete!")

    st.text_area("📝 Original Transcription", original_text, height=200)

    st.info("🌍 Translating...")
    translator = Translator()
    translation = translator.translate(original_text, dest=target_lang)
    st.success("✅ Translation complete!")

    st.text_area("🌐 Translated Text", translation.text, height=200)

    st.download_button(
        label="💾 Download Translated Text",
        data=translation.text,
        file_name="translation.txt",
        mime="text/plain"
    )
