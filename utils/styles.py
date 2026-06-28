def apply_styles(st):
    st.markdown("""
    <style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    section[data-testid="stSidebar"] {
        display: none;
    }

    .stApp{
        background:
        radial-gradient(circle at top left,#ff003c 0%,transparent 30%),
        radial-gradient(circle at bottom right,#990022 0%,transparent 30%),
        linear-gradient(135deg,#050505,#13000a);
        color:white;
    }

    .hero-title{
        font-size:82px;
        font-weight:900;
        color:white;
        line-height:1;
        text-shadow:0 0 25px rgba(255,0,60,0.5);
    }

    .hero-sub{
        font-size:26px;
        color:#dddddd;
    }

    .glass{
        background: rgba(255,255,255,0.08);
        border:1px solid rgba(255,255,255,0.18);
        border-radius:28px;
        padding:28px;
        backdrop-filter: blur(20px);
        box-shadow:0 8px 30px rgba(0,0,0,0.45);
    }

    img{
        border-radius:25px !important;
    }
    </style>
    """, unsafe_allow_html=True)