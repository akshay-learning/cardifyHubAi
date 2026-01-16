import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="CardifyHub AI", layout="centered")
st.title("🤖 CardifyHub AI Pro")

with st.sidebar:
    st.title("Settings")
    key = st.text_input("Paste Gemini Key Here", type="password")

if key:
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.chat_input("Ask me anything...")
        if user_input:
            st.session_state.chat_history.append(("User", user_input))
            response = model.generate_content(user_input)
            st.session_state.chat_history.append(("AI", response.text))

        for role, text in st.session_state.chat_history:
            st.write(f"**{role}:** {text}")
            
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Sidebar mein API Key daalein!")
