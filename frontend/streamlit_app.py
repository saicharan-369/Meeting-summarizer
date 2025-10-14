# streamlit_app.py
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Meeting Summarizer (Demo)")
uploaded_file = st.file_uploader("Upload meeting audio", type=["wav","mp3","m4a","flac"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading and processing..."):
        resp = requests.post(f"{BACKEND_URL}/upload-audio", files=files)
    if resp.status_code == 200:
        data = resp.json()
        st.subheader("Transcript")
        st.text_area("Transcript", value=data["transcript"], height=250)
        st.subheader("Summary & Action Items")
        st.text_area("Summary", value=data["summary"], height=300)
    else:
        st.error(f"Error: {resp.status_code} {resp.text}")
