import streamlit as st

def show():
    st.markdown(
        '<div class="hero-title">Developer</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='glass'>
        <h2>details</h2>
        <p><b>Name:</b> VEERA MANIKANTA DURGA PRASAD YARRAMSETTI</p>
        <p><b>Degree:</b> B.TECH FINAL YEAR</p>
        <p><b>Project:</b> Traffic Sign Recognition AI</p>
        <p><b>Skills:</b> Python, AI, Machine Learning, Deep Learning</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.markdown("### Connect With Me")

    # Center buttons using 4 columns
    c1, c2, c3, c4 = st.columns([1, 2, 2, 1])

    with c2:
        st.link_button(
            "🔗 GitHub",
            "https://github.com/maniyarramsetti"
        )

    with c3:
        st.link_button(
            "💼 LinkedIn",
            "https://www.linkedin.com/in/veera-manikanta-durga-prasad-yarramsetti-445608367/"
        )