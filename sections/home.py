import streamlit as st

def show():
    st.markdown(
        '<div class="hero-title">🚦 Traffic Sign<br>Recognition AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-sub">AI Powered Road Intelligence Platform</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Dataset", "39,209")

    with c2:
        st.metric("Classes", "43")

    with c3:
        st.metric("Accuracy", "96.58%")

    st.write("")
    st.write("")

    st.markdown("""
    <div class='glass'>
        <h2>Why This Project?</h2>
        <p>Traffic sign recognition helps:</p>
        <ul>
            <li>Autonomous vehicles</li>
            <li>ADAS systems</li>
            <li>Smart traffic monitoring</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # EXTRA SPACE BETWEEN BOX AND BUTTON
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    if st.button("Start Detection"):
        st.session_state.selected_page = "Detection"
        st.rerun()