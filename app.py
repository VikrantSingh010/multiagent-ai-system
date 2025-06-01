import streamlit as st
from orchestrator.process_input import process_input
import json

st.set_page_config(page_title="Multi-Agent File Processor", layout="centered")
st.title("📂 Multi-Agent File Processor")

# Initialize session state to store result
if "result" not in st.session_state:
    st.session_state.result = None

# File uploader
uploaded_file = st.file_uploader("Choose a file (.json, .pdf, .txt)", type=["json", "pdf", "txt"])

# Process File button
if st.button("Process File") and uploaded_file:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".json"):
            input_data = json.loads(file_bytes.decode("utf-8"))
            result = process_input(json.dumps(input_data), clear_memory=True)
        elif file_name.endswith(".txt"):
            input_data = file_bytes.decode("utf-8")
            result = process_input(input_data, clear_memory=True)
        elif file_name.endswith(".pdf"):
            result = process_input(file_bytes, clear_memory=True)
        else:
            st.error("Unsupported file type.")
            result = None

        st.session_state.result = result  # store result in session state

    except Exception as e:
        st.error(f"🚨 Error processing file: {str(e)}")
        st.session_state.result = None

# Show Output button
if st.session_state.result and st.button("Show Output"):
    st.subheader("🧾 Output")
    st.json(st.session_state.result)
