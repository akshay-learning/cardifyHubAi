import streamlit as st
import google.generativeai as genai
import requests
import json
import base64
from io import BytesIO

# --- Page Configuration & Styling ---
st.set_page_config(page_title="CardifyHub Ultimate AI", page_icon="🚀", layout="wide")

# Custom CSS for a premium, dark theme look with better spacing
st.markdown("""
    <style>
    .main {
        background-color: #1a1a2e; /* Darker background */
        color: #e0e0e0; /* Light grey text */
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
    }
    .stButton>button {
        background-color: #0f3460; /* Darker blue for buttons */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1a5e8a; /* Lighter blue on hover */
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #3e4a61;
        background-color: #2c2c4a;
        color: #e0e0e0;
        padding: 10px;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #3e4a61;
        background-color: #2c2c4a;
        color: #e0e0e0;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        color: #a0a0a0;
    }
    .stTabs [data-baseweb="tab-list"] button.st-emotion-cache-1litx2v { /* Active tab color */
        background-color: #0f3460;
        color: white;
        border-radius: 8px 8px 0 0;
    }
    .stAlert {
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 CardifyHub Ultimate AI")
st.caption("AIzaSyDDrjoP7vX542WvggMsQHqsbjytfqLjzcs")

# --- API Keys & Configuration ---
# Apni Gemini Key yahan ' ' ke beech mein daalein
DEFAULT_GEMINI_KEY = "AIzaSyDDrjoP7vX542WvggMsQHqsbjytfqLjzcs"

# Stability AI API Key for Image Generation (Free tier requires sign-up)
# Sign up here: https://platform.stability.ai/account/keys
# Agar aapke paas Stability AI key nahi hai, toh ye feature kaam nahi karega
DEFAULT_STABILITY_KEY = "sk-HNCi25nKectAEvj066vgdt60zSXdOcQsJc29quL1pEcSeWzD" 

# For Video Generation: Use a free service API if available or self-hosted
# For demo, we'll use a placeholder or a simple message.
# Real video generation is complex and often paid.
# For a truly free video, you might need to find an open-source model on HuggingFace and deploy it.
# For now, we'll simulate it or use a very basic free offering if found.
DEFAULT_VIDEO_KEY = "APNI_VIDEO_GEN_KEY_YAHAN_DAALEIN" 

# --- SESSION STATE INITIALIZATION ---
if "gemini_messages" not in st.session_state:
    st.session_state.gemini_messages = []
if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0
if "image_counter" not in st.session_state:
    st.session_state.image_counter = 0
if "video_counter" not in st.session_state:
    st.session_state.video_counter = 0

# --- SIDEBAR FOR SETTINGS & KEYS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Control Panel")
    
    st.subheader("Your API Keys")
    user_gemini_key = st.text_input("Gemini AI Key (Chat)", type="password", help="Google Gemini se chat ke liye")
    user_stability_key = st.text_input("Stability AI Key (Image)", type="password", help="Images banane ke liye")
    # user_video_key = st.text_input("Video Gen Key (Optional)", type="password", help="Videos banane ke liye") # Uncomment if you get a video API

    st.markdown("---")
    st.subheader("Free Usage Limits")
    st.info(f"Chat: {st.session_state.chat_counter}/10")
    st.info(f"Images: {st.session_state.image_counter}/3")
    st.info(f"Videos: {st.session_state.video_counter}/1 (Limited Free Trials)")
    st.markdown("---")
    st.write("📫 **Support:** cardifyhub@contact.com")

# Decide which keys to use
final_gemini_key = user_gemini_key if user_gemini_key else DEFAULT_GEMINI_KEY
final_stability_key = user_stability_key if user_stability_key else DEFAULT_STABILITY_KEY
# final_video_key = user_video_key if user_video_key else DEFAULT_VIDEO_KEY # For video key

# --- Usage Limits ---
FREE_CHAT_LIMIT = 10
FREE_IMAGE_LIMIT = 3
FREE_VIDEO_LIMIT = 1 # Video generation is generally more restrictive for free

# --- TABS FOR DIFFERENT FUNCTIONALITIES ---
chat_tab, image_tab, video_tab = st.tabs(["💬 AI Chat", "🖼️ Image Generator", "🎬 Video Creator"])

# --- AI CHAT TAB ---
with chat_tab:
    st.header("💬 Talk to CardifyHub AI")
    st.write("Aap yahan code likhwa sakte ho, essay likhwa sakte ho, ya koi bhi sawal puch sakte ho.")

    for message in st.session_state.gemini_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat_prompt = st.chat_input("Type your message here...")

    if chat_prompt:
        if st.session_state.chat_counter >= FREE_CHAT_LIMIT and not user_gemini_key:
            st.error(f"🛑 Chat Free Limit Reached ({FREE_CHAT_LIMIT}/{FREE_CHAT_LIMIT})! Please add your own Gemini API Key in the sidebar for unlimited use.")
        else:
            st.session_state.gemini_messages.append({"role": "user", "content": chat_prompt})
            with st.chat_message("user"):
                st.markdown(chat_prompt)
            
            try:
                genai.configure(api_key=final_gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = model.generate_content(chat_prompt)
                        st.markdown(response.text)
                
                st.session_state.gemini_messages.append({"role": "assistant", "content": response.text})
                st.session_state.chat_counter += 1
                st.sidebar.info(f"Chat: {st.session_state.chat_counter}/10") # Update sidebar immediately

            except Exception as e:
                st.error(f"Chat Error: Please check your Gemini API Key in the sidebar or try again. Details: {e}")

# --- IMAGE GENERATOR TAB ---
with image_tab:
    st.header("🖼️ Generate Stunning Images")
    st.write("Apna idea type karo aur AI uski photo bana dega. (Powered by Stability AI)")

    image_prompt = st.text_input("Describe the image you want to create (e.g., 'A futuristic city at sunset, cyberpunk style')", key="image_input")
    
    if st.button("Generate Image"):
        if not image_prompt:
            st.warning("Please enter a description for the image.")
        elif st.session_state.image_counter >= FREE_IMAGE_LIMIT and not user_stability_key:
            st.error(f"🛑 Image Free Limit Reached ({FREE_IMAGE_LIMIT}/{FREE_IMAGE_LIMIT})! Add your own Stability AI Key in the sidebar.")
        else:
            try:
                st.info("Generating your image... This might take a moment.")
                # Stability AI API Call (DALL-E se sasta aur free tier me better hai)
                # Replace with actual Stability AI endpoint and parameters
                headers = {
                    "Accept": "application/json",
                    "Authorization": f"Bearer {final_stability_key}"
                }
                payload = {
                    "text_prompts": [
                        {
                            "text": image_prompt
                        }
                    ],
                    "cfg_scale": 7,
                    "height": 512,
                    "width": 512,
                    "samples": 1,
                    "steps": 30,
                }
                
                # Using Stability AI's Stable Diffusion XL model
                response = requests.post(
                    f"https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    for i, image in enumerate(data["artifacts"]):
                        st.image(base64.b64decode(image["base64"]), caption=f"Generated Image {i+1}")
                        st.download_button(
                            label=f"Download Image {i+1}",
                            data=base64.b64decode(image["base64"]),
                            file_name=f"cardifyhub_image_{i+1}.png",
                            mime="image/png"
                        )
                    st.session_state.image_counter += 1
                    st.sidebar.info(f"Images: {st.session_state.image_counter}/{FREE_IMAGE_LIMIT}") # Update sidebar immediately
                else:
                    st.error(f"Image Generation Failed: {response.status_code} - {response.text}")
                    st.warning("Please ensure your Stability AI Key is correct and has active credits.")

            except Exception as e:
                st.error(f"Image Generation Error: {e}")
                st.warning("Could not connect to image generation service. Check your API key or try again later.")

# --- VIDEO CREATOR TAB (Simulated for Free Tier) ---
with video_tab:
    st.header("🎬 Create Short Videos from Text")
    st.write("Apna description type karo aur AI uski short video banane ki koshish karega. (Limited Free Access)")

    video_prompt = st.text_input("Describe the video you want (e.g., 'A short sci-fi film clip with robots dancing')", key="video_input")
    
    if st.button("Generate Video"):
        if not video_prompt:
            st.warning("Please enter a description for the video.")
        elif st.session_state.video_counter >= FREE_VIDEO_LIMIT: # No external key check for video here for simplicity as free options are rare
            st.error(f"🛑 Video Free Limit Reached ({FREE_VIDEO_LIMIT}/{FREE_VIDEO_LIMIT})! Video generation is very resource-intensive and often requires paid access.")
            st.markdown("Try services like [RunwayML](https://app.runwayml.com/login) or [PikaLabs](https://www.pika.art/) for limited free trials.")
        else:
            st.info("Initiating video generation... This can take several minutes and is highly experimental for free tiers.")
            st.warning("Real-time, high-quality video generation is extremely complex and costly. This is a simulated/very basic free attempt.")

            # --- SIMULATED VIDEO GENERATION ---
            # For truly free video generation, you'd need to find a free open-source API (e.g., Hugging Face Space for AnimateDiff)
            # and integrate it here. This part is a placeholder.
            try:
                # Placeholder: In a real scenario, you'd call a video generation API here.
                # Example (concept only):
                # video_response = requests.post("YOUR_FREE_VIDEO_API_ENDPOINT", headers=video_headers, json={"prompt": video_prompt})
                # if video_response.status_code == 200:
                #     video_url = video_response.json()["video_url"]
                #     st.video(video_url, format="video/mp4", start_time=0)
                #     st.download_button(label="Download Video", data=requests.get(video_url).content, file_name="generated_video.mp4", mime="video/mp4")
                # else:
                #     st.error(f"Video API Failed: {video_response.text}")

                # --- MOCK VIDEO GENERATION (for demonstration without a real free API) ---
                # This will show a placeholder video and a message.
                
                # Fetching a placeholder video from Pexels (free stock video)
                # In a real app, this would be your generated video.
                mock_video_url = "https://assets.mixkit.co/videos/preview/mixkit-street-performer-with-a-red-light-show-4416-large.mp4" # Replace with a generic video URL
                
                st.video(mock_video_url, format="video/mp4", start_time=0)
                st.download_button(
                    label="Download Sample Video", # Change to "Download Generated Video" when real
                    data=requests.get(mock_video_url).content,
                    file_name="cardifyhub_sample_video.mp4", # Change to generated_video.mp4
                    mime="video/mp4"
                )
                st.success("Video generation request processed (displayed a sample video). Actual free video generation is very limited.")

                st.session_state.video_counter += 1
                st.sidebar.info(f"Videos: {st.session_state.video_counter}/{FREE_VIDEO_LIMIT}") # Update sidebar immediately

            except Exception as e:
                st.error(f"Video Generation Error: {e}")
                st.warning("Could not connect to video generation service. Free video APIs are rare and often unreliable. Try paid services.")
