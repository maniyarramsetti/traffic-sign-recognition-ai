import streamlit as st

def show():
    st.markdown(
        '<div class="hero-title">About Project</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='glass'>
    <h2>Problem Statement</h2>
    Traffic sign recognition helps vehicles understand road signs.

    <h2>Dataset</h2>
    GTSRB Dataset with 43 traffic sign classes.

    <h2>Model</h2>
    CNN using TensorFlow / Keras.
    </div>
    """, unsafe_allow_html=True)