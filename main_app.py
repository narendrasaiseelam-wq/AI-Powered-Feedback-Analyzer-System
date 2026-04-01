import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. LOAD API KEY
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# 2. SET UP PAGE STYLE
st.set_page_config(page_title="AI Feedback Analyzer", page_icon="✨", layout="wide")

# This is a bit of "CSS" to make it look professional
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; border: none; padding: 10px 24px; }
    </style>
    """, unsafe_allow_html=True)

# 3. UI LAYOUT
st.title("✨ AI-Powered Feedback Analyzer System")
st.write("Helping organizers turn messy Google Form data into clear event improvements.")

# Two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Event Context")
    event_name = st.text_input("What was the event name?", placeholder="e.g. Annual Tech Fest")
    event_desc = st.text_area("What was the event about?", placeholder="e.g. A 2-day coding workshop with 100 students...")

with col2:
    st.subheader("📂 Upload Feedback")
    uploaded_file = st.file_uploader("Upload your Responses (CSV or Excel)", type=["csv", "xlsx"])

# 4. PROCESSING THE FILE
if uploaded_file:
    # Read the file based on its type
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success(f"Loaded {len(df)} responses!")
    
    # Let user pick the specific column that has the feedback text
    target_column = st.selectbox("Which column contains the feedback/comments?", df.columns)
    
    # 5. THE AI ANALYSIS LOGIC
    if st.button("🚀 Generate AI Insights Report"):
        if not event_name or not event_desc:
            st.error("Please fill in the Event Name and Description first!")
        else:
            with st.spinner("🤖 AI Brain is analyzing your data... please wait..."):
                # Combine all rows of feedback into one big paragraph for the AI
                all_text = " ".join(df[target_column].astype(str).tolist())
                
                # The "Prompt" (Instructions we give to the AI)
                prompt = f"""
                You are a Friendly Event Mentor. Your goal is to help a college club student understand their event feedback easily.
                
                EVENT NAME: {event_name}
                WHAT HAPPENED: {event_desc}
                
                FEEDBACK DATA FROM STUDENTS: 
                {all_text}
                
                Please write a report that is simple, positive, and easy to read.
                
                1. **The 'Vibe' Check**: In 2-3 simple sentences, tell me the overall mood of the students.
                2. **The Highlights Table**: Create a table with these columns:
                   - 🟢 What they Loved (Props)
                   - 🔴 What to Fix (Cons)
                   - 💡 Simple Next Step (AI Suggestion)
                3. **Top 3 Encouraging Wins**: Give 3 short, 'Quick-Win' bullet points to make the next event better.
                
                   *Note: Use simple words. If there is no feedback data, just say 'Please upload feedback to see the magic!'*
                """
                
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    st.markdown("---")
                    st.header("📊 Final Analysis Report")
                    st.markdown(response.text)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Something went wrong with the AI: {e}")

# FOOTER
st.markdown("---")
st.caption("Built for AI Solution Design Assignment | Guided by Gemini")