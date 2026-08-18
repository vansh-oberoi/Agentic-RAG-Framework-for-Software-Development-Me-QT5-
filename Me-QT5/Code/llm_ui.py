import streamlit as st
from datetime import datetime, timedelta
import time
import requests

from wrapper import LLMSession

api_port = 9696
url = f"http://localhost:{api_port}/ask"  # Update if your service runs on a different host/port


obj = LLMSession()

def send_request(prompt:str):
    # response = requests.post(url, json={"prompt": prompt})

    # # Check if the request was successful
    # if response.status_code == 200:
    #     # Get the response content
    #     data = response.json()
    #     return data.get("response")
    # else:
    #     return f"Error:{response.status_code, response.text}"

    return obj.query(prompt)
    
#-----------------------------------------------------------------
# Page configuration
st.set_page_config(
    page_title="ME-QT5",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for layout improvements
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #1E1E1F;
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #181818;
        padding: 1rem;
    }
    
    /* Centered chat container styling */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding-top: 2rem;
    }

    /* Input box styling - Darker background */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    [data-testid="stChatInput"] {
        background-color: #202123 !important;
        color: white;
        border-radius: 0.75rem;
        padding: 1rem;
        border: 1px solid #565869;
    }
    
    /* Chat input area specific styling */
    [data-testid="stChatInput"] {
        background-color: #202123;
        border-color: #565869;
    }
    
    /* Chat input container styling */
    .stChatFloatingInputContainer {
        background-color: #1E1E1F !important;
        border-top: 1px solid #2D2D2F;
        padding: 1.5rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #202123;
        color: #FFFFFF;
        border: 1px solid #565869;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #1E1E1F;
        border: 1px solid #2D2D2F;
    }
    .assistant-message {
        background-color: #2B2B2F;
    }
    
    /* Time period headers */
    .time-period {
        color: #777;
        font-size: 0.8rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Chat history items */
    .chat-history-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 0.3rem;
        cursor: pointer;
        color: #ECECF1;
    }
    .chat-history-item:hover {
        background-color: #252526;
    }
    
    /* Disclaimer styling */
    .disclaimer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 1rem;
        padding: 1rem;
        background-color: #1E1E1F;
    }
    
    /* Remove extra padding and margins */
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {
        'yesterday': ['Go constants vs define', 'DFT with Zero Padding', 'Self-starting Synchronous Motors'],
        'previous_7_days': ['Code without Comments', 'SJF Task Scheduling'],
    }

# Initialize API variables
tavilly_api = ""
hgf_api = ""

# Sidebar
with st.sidebar:
    # API input fields
    tavilly_api = st.text_input("Tavilly", type="password")
    hgf_api = st.text_input("Hugging-Face", type="password")

# Main content area
main_container = st.container()
with main_container:
    if not st.session_state.messages:
        st.markdown("<h1 style='text-align: center; color: white; margin-top: 20vh;'>What can I help with?</h1>", 
                    unsafe_allow_html=True)

    # Display chat messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        st.markdown(f"""
            <div class='chat-message {"user-message" if message["role"] == "user" else "assistant-message"}'>
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    simulated_response_a, simulated_response_b  = send_request(prompt)
    
    with st.chat_message("assistant"):
        st.code(simulated_response_a)
        st.markdown(simulated_response_b)
    
# Disclaimer
st.markdown("""
    <div class='disclaimer'>
        ME-QT5 can make mistakes. Check important info.
    </div>
""", unsafe_allow_html=True)