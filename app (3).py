import streamlit as st
import pandas as pd
import plotly.express as px
from database import conn, cursor
from ai_engine import generate_outreach
from sentiment import analyze_sentiment

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Influencer Outreach AI CRM",
    layout="wide",
    page_icon="🚀"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #071028;
}

.stApp {
    background: linear-gradient(to right,#071028,#0B1736);
    color: white;
}

h1,h2,h3,h4 {
    color: white;
}

div[data-testid="metric-container"] {
    background: #122347;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1f3c73;
}

.stButton>button {
    background: linear-gradient(to right,#2563eb,#1d4ed8);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background: #3b82f6;
    color: white;
}

.stDataFrame {
    border-radius: 15px;
}

.sidebar .sidebar-content {
    background-color: #0B1736;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================

st.title("🚀 AI Influencer Outreach CRM")

st.markdown("""
AI-powered influencer outreach management system using:

✅ Groq Llama 3.1  
✅ SQL Database  
✅ AI Analytics  
✅ Campaign Automation  
""")

# =========================================
# SIDEBAR
# =========================================

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Add Influencer",
        "Create Campaign",
        "Generate Outreach",
        "Followups",
        "Collaborations",
        "Analytics",
        "AI Prompt Logs"
    ]
)

# =========================================
# DASHBOARD
# =========================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    cursor.execute("SELECT COUNT(*) FROM influencers")
    influencer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM campaigns")
    campaign_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM outreach_messages")
    message_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM collaborations")
    collaboration_count = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Influencers",
        influencer_count
    )

    col2.metric(
        "Campaigns",
        campaign_count
    )

    col3.metric(
        "Messages",
        message_count
    )

    col4.metric(
        "Collaborations",
        collaboration_count
    )

    st.divider()

    cursor.execute("""
    SELECT niche, COUNT(*)
    FROM influencers
    GROUP BY niche
    """)

    niche_data = cursor.fetchall()

    if niche_data:

        niche_df = pd.DataFrame(
            niche_data,
            columns=["Niche", "Count"]
        )

        fig = px.pie(
            niche_df,
            names="Niche",
            values="Count",
            title="Influencer Niches"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================
# ADD INFLUENCER
# =========================================

elif menu == "Add Influencer":

    st.header("👤 Add Influencer")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Name")
        email = st.text_input("Email")

        platform = st.selectbox(
            "Platform",
            [
                "Instagram",
                "YouTube",
                "LinkedIn",
                "TikTok"
            ]
        )

        niche = st.selectbox(
            "Niche",
            [
                "Fashion",
                "Fitness",
                "Technology",
                "Travel",
                "Gaming"
            ]
        )

    with col2:

        followers = st.number_input(
            "Followers",
            min_value=0
        )

        engagement = st.slider(
            "Engagement Rate",
            0.0,
            100.0
        )

        country = st.text_input(
            "Country"
        )

        instagram = st.text_input(
            "Instagram Link"
        )

        youtube = st.text_input(
            "YouTube Link"
        )

    if st.button("Save Influencer"):

        collaboration_rate = (
            followers * engagement
        ) / 100

        cursor.execute("""
        INSERT INTO influencers(
            name,
            email,
            platform,
            niche,
            followers,
            engagement_rate,
            country,
            collaboration_rate,
            instagram_link,
            youtube_link,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            platform,
            niche,
            followers,
            engagement,
            country,
            collaboration_rate,
            instagram,
            youtube,
            "Active"
        ))

        conn.commit()

        st.success(
            "Influencer Added Successfully"
        )

# =========================================
# CREATE CAMPAIGN
# =========================================

elif menu == "Create Campaign":

    st.header("📢 Create Campaign")

    campaign_name = st.text_input(
        "Campaign Name"
    )

    brand = st.text_input(
        "Brand Name"
    )

    goal = st.text_area(
        "Campaign Goal"
    )

    audience = st.text_input(
        "Target Audience"
    )

    budget = st.number_input(
        "Budget"
    )

    col1, col2 = st.columns(2)

    with col1:
        start = st.date_input(
            "Start Date"
        )

    with col2:
        end = st.date_input(
            "End Date"
        )

    if st.button("Create Campaign"):

        cursor.execute("""
        INSERT INTO campaigns(
            campaign_name,
            brand_name,
            campaign_goal,
            target_audience,
            budget,
            start_date,
            end_date,
            campaign_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign_name,
            brand,
            goal,
            audience,
            budget,
            start,
            end,
            "Active"
        ))

        conn.commit()

        st.success(
            "Campaign Created Successfully"
        )

# =========================================
# GENERATE OUTREACH
# =========================================

elif menu == "Generate Outreach":

    st.header("🤖 AI Outreach Generator")

    cursor.execute("""
    SELECT influencer_id, name
    FROM influencers
    """)

    influencers = cursor.fetchall()

    influencer_dict = {
        name: influencer_id
        for influencer_id, name in influencers
    }

    influencer_name = st.selectbox(
        "Select Influencer",
        list(influencer_dict.keys())
    )

    cursor.execute("""
    SELECT campaign_id, campaign_name
    FROM campaigns
    """)

    campaigns = cursor.fetchall()

    campaign_dict = {
        name: campaign_id
        for campaign_id, name in campaigns
    }

    campaign_name = st.selectbox(
        "Select Campaign",
        list(campaign_dict.keys())
    )

    tone = st.selectbox(
        "Message Tone",
        [
            "Professional",
            "Luxury",
            "Friendly",
            "Startup",
            "Gen-Z"
        ]
    )

    if st.button("Generate AI Message"):

        cursor.execute("""
        SELECT niche,
               platform,
               followers,
               engagement_rate
        FROM influencers
        WHERE name=?
        """, (influencer_name,))

        influencer_data = cursor.fetchone()

        niche = influencer_data[0]
        platform = influencer_data[1]
        followers = influencer_data[2]
        engagement = influencer_data[3]

        cursor.execute("""
        SELECT campaign_goal
        FROM campaigns
        WHERE campaign_name=?
        """, (campaign_name,))

        goal = cursor.fetchone()[0]

        response = generate_outreach(
            influencer_name,
            niche,
            platform,
            tone,
            goal
        )

        st.subheader("📩 Generated Outreach")

        st.markdown(response)

        sentiment = analyze_sentiment(
            response
        )

        st.success(
            f"Sentiment: {sentiment}"
        )

        score = (
            followers * 0.4
            +
            engagement * 100
        )

        st.info(
            f"Influencer Score: {round(score,2)}"
        )

        cursor.execute("""
        INSERT INTO outreach_messages(
            influencer_id,
            campaign_id,
            tone,
            subject_line,
            generated_message,
            generated_by_ai,
            sent_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            influencer_dict[influencer_name],
            campaign_dict[campaign_name],
            tone,
            "AI Generated Subject",
            response,
            True,
            "Pending"
        ))

        conn.commit()

        message_id = cursor.lastrowid

        # FOLLOWUP

        followup = f"""
        Hi {influencer_name},

        Just following up regarding our
        collaboration opportunity.
        """

        cursor.execute("""
        INSERT INTO followups(
            message_id,
            followup_message,
            followup_date,
            followup_status
        )
        VALUES (?, ?, DATE('now','+3 day'), ?)
        """, (
            message_id,
            followup,
            "Pending"
        ))

        conn.commit()

        # RESPONSE

        cursor.execute("""
        INSERT INTO influencer_responses(
            influencer_id,
            message_id,
            response_text,
            sentiment
        )
        VALUES (?, ?, ?, ?)
        """, (
            influencer_dict[influencer_name],
            message_id,
            "Interested in collaboration.",
            "Positive"
        ))

        conn.commit()

        # ANALYTICS

        cursor.execute("""
        INSERT INTO analytics(
            campaign_id,
            total_messages,
            positive_responses,
            negative_responses,
            response_rate,
            engagement_score
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            campaign_dict[campaign_name],
            1,
            1,
            0,
            100,
            engagement
        ))

        conn.commit()

        # COLLABORATIONS

        cursor.execute("""
        INSERT INTO collaborations(
            influencer_id,
            campaign_id,
            agreed_amount,
            contract_status,
            payment_status,
            collaboration_start,
            collaboration_end
        )
        VALUES (?, ?, ?, ?, ?, DATE('now'),
                DATE('now','+30 day'))
        """, (
            influencer_dict[influencer_name],
            campaign_dict[campaign_name],
            50000,
            "Pending",
            "Unpaid"
        ))

        conn.commit()

        st.success(
            "All Records Stored Successfully"
        )

# =========================================
# FOLLOWUPS
# =========================================

elif menu == "Followups":

    st.header("📌 Followup Messages")

    cursor.execute("""
    SELECT * FROM followups
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Message ID",
            "Followup",
            "Date",
            "Status"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# =========================================
# COLLABORATIONS
# =========================================

elif menu == "Collaborations":

    st.header("🤝 Collaborations")

    cursor.execute("""
    SELECT * FROM collaborations
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Influencer ID",
            "Campaign ID",
            "Amount",
            "Contract",
            "Payment",
            "Start",
            "End"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# =========================================
# ANALYTICS
# =========================================

elif menu == "Analytics":

    st.header("📈 Analytics Dashboard")

    cursor.execute("""
    SELECT sentiment,
           COUNT(*)
    FROM influencer_responses
    GROUP BY sentiment
    """)

    data = cursor.fetchall()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Sentiment",
                "Count"
            ]
        )

        fig = px.bar(
            df,
            x="Sentiment",
            y="Count",
            title="Influencer Response Sentiment"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================
# AI PROMPT LOGS
# =========================================

elif menu == "AI Prompt Logs":

    st.header("🧠 AI Prompt Logs")

    cursor.execute("""
    SELECT * FROM ai_prompt_logs
    """)

    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "Prompt ID",
            "Prompt",
            "AI Response",
            "Model",
            "Created"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )