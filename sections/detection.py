import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.model_loader import get_model, classes

# ---------------- SAFE SESSION INIT ----------------
if "history" not in st.session_state:
    st.session_state["history"] = []

if "last_spoken" not in st.session_state:
    st.session_state["last_spoken"] = ""

# ---------------- LOAD MODEL ----------------
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
        return "HIGH RISK", "🚨", "#ff003c", "Immediate attention required"
    elif label in MEDIUM_RISK:
        return "CAUTION", "⚠️", "#ff9d00", "Drive carefully"
    else:
        return "INFO", "ℹ️", "#00cc66", "Informational traffic sign"

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

# ---------------- SHOW PREDICTION ----------------
def show_prediction(image, pred, idx, conf):
    label = classes[idx]

    voice_message = generate_voice_message(label)
    if st.session_state["last_spoken"] != label:
        speak_alert(voice_message)
        st.session_state["last_spoken"] = label

    st.session_state["history"].insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "label": label,
        "confidence": round(conf, 2)
    })

    st.session_state["history"] = st.session_state["history"][:5]

    level, icon, color, message = get_alert(label)

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
        <div style="
            background:{color}20;
            border:2px solid {color};
            padding:20px;
            border-radius:20px;
            margin-top:15px;
        ">
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

# ---------------- HISTORY ----------------
def show_history():
    st.markdown("## Recent Detections")

    if "history" not in st.session_state:
        st.session_state["history"] = []

    if len(st.session_state["history"]) == 0:
        st.info("No detections yet.")
        return

    for item in st.session_state["history"]:
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

    tab1, tab2 = st.tabs([
        "📁 Upload Image",
        "📷 Camera Capture"
    ])

    with tab1:
        uploaded = st.file_uploader(
            "Upload Traffic Sign",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            pred, idx, conf = predict_image(image)
            show_prediction(image, pred, idx, conf)

    with tab2:
        camera_image = st.camera_input("Capture Traffic Sign")

        if camera_image:
            image = Image.open(camera_image).convert("RGB")
            pred, idx, conf = predict_image(image)
            show_prediction(image, pred, idx, conf)

    st.write("")
    show_history()