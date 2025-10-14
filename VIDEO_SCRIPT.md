# Demo Video Script — Meeting Summarizer

Goal: 2-3 minute demo to show functionality, architecture, and why this project is a good fit for Unthinkable Solutions.

00:00 - 00:10 — Intro
- "Hi, I'm AYITHA VENKATA SAI CHARAN. This is my Meeting Summarizer assignment for Unthinkable Solutions' Super Dream Internship."

00:10 - 00:35 — Problem & Objective
- Briefly state the problem: meetings produce long audio; stakeholders need concise summaries and action items.
- Objective: Transcribe audio and produce decisions & action items.

00:35 - 01:05 — Architecture (screen: repo tree / README)
- Point out backend (FastAPI), ASR integration (OpenAI Whisper), LLM summarizer (OpenAI Chat), and Streamlit frontend.
- Mention Dockerfiles and how to run locally.

01:05 - 01:40 — Demo (screen: Streamlit app)
- Show login, upload a sample audio file, wait for processing, and show transcript + summary.
- Highlight extracted action items and decisions.

01:40 - 02:00 — Evaluation & Next steps
- Mention data accuracy, prompt tuning, and how to improve (speaker diarization, speaker labels, better prompt engineering).
- Call to action: provide GitHub link and deployed URL for reviewers to try.

02:00 - 02:15 — Closing
- Thank the viewer and restate contact details.

Notes:
- Keep the demo short and focused. Show the app working end-to-end.
- If network API calls are slow, record a pre-generated transcript for the demo run to show UI and summary behavior.
