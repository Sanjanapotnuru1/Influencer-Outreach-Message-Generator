import sqlite3
import os

# Create database folder automatically
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(
    "database/influencer.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ==========================================
# USERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================
# INFLUENCERS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS influencers (
    influencer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    platform TEXT,
    niche TEXT,
    followers INTEGER,
    engagement_rate REAL,
    country TEXT,
    collaboration_rate REAL,
    instagram_link TEXT,
    youtube_link TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================
# CAMPAIGNS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT,
    brand_name TEXT,
    campaign_goal TEXT,
    target_audience TEXT,
    budget REAL,
    start_date DATE,
    end_date DATE,
    campaign_status TEXT
)
""")

# ==========================================
# OUTREACH MESSAGES TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS outreach_messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    influencer_id INTEGER,
    campaign_id INTEGER,
    tone TEXT,
    subject_line TEXT,
    generated_message TEXT,
    generated_by_ai BOOLEAN,
    sent_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(influencer_id)
    REFERENCES influencers(influencer_id),

    FOREIGN KEY(campaign_id)
    REFERENCES campaigns(campaign_id)
)
""")

# ==========================================
# FOLLOWUPS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS followups (
    followup_id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER,
    followup_message TEXT,
    followup_date DATE,
    followup_status TEXT,

    FOREIGN KEY(message_id)
    REFERENCES outreach_messages(message_id)
)
""")

# ==========================================
# RESPONSES TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS influencer_responses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    influencer_id INTEGER,
    message_id INTEGER,
    response_text TEXT,
    sentiment TEXT,
    response_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(influencer_id)
    REFERENCES influencers(influencer_id),

    FOREIGN KEY(message_id)
    REFERENCES outreach_messages(message_id)
)
""")

# ==========================================
# ANALYTICS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS analytics (
    analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER,
    total_messages INTEGER,
    positive_responses INTEGER,
    negative_responses INTEGER,
    response_rate REAL,
    engagement_score REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(campaign_id)
    REFERENCES campaigns(campaign_id)
)
""")

# ==========================================
# COLLABORATIONS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS collaborations (
    collaboration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    influencer_id INTEGER,
    campaign_id INTEGER,
    agreed_amount REAL,
    contract_status TEXT,
    payment_status TEXT,
    collaboration_start DATE,
    collaboration_end DATE,

    FOREIGN KEY(influencer_id)
    REFERENCES influencers(influencer_id),

    FOREIGN KEY(campaign_id)
    REFERENCES campaigns(campaign_id)
)
""")

# ==========================================
# AI PROMPT LOGS
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_prompt_logs (
    prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_text TEXT,
    ai_response TEXT,
    model_used TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()