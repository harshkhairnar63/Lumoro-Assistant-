import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, AIMessageChunk
from langgraph_database_backend import chatbot, retrieve_all_threads, submit_async_task
import uuid 
import time 
import queue
# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="centered"
)

CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>

/* Apple Typography */
html, body, [class*="css"] {
    font-family:
    "SF Pro Display",
    "SF Pro Text",
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;
}

/* App Background */
.stApp {
    background: #f5f5f7;
}

/* Main Container */
.block-container {
    max-width: 980px;
    padding-top: 3rem;
}

/* Header */
.apple-title {
    font-size: 56px;
    font-weight: 600;
    letter-spacing: -0.03em;
    text-align: center;
    color: #1d1d1f;
    margin-bottom: 10px;
}

.apple-subtitle {
    font-size: 21px;
    font-weight: 400;
    text-align: center;
    color: #6e6e73;
    margin-bottom: 50px;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

/* Message Text */
[data-testid="stChatMessageContent"] {
    color: #1d1d1f !important;
    font-size: 17px;
    line-height: 1.47;
    letter-spacing: -0.01em;
}

/* Input */
.stChatInput input {
    background: #2997ff !important;
    border: 1px solid #d2d2d7 !important;
    border-radius: 999px !important;
    color: #1d1d1f !important;
    font-size: 17px !important;    
    padding-left: 20px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #e0e0e0;
    border-right: 1px solid #e0e0e0;
}

/* Buttons */
.stButton button {
    background: #0066cc;
    color: white;
    border-radius: 999px;
    border: none;
    padding: 11px 22px;
    font-size: 17px;
    font-weight: 400;
}

.stButton button:hover {
    background: #0071e3;
}

/* Spinner */
.stSpinner {
    color: #0066cc;
}

/* Remove Streamlit top padding */
header[data-testid="stHeader"] {
    background: transparent;
}
  
</style>
""", unsafe_allow_html=True)


# ---------------------------
# Header
# ---------------------------
st.markdown(
    '<div class="apple-title"> Lumoro Assistant </div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="apple-subtitle"> Chat any time with lumoro </div>',
    unsafe_allow_html=True
)
# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = str(uuid.uuid4())
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])  


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = "user"

            elif isinstance(msg, AIMessage):
                role = "assistant"

            elif isinstance(msg, ToolMessage):
                continue

            else:
                continue

            temp_messages.append(
                {
                    "role": role,
                    "content": msg.content
                }
            )

        st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if not st.session_state["message_history"]:
    st.info(
        """
        Try:
        • What's the weather in Mumbai?
        • Current Apple stock price
        • Search latest AI news
        • List files in Documents
        """
    )

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']},
              "metadata":{"thread_id": st.session_state["thread_id"]},
              "run_name": "chart_turn",
              }

     # first add the message to message_history
    with st.chat_message("assistant"):
        status_holder = {"box": None}
        def ai_only_stream():
            event_queue: queue.Queue = queue.Queue()

            async def run_stream():
                try:
                    async for message_chunk, metadata in chatbot.astream(
                        {"messages": [HumanMessage(content=user_input)]},
                        config=CONFIG,
                        stream_mode="messages",
                    ):
                        event_queue.put((message_chunk, metadata))
                except Exception as exc:
                    event_queue.put(("error", exc))
                finally:
                    event_queue.put(None)

            submit_async_task(run_stream())

            while True:
                item = event_queue.get()
                if item is None:
                    break
                message_chunk, metadata = item
                if message_chunk == "error":
                    raise metadata

                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, (AIMessage, AIMessageChunk)):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )