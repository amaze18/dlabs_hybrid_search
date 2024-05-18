import streamlit as st
from openai import OpenAI
import os

# Set your OpenAI API key
YOUR_API_KEY = os.environ["SECRET_API_KEY"]
# Initialize the OpenAI client
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# Initialize session state for messages if not already initialized
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to get response from the custom model API
def get_custom_model_response(messages):
    modified_messages = []
    for message in messages:
        if message["role"] == "user":
            modified_message = {"role": "user", "content": f"{message['content']} I-venture ISB"}
        else:
            modified_message = message
        modified_messages.append(modified_message)
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=modified_messages,
    )
    return response.choices[0].message.content

# Streamlit UI setup
st.title("I-Venuture @ ISB : AI Chatbot, developed by [GurukulAI](https://anupam-purwar.github.io/page/research_group.html)!! ")


with st.sidebar:
   
    st.title("🤗💬I-Venuture @ ISB : AI Chatbot")
    st.success('Access to this Gen-AI Powered Chatbot is provided by [Anupam](https://anupam-purwar.github.io/page/research_group.html)!!', icon='✅')
    hf_email = 'anupam_purwar2019@pgp.isb.edu'
    hf_pass = 'PASS'

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    prompt1=f"{prompt} I-venture ISB"
    st.session_state.messages.append({"role": "user", "content": str(prompt1)})
    
    # Append "ISB" to the user's question internally
    

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If the last message is not from the assistant, generate a new response
if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare the conversation history for the API request
            conversation_history = [
                {"role": "system", 
                 "content": "You are an artificial intelligence assistant which answers questions related to I-Venture at ISB or DLabs ISB from web search and you need to engage in a helpful, detailed, conversation with a user. Also list sources of answer."}]  + st.session_state.messages
            #"You are an artificial intelligence assistant which answers questions related to I-Venture at ISB and you need to engage in a helpful, detailed, conversation with a user."}
           

            # Get the response from the custom model API
            response = get_custom_model_response(conversation_history)

            # Append the assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
