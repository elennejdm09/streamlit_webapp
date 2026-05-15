import os
import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIG (Customizes the tab name and icon)
st.set_page_config(page_title="Gemi's AI Agent", page_icon="🤖", layout="wide")

# 2. DYNAMIC SIDEBAR (Customizable settings)
with st.sidebar:
    st.title("⚙️ Settings")
    # Try to get key from Streamlit secrets or environment first
    default_key = None
    if "GEMINI_API_KEY" in st.secrets:
        default_key = st.secrets["GEMINI_API_KEY"]
    elif os.environ.get("GEMINI_API_KEY"):
        default_key = os.environ.get("GEMINI_API_KEY")

    if default_key:
        st.success("Using GEMINI_API_KEY from Streamlit secrets / environment.")
        api_key = default_key
    else:
        api_key = st.text_input("Enter your Gemini API Key:", type="password")

    model_choice = st.selectbox("Choose Intelligence Level:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    st.info("Your API Key is only used for this session and is not stored. For Cloud deploys, set `GEMINI_API_KEY` in Streamlit secrets.")

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
                err = str(e)
                # Provide actionable guidance for common API key errors
                if "API key not valid" in err or "API_KEY_INVALID" in err:
                    st.error("API key not valid. Please check your key and project settings.")
                    st.markdown("**Quick fixes to try:**\n\n- Ensure you created an **API key** (not an OAuth token or service account JSON).\n- In Google Cloud Console enable the **Generative Language API** (generativelanguage.googleapis.com).\n- Make sure billing is enabled for the project that owns the API key.\n- If the key has API restrictions, allow `generativelanguage.googleapis.com` or remove restrictions.\n- If deploying on Streamlit Cloud, set `GEMINI_API_KEY` in the app's Secrets (do not paste in public code).")
                else:
                    st.error(f"An error occurred: {e}")