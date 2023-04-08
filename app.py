import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

PAGE_TITLE = "A New Friend"
PAGE_ICON = "👯"
LAYOUT = "wide"
SESSION_STATE_KEYS = ["generated", "past", "input", "stored_session"]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []


def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                               placeholder="Your AI assistant here! Ask me anything ...",
                               label_visibility='hidden')
    return input_text


def new_chat():
    save = ["User:" + msg for msg in st.session_state["past"]] + \
        ["Bot:" + msg for msg in st.session_state["generated"]]
    st.session_state["stored_session"].append(save)
    for key in SESSION_STATE_KEYS:
        st.session_state[key] = []
    st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()


col1, col2, col3, col4 = st.sidebar.columns(4)
col2.image("https://em-content.zobj.net/thumbs/240/apple/354/alien_1f47d.png",
           width=130)
col3.image("https://em-content.zobj.net/thumbs/240/apple/354/sparkles_2728.png",
           width=130)
col1.write("")
col4.write("")
with st.sidebar.expander("🤖 How this app works"):
    st.markdown('''
- The required libraries are StreamLit, LangChain and OpenAI.
- The st.session_state object is used to store the conversation history, user input, generated output, and stored session.
- The ```get_text()``` function creates a text input field using ```st.text_input``` to get user input. The function returns the input text.
- The ```new_chat()``` function is triggered by the "New Chat" button and saves the current conversation history to the stored session. The function also clears the conversation history, entity memory store, and buffer.
- The sidebar is set up with ```st.sidebar.columns``` to create three columns. The first two columns contain images, and the third column is empty. The explanation and settings expanders are created using ```st.sidebar.expander```.
- The ```MODEL``` and ```K``` settings are set using ```st.selectbox``` and ```st.number_input```, respectively. ```MODEL``` selects the LLM model to use, and ```K``` sets the number of prompts to consider for each response.
- The ```API_O``` text input field is used to get the OpenAI API key from the user.
- The ```llm``` object is created using the OpenAI class with the specified settings, and the ```ConversationEntityMemory``` object is created using the ```llm``` and ```K``` values.
- The ```ConversationChain``` object is created using the ```llm```, ```ENTITY_MEMORY_CONVERSATION_TEMPLATE```, and ```entity_memory``` objects.
- The ```user_input``` variable is set to the result of ```get_text()``` function.
- The ```ConversationChain``` object's ```run()``` function is called with the ```user_input``` as ```input```. The output is stored in the output variable.
- If output is ```not None```, the conversation history is updated with the user input and generated output, and the updated conversation is displayed in the expandable "Conversation" section.
- The ```st.download_button``` is used to create a download button to download the conversation history as a text file.
- The ```stored_session``` is displayed in the sidebar as expandable sections with the conversation history.
- If the "Clear-all" checkbox is selected, the stored_session object is deleted.
        '''
                )

with st.sidebar.expander(" 🛠️ Settings ", expanded=False):
    if st.checkbox("Preview memory store"):
        st.write(st.session_state.entity_memory.store)
    if st.checkbox("Preview memory buffer"):
        st.write(st.session_state.entity_memory.buffer)
    MODEL = st.selectbox(label='Model', options=[
                         'gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'code-davinci-002'])
    K = st.number_input(' (#)Summary of prompts to consider',
                        min_value=3, max_value=1000)

st.title(PAGE_TITLE)
st.subheader("A conversational AI assistant that remembers what you say")

API_O = st.sidebar.text_input(":blue[Enter Your OPENAI API-KEY :]",
                              placeholder="Paste your OpenAI API key here (sk-...)", type="password")

if API_O:
    llm = OpenAI(temperature=0.7, openai_api_key=API_O,
                 model_name=MODEL, verbose=False)
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)
    Conversation = ConversationChain(
        llm=llm, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, memory=st.session_state.entity_memory)
else:
    st.markdown('''
    ```  
    Start Here: 
        - 1. Enter your OpenAI API key to use this app 🔐
        - 2. Change language model and other freatures under Settings 📝 
        - 3. Start chatting! 🚀
    ''')
    st.sidebar.warning(
        'API key is required to try this app. The API key is not stored in any form.')

st.sidebar.button("New Chat", on_click=new_chat, type='primary')
user_input = get_text()

st.sidebar.write(
    ":robot_face: Application created by [@Kirby_](https://twitter.com/Kirby_) & GPT-4")
st.sidebar.write(
    ":link: Utilizing [@LangChainAI](https://twitter.com/LangChainAI)")
st.sidebar.write(
    ":point_right: The code for this app is available on [GitHub](https://github.com/jaredkirby)")

if user_input:
    output = Conversation.run(input=user_input)
    if output:
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

        with st.expander("Conversation", expanded=True):
            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                st.info(st.session_state["past"][i], icon="🧐")
                st.success(st.session_state["generated"][i], icon="🤖")
            download_str = '\n'.join(
                st.session_state["past"] + st.session_state["generated"])
            if download_str:
                st.download_button('Download', download_str)

for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label=f"Conversation-Session:{i}"):
        st.write(sublist)

if st.session_state.stored_session:
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session
