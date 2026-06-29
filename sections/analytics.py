import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


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


def get_risk(label):
    if label in HIGH_RISK:
        return "High Risk"
    elif label in MEDIUM_RISK:
        return "Medium Risk"
    else:
        return "Low Risk"


def generate_pdf(history):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("Traffic Sign Recognition AI Report", styles["Title"])
    )
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(f"Total Detections: {len(history)}", styles["Normal"])
    )
    elements.append(Spacer(1, 10))

    if len(history) == 0:
        elements.append(
            Paragraph("No detections available.", styles["Normal"])
        )
    else:
        for item in history:
            line = (
                f"Time: {item['time']} | "
                f"Sign: {item['label']} | "
                f"Confidence: {item['confidence']}%"
            )
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 5))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def show():
    st.markdown(
        '<div class="hero-title">Analytics</div>',
        unsafe_allow_html=True
    )

    history = st.session_state.get("history", [])
    total_detections = len(history)

    if total_detections > 0:
        avg_conf = round(
            sum(item["confidence"] for item in history) / total_detections,
            2
        )

        labels = [item["label"] for item in history]
        most_common = max(set(labels), key=labels.count)

        high_risk_count = sum(
            1 for item in history
            if get_risk(item["label"]) == "High Risk"
        )
    else:
        avg_conf = 0
        most_common = "None"
        high_risk_count = 0

    # KPI CARDS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Detections", total_detections)
    c2.metric("High Risk Alerts", high_risk_count)
    c3.metric("Avg Confidence", f"{avg_conf}%")
    c4.metric("Most Common Sign", most_common)

    st.write("")

    # TRAINING GRAPH
    st.markdown("## Model Training Performance")

    df_train = pd.DataFrame({
        "Epoch": [1,2,3,4,5,6,7,8,9,10],
        "Accuracy": [72,80,85,88,91,93,94,95,96,96.58]
    })

    fig_train = px.line(
        df_train,
        x="Epoch",
        y="Accuracy",
        markers=True,
        title="Training Accuracy Curve"
    )

    st.plotly_chart(fig_train, use_container_width=True)

    if total_detections == 0:
        st.info("No detections yet. Use Detection page first.")
        return

    # PIE CHART
    st.markdown("## Risk Distribution")

    risk_data = pd.DataFrame({
        "Risk": [get_risk(item["label"]) for item in history]
    })

    risk_counts = risk_data["Risk"].value_counts().reset_index()
    risk_counts.columns = ["Risk", "Count"]

    fig_pie = px.pie(
        risk_counts,
        names="Risk",
        values="Count",
        title="Risk Level Breakdown"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # TOP DETECTED SIGNS
    st.markdown("## Top Detected Signs")

    sign_counts = pd.DataFrame({
        "Sign": [item["label"] for item in history]
    })

    sign_counts = sign_counts["Sign"].value_counts().reset_index()
    sign_counts.columns = ["Sign", "Count"]

    fig_bar = px.bar(
        sign_counts,
        x="Sign",
        y="Count",
        title="Detection Frequency"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # TABLE
    st.markdown("## Recent Detection Records")

    df_history = pd.DataFrame(history)
    st.dataframe(df_history, use_container_width=True)

    # DOWNLOAD REPORTS
    st.markdown("## Download Reports")

    csv = df_history.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name="traffic_report.csv",
        mime="text/csv"
    )

    pdf_file = generate_pdf(history)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="traffic_report.pdf",
        mime="application/pdf"
    )