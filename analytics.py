import streamlit as st
import pandas as pd
import plotly.express as px

def analytics_dashboard(data):

    df = pd.DataFrame(
        data,
        columns=[
            "Message ID",
            "Influencer ID",
            "Campaign ID",
            "Tone",
            "Subject",
            "Message",
            "AI",
            "Status",
            "Created"
        ]
    )

    st.subheader("Campaign Analytics")

    st.metric(
        "Total Messages",
        len(df)
    )

    tone_chart = px.histogram(
        df,
        x="Tone"
    )

    st.plotly_chart(
        tone_chart,
        use_container_width=True
    )