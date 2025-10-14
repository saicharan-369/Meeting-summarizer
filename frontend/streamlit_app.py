# streamlit_app.py
import os
import streamlit as st
import requests
from datetime import datetime

# Read backend URL from environment so deployments can point to the public backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def _local_css():
    st.markdown(
        """
        <style>
        .hero {background: linear-gradient(135deg,#6EE7B7 0%,#3B82F6 100%); padding: 40px; border-radius: 12px; color: white}
        .section {padding: 18px 12px}
        .card {border-radius: 8px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.08);}
        .small {font-size:12px; color:#6b7280}
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ''
    if 'last_upload' not in st.session_state:
        st.session_state.last_upload = None


def login_flow():
    st.header("Sign in to continue")
    with st.form("login_form"):
        email = st.text_input("Email")
        name = st.text_input("Full name")
        submitted = st.form_submit_button("Sign in")
        if submitted:
            if email.strip() == '':
                st.error("Please enter an email.")
            else:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = name or email.split('@')[0]
                st.success(f"Signed in as {st.session_state.user_name}")


def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = ''
    st.session_state.user_name = ''
    st.experimental_rerun()


def home_page():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("""
    <h1 style='margin:0'>Meeting Summarizer</h1>
    <p style='margin-top:8px; font-size:16px'>Fast, accurate meeting transcription and concise summaries with action items and decisions — powered by OpenAI Whisper + Chat.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>\n')

    st.markdown("## Features")
    col1, col2, col3 = st.columns([1,1,1])
    col1.markdown("**Accurate Transcription**\n\nWe use state-of-the-art ASR to transcribe audio quickly.")
    col2.markdown("**Concise Summaries**\n\nGet meeting summaries (3-5 sentences), decisions, and action items.")
    col3.markdown("**Action Items**\n\nAction items are extracted and presented with owners and due dates when available.")

    st.markdown("---")

    st.markdown("### Why this project")
    st.write(
        "This meeting summarizer demonstrates backend + frontend integration, real-world API usage, and a clean UX — ideal for showcasing in internship drives."
    )


def upload_page():
    st.header("Upload Meeting Audio")
    if not st.session_state.logged_in:
        st.info("Please sign in to upload audio.")
        return

    st.markdown("Upload an audio file (wav, mp3, m4a, flac). The backend will transcribe and summarize the meeting.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["wav","mp3","m4a","flac"])
    if uploaded_file is not None:
        show_preview = st.checkbox("Show transcript & summary on completion", value=True)
        with st.spinner("Uploading and processing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                resp = requests.post(f"{BACKEND_URL}/upload-audio", files=files, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                st.success("Processing complete")
                st.session_state.last_upload = {'filename': data.get('filename'), 'time': datetime.utcnow().isoformat()}
                if show_preview:
                    st.subheader("Transcript")
                    st.text_area("Transcript", value=data.get("transcript",""), height=250)
                    st.subheader("Summary & Action Items")
                    st.text_area("Summary", value=data.get("summary",""), height=300)
            except Exception as e:
                st.error(f"Upload failed: {e}")


def profile_page():
    st.header("User Profile & Assignment")
    if not st.session_state.logged_in:
        st.info("Please sign in to view profile.")
        return

    st.markdown("""
    <div class='card'>
    <h3>Owner</h3>
    <p><strong>AYITHA VENKATA SAI CHARAN</strong></p>
    <p class='small'>Candidate for Unthinkable Solutions - Super Dream Internship Registration - 2026 Batch</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Assignment details")
    st.write("Project: Meeting Summarizer")
    st.write("Deadline to submit the assignment: 15th Oct 2025")
    st.write("Purpose: Submit the summarized meeting app as part of the internship application.")

    st.markdown("---")
    st.markdown("### Internship drive details")
    st.markdown(
        """
    - Company: **Unthinkable Solutions**
    - Category: Super Dream Internship
    - CTC: 1,000,000
    - Stipend: 37,000
    - Last date to register: 01/10/2025 10:00 AM
    - Location: Gurgaon
    """
    )


def assignment_submission():
    st.header("Assignment Submission")
    st.markdown("Please submit your assignment link (GitHub or deployed URL) below. Deadline: 15th Oct 2025")
    link = st.text_input("Enter public URL to your deployed app or GitHub repo")
    if st.button("Submit assignment"):
        if not link:
            st.error("Please paste a public link before submitting.")
        else:
            st.success("Assignment submitted successfully (demo). Make sure to share this link with the company form.")
            st.write("Submitted link:", link)


def main():
    _local_css()
    init_state()

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Home", "Login", "Upload Audio", "Profile", "Assignment"])

    if menu == "Home":
        home_page()
    elif menu == "Login":
        if st.session_state.logged_in:
            st.success(f"Logged in as {st.session_state.user_name} ({st.session_state.user_email})")
            if st.button("Logout"):
                logout()
        else:
            login_flow()
    elif menu == "Upload Audio":
        upload_page()
    elif menu == "Profile":
        profile_page()
    elif menu == "Assignment":
        assignment_submission()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"Backend: {BACKEND_URL}")


if __name__ == '__main__':
    main()

