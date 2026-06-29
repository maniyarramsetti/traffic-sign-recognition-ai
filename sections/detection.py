import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av

from utils.model_loader import get_model, classes

model = get_model()

# ---------------- ALERT CATEGORIES ----------------
HIGH_RISK = [
    "Stop",
    "No entry",
    "Pedestrians",
    "Children crossing"
]

MEDIUM_RISK = [
    "Road work",
    "Slippery road",
    "Traffic signals"
]

if "history" not in st.session_state:
    st.session_state.history = []

if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = ""

if "live_prediction" not in st.session_state:
    st.session_state.live_prediction = "Waiting..."

if "live_confidence" not in st.session_state:
    st.session_state.live_confidence = 0


# ---------------- VOICE ----------------
def speak_alert(message):
    js = f"""
    <script>
    const msg = new SpeechSynthesisUtterance("{message}");
    msg.rate = 1;
    msg.pitch = 1;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)


def generate_voice_message(label):
    if label == "Stop":
        return "Warning. Stop sign detected."
    elif label == "No entry":
        return "Alert. No entry sign detected."
    elif label == "Pedestrians":
        return "Caution. Pedestrian crossing ahead."
    elif label == "Children crossing":
        return "Warning. Children crossing ahead."
    else:
        return f"{label} detected."


# ---------------- ALERT ----------------
def get_alert(label):
    if label in HIGH_RISK:
        return "HIGH RISK", "🚨", (0, 0, 255), "Immediate attention required"
    elif label in MEDIUM_RISK:
        return "CAUTION", "⚠", (0, 165, 255), "Drive carefully"
    else:
        return "INFO", "ℹ", (0, 255, 0), "Informational traffic sign"


# ---------------- IMAGE PREDICTION ----------------
def predict_image(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (32, 32))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img, verbose=0)
    idx = np.argmax(pred)
    conf = np.max(pred) * 100

    return pred, idx, conf


# ---------------- LIVE VIDEO PROCESSOR ----------------
class LiveProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        resized = cv2.resize(img, (32, 32))
        normalized = resized.astype("float32") / 255.0
        input_img = np.expand_dims(normalized, axis=0)

        pred = model.predict(input_img, verbose=0)
        idx = np.argmax(pred)
        conf = float(np.max(pred) * 100)
        label = classes[idx]

        st.session_state.live_prediction = label
        st.session_state.live_confidence = conf

        level, icon, color, _ = get_alert(label)

        cv2.rectangle(img, (20, 20), (620, 110), color, -1)

        cv2.putText(
            img,
            f"{icon} {label}",
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            img,
            f"Confidence: {conf:.2f}%",
            (40, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# ---------------- NORMAL PREDICTION UI ----------------
def show_prediction(image, pred, idx, conf):
    label = classes[idx]

    voice_message = generate_voice_message(label)
    if st.session_state.last_spoken != label:
        speak_alert(voice_message)
        st.session_state.last_spoken = label

    st.session_state.history.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "label": label,
        "confidence": round(conf, 2)
    })

    st.session_state.history = st.session_state.history[:5]

    level, icon, _, message = get_alert(label)

    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.image(image, width=320)

    with col2:
        st.markdown(f"""
        <div class='glass'>
            <h2>Prediction Result</h2>
            <h1>{label}</h1>
            <h3>Confidence: {conf:.2f}%</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='glass'>
            <h2>{icon} {level}</h2>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=conf,
        title={'text': "Confidence Meter"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    st.plotly_chart(gauge, use_container_width=True)

    top_idx = pred[0].argsort()[-5:][::-1]

    df = pd.DataFrame({
        "Class": [classes[i] for i in top_idx],
        "Probability": [pred[0][i] * 100 for i in top_idx]
    })

    fig = px.bar(
        df,
        x="Probability",
        y="Class",
        orientation="h",
        title="Top Predictions"
    )

    st.plotly_chart(fig, use_container_width=True)


def show_history():
    st.markdown("## Recent Detections")

    if len(st.session_state.history) == 0:
        st.info("No detections yet.")
        return

    for item in st.session_state.history:
        st.markdown(f"""
        <div class='glass' style='margin-bottom:12px'>
            <b>{item['time']}</b><br>
            {item['label']} — {item['confidence']}%
        </div>
        """, unsafe_allow_html=True)
        # ---------------- MAIN PAGE ----------------
def show():
    st.markdown(
        '<div class="hero-title">Detection</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    c1.success("Model Loaded")
    c2.info("CNN Active")
    c3.warning("CPU Mode")

    st.write("")

    tab1, tab2, tab3 = st.tabs([
        "📁 Upload Image",
        "📷 Camera Capture",
        "🎥 Live Detection"
    ])

    # ---------------- UPLOAD TAB ----------------
    with tab1:
        uploaded = st.file_uploader(
            "Upload Traffic Sign",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            pred, idx, conf = predict_image(image)
            show_prediction(image, pred, idx, conf)

    # ---------------- CAMERA TAB ----------------
    with tab2:
        camera_image = st.camera_input("Capture Traffic Sign")

        if camera_image:
            image = Image.open(camera_image).convert("RGB")
            pred, idx, conf = predict_image(image)
            show_prediction(image, pred, idx, conf)

    # ---------------- LIVE TAB ----------------
    with tab3:
        st.markdown("""
        <div class='glass'>
            <h2>🚘 Advanced HUD Live Detection</h2>
            <p>Real-time AI webcam detection with ADAS-style dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        webrtc_streamer(
            key="traffic-live-detection",
            video_processor_factory=LiveProcessor,
            media_stream_constraints={
                "video": True,
                "audio": False
            }
        )

        st.write("")

        # Live dashboard
        pred_label = st.session_state.live_prediction
        pred_conf = st.session_state.live_confidence

        level, icon, _, message = get_alert(pred_label)

        d1, d2, d3 = st.columns(3)

        with d1:
            st.metric("Live Prediction", pred_label)

        with d2:
            st.metric("Confidence", f"{pred_conf:.2f}%")

        with d3:
            st.metric("Alert Level", level)

        st.markdown(f"""
        <div class='glass'>
            <h2>{icon} {level}</h2>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)

        live_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred_conf,
            title={'text': "Live Confidence"},
            gauge={'axis': {'range': [0, 100]}}
        ))

        st.plotly_chart(live_gauge, use_container_width=True)

    st.write("")
    show_history()