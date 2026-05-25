from groq import Groq
from database import cursor, conn

client = Groq(
    api_key="USE_YOUR_API_KEY"
)

def generate_outreach(
        influencer,
        niche,
        platform,
        tone,
        campaign_goal):

    prompt = f"""
    Generate a highly professional influencer outreach message.

    Influencer Name: {influencer}
    Niche: {niche}
    Platform: {platform}
    Tone: {tone}
    Campaign Goal: {campaign_goal}

    Generate:
    1. Email Subject
    2. Personalized Outreach Message
    3. Follow-up Message
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=700
    )

    response = completion.choices[0].message.content

    cursor.execute("""
    INSERT INTO ai_prompt_logs(
        prompt_text,
        ai_response,
        model_used
    )
    VALUES (?, ?, ?)
    """, (
        prompt,
        response,
        "llama-3.1-8b-instant"
    ))

    conn.commit()

    return response