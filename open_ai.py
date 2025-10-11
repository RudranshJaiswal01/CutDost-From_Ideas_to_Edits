import os
import json
from typing import List, Optional
from groq import Groq
from pydantic import BaseModel
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# Load environment
# ----------------------------------------------------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API not found in environment. Please set it in .env")

client = Groq(api_key=GROQ_API_KEY)

# ----------------------------------------------------------------------
# Structured response schema
# ----------------------------------------------------------------------
class AIResponse(BaseModel):
    message: str
    editing_code: Optional[str] = None
    required_libs: Optional[List[str]] = None
    reason: Optional[str] = None

# ----------------------------------------------------------------------
# Generate response with schema
# ----------------------------------------------------------------------
def generate_response(
    library_choice: str,
    user_message: str,
    video_desc: str,
    video_file_path: str,
    assets: dict,
    chat_history: list,
    model_name="openai/gpt-oss-120b"
):
    """
    Returns structured response with:
      - message (chat to user)
      - editing_code (optional Python code for editing)
      - required_libs (optional list of libraries required)
      - reason (assistant's short reasoning, shown as 'Thought for this second')
    """

    if library_choice not in ["MoviePy", "Movis"]:
        raise ValueError(f"Unsupported library choice: {library_choice}")

    system_prompt = (
        f"You are a professional Python video editor assistant. "
        f"You only generate Python code for {library_choice} video editing and descriptive text. "
        f"Main video description: {video_desc}\n"
        f"Main video file path: {video_file_path}\n"
        f"Available assets (file paths): {assets}\n"
        "Edited Video File Path: output.mp4\n\n"
        "Rules:\n"
        "- Always respond in **JSON** following the exact schema.\n"
        "- 'message': Friendly reply to the user in plain text (never include code here).\n"
        "- 'editing_code': Only include valid Python editing code when edits are required.\n"
        "- 'required_libs': List libraries needed **only if editing_code is provided**.\n"
        "- 'reason': A short 1–2 sentence explanation of why you replied this way (shown as a thought).\n"
        "- Do not output instructions to run the code — the system will run it automatically.\n"
        "- If code is provided, it must be complete, executable, and use the uploaded assets.\n"
        "- Never hallucinate features. If unsure, ask user for clarification instead of guessing.\n"
    )


    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "ai_response",
                    "schema": AIResponse.model_json_schema(),
                },
            },
            temperature=0.1,
            max_completion_tokens=8192*8,
            top_p=1,
            reasoning_effort="high",
            # tools=[{"type":"code_interpreter"}]
        )
        response_text = response.choices[0].message.content
        print(response.choices[0].message)
        ai_resp = AIResponse.model_validate(json.loads(response_text))
        return ai_resp.model_dump()
    except Exception as e:
            return {
                "message": f"⚠️ Sorry, I failed. Error: {str(e)}",
                "editing_code": None,
                "required_libs": None,
                "reason": "System could not complete the request, needs user clarification.",
            }
