import streamlit as st
import openai

# Set the page configuration
st.set_page_config(page_title="Talk to Us", page_icon="🗣️")

# Load OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page title
st.title("Talk to Our Emissions AI 🤖")
st.write("Ask me anything about vehicle emissions, environmental impact, or regulations!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask your emissions question here...")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI response
    with st.spinner("Thinking..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an environmental science expert. Only answer questions about vehicle emissions, fuel efficiency, pollution, or related environmental impacts."},
                    *st.session_state.messages,
                ],
            )
            ai_message = response.choices[0].message.content

            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": ai_message})

            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(ai_message)

        except openai.RateLimitError:
            with st.chat_message("assistant"):
                st.error("⚠️ Sorry, the AI service is currently unavailable. Please try again later.")