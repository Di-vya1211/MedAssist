import streamlit as st

st.set_page_config(page_title="Test Popover")
st.write("Main Page Content")

if "bot_history" not in st.session_state:
    st.session_state.bot_history = [
        {"role": "assistant", "content": "Hello! I am your MedAssist AI. How may I help you today?"}
    ]

with st.popover("🤖 How may I help you?", help="Chat with MedAssist AI"):
    st.markdown("### 🤖 MedAssist Bot")
    st.caption("🟢 Online • How may I help you?")
    
    for msg in st.session_state.bot_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    with st.form("test_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question:", placeholder="Type here...")
        submitted = st.form_submit_button("Send")
        if submitted and user_input:
            st.session_state.bot_history.append({"role": "user", "content": user_input})
            st.session_state.bot_history.append({"role": "assistant", "content": f"You asked: {user_input}"})
            st.rerun()

st.write("End of page")
