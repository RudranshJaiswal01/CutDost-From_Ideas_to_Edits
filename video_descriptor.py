import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
import os
import streamlit as st

# Configure the API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"] # Load from .env file or secrets.
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def video_descriptor(video_path: str) -> str:
    """
    Generate a detailed visual and audio description of the video with accurate timestamps.

    Args:
        video_path (str): Path to the input video file.

    Returns:
        json: Generated description of the video.
    """
    # Read the video file
    video_file = Path(video_path)
    video = {
        "mime_type": "video/mp4",
        "data": video_file.read_bytes()
    }

    # Generate content
    prompt = "You are a film editor. Give a detailed visual and audio description of the video with accurate timestamps."
    response = model.generate_content(
        [prompt, video],
        generation_config={
            "max_output_tokens": 2048*16,
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
            "response_mime_type": "application/json"
        }
    )

    return response.text