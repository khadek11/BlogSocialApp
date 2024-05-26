import streamlit as st
import replicate
import os

# Set the app's title and favicon
st.set_page_config(page_title="Medicine Bot 🩺", page_icon="💊")

# Initialize session state for chat messages if not already initialized
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Storing API Key in the backend session state
if "replicate_api_key" not in st.session_state:
    st.session_state.replicate_api_key = "r8_5VOnOrDKTkgdWuLQrvqybDAraYvu3yo2VHUCm"
    os.environ['REPLICATE_API_TOKEN'] = st.session_state.replicate_api_key  

# Initializing LLaMA2 model
llm = ''

# Function to generate LLaMA2 response
def generate_llama2_response(prompt_input):
    temperature = st.session_state.temperature
    top_p = st.session_state.top_p
    max_length = st.session_state.max_length

    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'.\n\n"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    output = replicate.run(
        llm,  # Use the selected model
        input={"prompt": f"{string_dialogue} {prompt_input}\nAssistant: ", "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1.0}
    )
    return output

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.session_state.input_prompt = ""  # Clear input field

# Sidebar setup
with st.sidebar:
    st.title("My Health Partner 🩺")
    st.write("👋 Welcome to My Health Partner! I'm here to assist you with all your health and wellness questions. 🌟 Whether it's advice on healthy living 🥦, understanding medical conditions 🏥, or simply curious about something related to medicine 💊, feel free to ask! Let's embark on this journey to better health together! 🚀")

    st.subheader('Models and Parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

    st.session_state.temperature = st.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    st.session_state.top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    st.session_state.max_length = st.slider('Max Length', min_value=32, max_value=128, value=120, step=8)
    st.button("Clear Chat History", on_click=clear_chat_history)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input and response generation
if st.session_state.replicate_api_key:
    def submit_question():
        prompt = st.session_state.input_prompt
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.input_prompt = ""  # Clear input field

            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_llama2_response(prompt)
                    full_response = ''.join(response)
                    st.write(full_response)
                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)

    st.text_input("Ask a question about medicine or healthy living:", key="input_prompt", on_change=submit_question, placeholder="Type in your query")
else:
    st.error("Replicate API Key not set. Please set it in the backend.")
