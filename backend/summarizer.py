# summarizer.py
from openai import OpenAI
from .utils import OPENAI_API_KEY, OUTPUT_DIR
from pathlib import Path

# Create a client using the modern OpenAI SDK
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else OpenAI()

DEFAULT_SUMMARY_PROMPT = """
You are a meeting summarization assistant.
Given the meeting transcript, produce:
1) A concise meeting summary (3-5 sentences).
2) Major decisions (bullet list).
3) Action items as: [Action] — [Owner] — [Due date if mentioned or assign TBD].
4) Any open questions.

Use bullet points for decisions and action items.
Transcript:
{transcript}
"""


def generate_summary_and_actions(transcript: str, model: str = "gpt-4o-mini"):
    prompt = DEFAULT_SUMMARY_PROMPT.format(transcript=transcript)

    # Use the new chat completions API on the client
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.2,
        )

        # The response may be an object with choices
        content = ""
        choices = getattr(resp, "choices", None) or resp.get("choices", [])
        if choices:
            first = choices[0]
            # new SDK often places message content in first.message.content
            msg = getattr(first, "message", None) or first.get("message")
            if msg:
                content = getattr(msg, "content", None) or msg.get("content", "")
            else:
                content = getattr(first, "text", None) or first.get("text", "")

        content = (content or "").strip()
    except Exception as e:
        # If the modern client call fails, surface the error
        raise

    # Save output
    out = OUTPUT_DIR / "last_summary.txt"
    out.write_text(content, encoding="utf-8")
    return content
