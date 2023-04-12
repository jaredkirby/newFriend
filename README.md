# A New Friend: Conversational AI Assistant

A New Friend is a Streamlit web app that provides a conversational AI assistant using OpenAI's GPT-4 model. The app has an interactive user interface that allows users to engage in a conversation with the AI, store multiple chat sessions, and download chat history.

## Features

- Conversational AI assistant based on OpenAI's GPT-4 model
- Remembers context and entities during conversation
- Allows users to choose different language models and settings
- Stores multiple conversation sessions
- Download chat history as a text file
- Preview memory store and buffer

## Installation

To use this app, you will need to install the required libraries:

bashCopy code

`pip install streamlit langchain openai`

## Usage

To run the app, navigate to the directory containing the `app.py` file and run:

bashCopy code

`streamlit run app.py`

This will launch the web app in your default browser. To interact with the AI, provide your OpenAI API key and start chatting.

## How it works

- The app uses Streamlit, LangChain, and OpenAI libraries.
- The `st.session_state` object is used to store the conversation history, user input, generated output, and stored sessions.
- A `get_text()` function is used to create a text input field to get user input.
- A `new_chat()` function is triggered by the "New Chat" button to save the current conversation history and clear the chat history, entity memory store, and buffer.
- The sidebar is set up with `st.sidebar.columns` to create four columns. The first two columns contain images, and the third and fourth columns are empty. The explanation and settings expanders are created using `st.sidebar.expander`.
- The `MODEL` and `K` settings are set using `st.selectbox` and `st.number_input`, respectively. `MODEL` selects the LLM model to use, and `K` sets the number of prompts to consider for each response.
- The `llm` object is created using the `OpenAI` class with the specified settings, and the `ConversationEntityMemory` object is created using the `llm` and `K` values.
- The `ConversationChain` object is created using the `llm`, `ENTITY_MEMORY_CONVERSATION_TEMPLATE`, and `entity_memory` objects.
- The `user_input` variable is set to the result of the `get_text()` function.
- The `ConversationChain` object's `run()` function is called with the `user_input` as `input`. The output is stored in the output variable.
- If output is `not None`, the conversation history is updated with the user input and generated output, and the updated conversation is displayed in the expandable "Conversation" section.
- The `st.download_button` is used to create a download button to download the conversation history as a text file.
- The `stored_session` is displayed in the sidebar as expandable sections with the conversation history.
- If the "Clear-all" checkbox is selected, the stored_session object is deleted.

## Credits

- Application created by [@Kirby_](https://twitter.com/Kirby_) & GPT-4
- Utilizing [@LangChainAI](https://twitter.com/LangChainAI)
