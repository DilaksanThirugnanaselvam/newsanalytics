import streamlit as st
import openai
import requests
from datetime import datetime, timedelta

# Initialize OpenAI API
openai.api_key = "openai.api_key"  # Replace with your actual OpenAI API key


# Telegram Bot Token and Channel Chat ID (replace with your actual values)
TELEGRAM_BOT_TOKEN = "7845194271:AAHd07FXO4UB4aAw24xlXmMFnGkV6Q4v1JQ"  # Replace with your actual Telegram bot token
TELEGRAM_CHAT_ID = "-1002496992612"  # Your Telegram channel username (e.g., @newsdilak)

# Function to send messages to Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    return response.ok

# Function to generate and summarize news with emojis
def generate_and_send_news(news_data, period, period_date):
    prompt = f"Today is {datetime.now().strftime('%B %d, %Y')}. Below are the generated news articles with clickable links and emojis for the {period} period (deadline on or before {period_date}):\n\n"

    emoji_map = {
        "scholarship": "🎓",
        "technology": "💻",
        "international": "🌎",
        "women": "👩‍💻",
        "general": "📰"
    }

    for news in news_data:
        title = news.get('title', 'No Title')
        link = news.get('url', '#')
        category = news.get('category', 'general')
        emoji = emoji_map.get(category, "📰")
        prompt += f"- {emoji} <a href='{link}'>{title}</a>\n"

    prompt += (
        "\nSummarize these articles with concise, attractive points, and use emojis to make them engaging."
    )

    # Generate summary using GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    summary = response['choices'][0]['message']['content'].strip()

    # Format message for Telegram and send
    telegram_message = f"<b>News Updates ({period.capitalize()} Deadline)</b>\n\n" + summary
    send_to_telegram(telegram_message)

    return summary

# Function to categorize deadlines
def categorize_deadlines():
    today = datetime.now()
    week_later = today + timedelta(days=7)
    month_later = today + timedelta(days=30)

    return today.strftime("%B %d, %Y"), week_later.strftime("%B %d, %Y"), month_later.strftime("%B %d, %Y")

# Sample news data with categories and URLs
news_data = [
    {"title": "Global STEM Scholarship for Students Worldwide", "url": "https://www.globalstemscholarship.org", "category": "scholarship"},
    {"title": "Advances in Artificial Intelligence", "url": "https://www.techadvances.com", "category": "technology"},
    {"title": "Women in Technology International Scholarship", "url": "https://www.womenintechnology.org", "category": "women"},
    {"title": "Undergraduate Scholarship for International Students", "url": "https://www.internationalscholarships.com", "category": "international"}
]

# Streamlit app layout
st.title("📰 AI-Powered News with Emojis")
st.markdown("Get AI-generated news updates, categorized and enhanced with engaging emojis!")

# Categorize deadlines and generate summaries for each period
today, week_later, month_later = categorize_deadlines()

st.subheader("News Articles")
for news in news_data:
    title = news.get('title', 'No Title')
    link = news.get('url', '#')
    emoji = "📌"  # Static emoji for listing
    st.markdown(f"{emoji} [{title}]({link})")

st.subheader("Generated Summaries")

st.markdown("### Today's News")
summary_today = generate_and_send_news(news_data, "day", today)
st.write(summary_today)

st.markdown("### This Week's News")
summary_week = generate_and_send_news(news_data, "week", week_later)
st.write(summary_week)

st.markdown("### This Month's News")
summary_month = generate_and_send_news(news_data, "month", month_later)
st.write(summary_month)

can we get a timer? 
like scheduled pushing no deployment app

