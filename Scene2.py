import streamlit as st
import random
import time
import requests
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objs as go

# Dummy storage for memory
@st.cache_data
def get_priyas_history():
    return [
        {"date": "2025-04-18", "task": "7 hours of manual invoice reconciliation"},
        {"date": "2025-04-19", "task": "6.5 hours updating Excel P&L statements"},
        {"date": "2025-04-20", "task": "7.5 hours data entry: quarterly sales numbers"},
    ]

# IBM Watsonx Credentials
API_KEY = "YOUR_IBM_API_KEY"
PROJECT_ID = "YOUR_PROJECT_ID"

# Token generator
@st.cache_data(show_spinner=False)
def get_ibm_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# IBM Granite-powered question builder
@st.cache_data
def generate_questions_with_granite():
    priya_tasks = get_priyas_history()
    last_task = priya_tasks[-1]['task'] if priya_tasks else "Excel data analysis"
    prompt = f"Priya has spent hours on {last_task}. Generate 7 multiple choice questions relevant to that kind of Excel work. Each question should have 4 options and indicate the correct answer."

    access_token = get_ibm_access_token(API_KEY)
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-01-15"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 800
        },
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "project_id": PROJECT_ID
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()["results"][0]["generated_text"]
    except:
        return "Granite model error or quota exceeded."

# Stylish badge view

def show_badges():
    st.markdown("""
    ## 🏅 Achievement Unlocked
    - 🧠 **Data Viz Basics** `🆕`
    - 📊 **Excel Expert**
    """)

def suggest_next_step():
    st.markdown("## 💡 Smart Workflow Suggestion")
    st.info("Great job! Want to apply this to your quarterly report? TaskGene has reshuffled your tasks ✨")

def show_timeline():
    st.markdown("""
    ## 📊 Priya's Progress Timeline
    | Date       | Activity                               |
    |------------|----------------------------------------|
    | Apr 18     | 🧾 Manual invoice reconciliation        |
    | Apr 19     | 📈 Excel P&L statement updates          |
    | Apr 20     | 🔢 Quarterly sales data entry           |
    | Today      | 🚀 Completed micro-challenge            |
    """)

def show_skill_productivity_meters(monotony_before=75, productivity_before=82, skill_before=68,
                                    monotony_after=None, productivity_after=None, skill_after=None):
    st.markdown("## 📈 Skill & Productivity Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🧠 Monotony Score", f"{monotony_before}%" if not monotony_after else f"{monotony_after}%",
                  delta=f"{monotony_before - monotony_after}%" if monotony_after else None)
    with col2:
        st.metric("⚙️ Productivity", f"{productivity_before}%" if not productivity_after else f"{productivity_after}%",
                  delta=f"+{productivity_after - productivity_before}%" if productivity_after else None)
    with col3:
        st.metric("📚 Skill Engagement", f"{skill_before}%" if not skill_after else f"{skill_after}%",
                  delta=f"+{skill_after - skill_before}%" if skill_after else None)

    st.markdown("### 📊 Visual Skill Tracker")
    labels = ['Excel', 'Visualization', 'Automation', 'Analysis']
    values_before = [70, 50, 30, 60]
    values_after = [v + (skill_after - skill_before if skill_after else 0) for v in values_before]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values_after if skill_after else values_before, hole=.4)])
    fig.update_traces(marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig, use_container_width=True)

def get_mcq_challenges():
    return [
        {"question": "Which Excel function is best for looking up a value in a table?",
         "options": ["A. SUM", "B. VLOOKUP", "C. COUNT", "D. IF"],
         "answer": "B. VLOOKUP"},
        {"question": "What does the CONCAT function do in Excel?",
         "options": ["A. Adds numbers", "B. Joins text strings", "C. Counts cells", "D. Finds maximum"],
         "answer": "B. Joins text strings"},
        {"question": "Which chart type is best for showing trends over time?",
         "options": ["A. Pie Chart", "B. Line Chart", "C. Bar Chart", "D. Scatter Plot"],
         "answer": "B. Line Chart"},
        {"question": "What is the default file extension for Excel files?",
         "options": ["A. .docx", "B. .xls", "C. .xlsx", "D. .csv"],
         "answer": "C. .xlsx"},
        {"question": "Which function counts only numeric values?",
         "options": ["A. COUNTA", "B. COUNTIF", "C. COUNT", "D. SUM"],
         "answer": "C. COUNT"},
        {"question": "Which shortcut saves a workbook in Excel?",
         "options": ["A. Ctrl+S", "B. Ctrl+V", "C. Ctrl+P", "D. Ctrl+Z"],
         "answer": "A. Ctrl+S"},
        {"question": "Which of these is a valid Excel cell reference?",
         "options": ["A. 12A", "B. A12", "C. 1A2", "D. A-12"],
         "answer": "B. A12"}
    ]

if 'test_started' not in st.session_state:
    st.title("🎯 TaskGene Challenge Arena")
    st.markdown("""
    Welcome, Priya! 💼 
    You're 45 minutes into Q2 Sales Data work. Feeling the monotony?

    🧠 Powered by **IBM Granite**
    Ready to refresh your skills?
    """)
    if st.button("🚀 Generate Challenge Questions (IBM Granite)"):
        st.session_state.test_started = True
        st.rerun()

else:
    st.markdown("### ⏳ Generating questions using IBM Granite AI model...")
    with st.spinner("Preparing your challenge..."):
        time.sleep(5)  # simulate loading

    st.subheader("Before Test")
    show_skill_productivity_meters()

    challenges = get_mcq_challenges()
    user_answers = {}

    with st.form("challenge_form"):
        for i, challenge in enumerate(challenges):
            st.markdown(f"### {i+1}. {challenge['question']}")
            user_answers[i] = st.radio("Choose one:", challenge['options'], key=f"q{i}")
            st.markdown("---")
        submitted = st.form_submit_button("✅ Submit All")

    if submitted:
        score = 0
        for i, challenge in enumerate(challenges):
            if user_answers[i] == challenge['answer']:
                score += 1

        st.success(f"🎉 You scored {score} out of {len(challenges)}")

        if score >= 5:
            show_badges()
            suggest_next_step()
            st.balloons()
            skill_boost = 10
            productivity_boost = 3
            monotony_reduction = 5
        else:
            skill_boost = 3
            productivity_boost = 1
            monotony_reduction = 2

        st.subheader("After Test")
        show_skill_productivity_meters(
            monotony_before=75, productivity_before=82, skill_before=68,
            monotony_after=75 - monotony_reduction,
            productivity_after=82 + productivity_boost,
            skill_after=68 + skill_boost
        )

        show_timeline()
