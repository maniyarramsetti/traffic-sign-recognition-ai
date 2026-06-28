import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px
from utils.model_loader import get_model, classes

model = get_model()

def show():
    st.markdown('<div class="hero-title">Detection</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.success("Model Loaded")
    c2.info("CNN Active")
    c3.warning("CPU Mode")

    uploaded = st.file_uploader(
        "Upload Traffic Sign",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")

        col1, col2 = st.columns([1, 1.4])

        with col1:
            st.image(image, width=300)

        img = np.array(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (32, 32))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)
        idx = np.argmax(pred)
        conf = np.max(pred) * 100

        with col2:
            st.markdown(f"""
            <div class='glass'>
            <h2>Prediction Result</h2>
            <h1>{classes[idx]}</h1>
            <h2>Confidence: {conf:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)

        top_idx = pred[0].argsort()[-5:][::-1]

        df = pd.DataFrame({
            "Class": [classes[i] for i in top_idx],
            "Probability": [pred[0][i]*100 for i in top_idx]
        })

        fig = px.bar(
            df,
            x="Probability",
            y="Class",
            orientation="h"
        )

        st.plotly_chart(fig, use_container_width=True)