import streamlit as st
import openai
import toml

# Load secrets from the .streamlit/secrets.toml file
secrets = toml.load(".streamlit/secrets.toml")

# Debug statement to check loaded secrets
# st.write(secrets)  # Uncomment this to check the secrets

# Set up OpenAI client
client = openai.OpenAI(api_key=secrets["secrets"]["OPENAI_API_KEY"])


# Password protection
def check_password():
    def password_entered():
        if st.session_state["password"] == secrets["secrets"]["app_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True


if check_password():
    st.title("ChatGPT-like Chatbot")

    # Initialize session state for storing chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Define the system prompt
    system_prompt = {
        "role": "system",
        "content": (
            "You are an expert in content writing, SEO, programming. Don't use language that is bragging, for instance don't use words like revolutionize, game changer, "
            "realm, cater, delve, ever evolving, beacon, unleash, mastery, elevate, Dive into. Don't use complicated words and language, try to write in plain English.")
    }


    def query_openai(messages):
        # Include the system prompt in the messages
        all_messages = [system_prompt] + messages
        response = client.chat.completions.create(
            model="gpt-4",
            messages=all_messages
        )
        return response.choices[0].message.content


    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("You: "):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from OpenAI
        with st.chat_message("assistant"):
            response = query_openai(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})