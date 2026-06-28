import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.markdown('<div class="hero-title">Analytics</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Training Accuracy", "98.2%")
    c2.metric("Validation Accuracy", "96.58%")
    c3.metric("Classes", "43")

    df = pd.DataFrame({
        "Epoch":[1,2,3,4,5,6,7,8,9,10],
        "Accuracy":[72,80,85,88,91,93,94,95,96,96.58]
    })

    fig = px.line(df, x="Epoch", y="Accuracy")
    st.plotly_chart(fig, use_container_width=True)