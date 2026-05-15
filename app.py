import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIG (Customizes the tab name and icon)
st.set_page_config(page_title="Gemi's AI Agent", page_icon="🤖", layout="wide")

# 2. DYNAMIC SIDEBAR (Customizable settings)
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    model_choice = st.selectbox("Choose Intelligence Level:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.info("Your API Key is only used for this session and is not stored.")

# 3. MAIN INTERFACE
st.title("📩 AI Enquiry Processor")
st.subheader("Your Personal Triage Agent")

# Input field for the user
user_query = st.text_area("Paste the enquiry/email here:", height=200)

# 4. THE PROCESSING LOGIC
if st.button("Analyze Enquiry"):
    if not api_key:
        st.error("❌ Please provide an API key in the sidebar first!")
    elif not user_query:
        st.warning("⚠️ The enquiry box is empty.")
    else:
        with st.status("🤖 AI is thinking...", expanded=True) as status:
            try:
                # Configure the AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_choice)
                
                # Dynamic Prompting
                prompt = f"Analyze this enquiry. Categorize it (Spam, Support, Lead), determine urgency, and suggest a reply: {user_query}"
                
                response = model.generate_content(prompt)
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                # Display Results in a nice layout
                st.success("### Analysis Result")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")