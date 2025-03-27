import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)





import streamlit as st
from src.Brain.sim_router import function_call_gem_gemini_similarity 
from src.Functions.exe_function import execute_routing_call
from src.Conversations.text_speech import text_to_speech_local
from src.Conversations.voice_text import voice_to_text
import tempfile
import os
st.set_page_config(layout="wide")


st.sidebar.image("./static/logo.png", use_container_width=True)
st.markdown("<h1 style='text-align: center; color: gray;'>🌍 Finance  Management System</h1>", unsafe_allow_html=True)


st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #FF6F61;
    color: black;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    border-radius: 20px;
    padding: 5px 10px;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    text-align: center;
}
div.stButton > button:first-child:hover {
    background-color: green;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}
div.stButton > button:first-child:focus {
    outline: none;
    box-shadow: 0 0 0 4px rgba(255, 111, 97, 0.5);
}
div.stButton > button[disabled] {
    background-color: #ddd;
    cursor: not-allowed;
    opacity: 0.6;
    box-shadow: none;
}

/* Styling the checkbox */
div[data-testid="stCheckbox"] {
    display: flex;
    align-items: center;
    font-size: 14px;
    font-weight: bold;
    justify-content: center;
    background-color: #4CAF50;
    border-radius: 50px;
    padding: 6px 16px;
    transition: 0.3s;
    cursor: pointer;
    width: fit-content;
    margin: auto;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
div[data-testid="stCheckbox"]:hover {
    background-color: red;
}
div[data-testid="stCheckbox"] > label {
    color: black !important;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "audio_input_key_counter" not in st.session_state:
    st.session_state.audio_input_key_counter = 0



def add_message(role, content):
    """Prevent duplicate messages before adding to session state."""
    if not any(msg["content"] == content and msg["role"] == role for msg in st.session_state.messages):
        st.session_state.messages.append({"role": role, "content": content})
        
def talk_to_agent(query):
    list_of_calls = function_call_gem_gemini_similarity(query)
    list_of_solutions = []
    for func in list_of_calls:
        solution = execute_routing_call(func)
        list_of_solutions.append(str(solution))
    return  "\n".join(list_of_solutions)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "html":
            st.components.v1.html(message["content"], height=700, scrolling=True)
            st.session_state.messages = [msg for msg in st.session_state.messages if msg["role"] != "html"]
        else:
            st.markdown(message["content"], unsafe_allow_html=True)
            

audio_input_key = f"audio_input_key_{st.session_state.audio_input_key_counter}"
audio_value = st.sidebar.audio_input(label="Voice", key=audio_input_key)
on = st.sidebar.toggle("🗣️ Voice Reply")
if audio_value:
    print("recorded value")
    
    with tempfile.TemporaryFile(suffix=".wav") as temp_audio:
        temp_audio.write(audio_value.getvalue())
        temp_audio.seek(0)  # Move to the beginning of the file
        
        transcribed_text = voice_to_text(temp_audio)
        transcribed_text = transcribed_text
        if transcribed_text:
            st.chat_message("user").markdown(transcribed_text)
            #st.session_state.messages.append({"role": "user", "content": transcribed_text})
            add_message("user",transcribed_text)
            response = talk_to_agent(transcribed_text)
            bot_response = f"**{response}**"
            st.chat_message("assistant").markdown(bot_response)
            
            if on:
                print("on")
                if response.strip():
                    audio_io = text_to_speech_local(response.replace("*", ""))
                    # Autoplay audio using HTML audio tag
                    st.markdown(f"""
                        <audio autoplay="true">
                            <source src="data:audio/mp3;base64,{audio_io}" type="audio/mp3">
                        </audio>
                        """, unsafe_allow_html=True)
                    #st.audio(audio_io, format="audio/wav")
            else:
                st.warning("No valid response to speak.")

            #st.session_state.messages.append({"role": "assistant", "content": response})
            add_message("assistant",bot_response)
            del st.session_state[audio_input_key]
            st.session_state.audio_input_key_counter += 1


if user_input := st.chat_input("Ask about disasters, weather, or precautions..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = talk_to_agent(user_input)
    bot_response = f"**{response}**"
    st.chat_message("assistant").markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": response})

