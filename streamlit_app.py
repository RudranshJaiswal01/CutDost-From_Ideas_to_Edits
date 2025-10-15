import os
import subprocess, sys
import time
import streamlit as st
from pathlib import Path
from open_ai import generate_response
from video_descriptor import video_descriptor

# -------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------
st.set_page_config(page_title="🎬 AI Video Editing Assistant", layout="wide")

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "assets" not in st.session_state:
    st.session_state.assets = {}
if "video_desc" not in st.session_state:
    st.session_state.video_desc = "No description yet."
if "last_output" not in st.session_state:
    st.session_state.last_output = None

# -------------------------------------------------
# Sidebar – File Upload & Library Choice
# -------------------------------------------------
st.sidebar.header("📂 Project Setup")

library_choice = st.sidebar.selectbox("Choose editing library:", ["MoviePy", "Movis"])
st.session_state.library_choice = library_choice

uploaded_file = st.sidebar.file_uploader("Upload your main video (MP4)", type=["mp4"])
if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", "main_video.mp4")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.session_state.assets["main_video"] = file_path

    # Auto-generate video description if not already done
    if st.session_state.video_desc == "No description yet.":
        with st.spinner("Analyzing video..."):
            try:
                st.session_state.video_desc = video_descriptor(file_path)
                st.sidebar.success("✅ Video description generated!")
            except Exception as e:
                st.sidebar.error(f"❌ Video analysis failed: {e}")

# Show video description in a dropdown
with st.sidebar.expander("📑 Video Description"):
    st.text_area("Auto-generated description", st.session_state.video_desc, height=250)

# -------------------------------------------------
# Main Content – Video Preview + Chat
# -------------------------------------------------
st.title("🎬 AI Video Editing Assistant")

# Video Preview (top)
if st.session_state.last_output and Path(st.session_state.last_output).exists():
    st.video(st.session_state.last_output)
elif "main_video" in st.session_state.assets:
    st.video(st.session_state.assets["main_video"])

st.divider()

# -------------------------------------------------
# Chat Interface
# -------------------------------------------------
st.subheader("💬 Chat with your AI editor")

user_input = st.chat_input("Describe your edit request...")
if st.session_state.chat_history:
    with st.chat_message("user"):
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])
                    if msg.get("reason"):
                        st.caption(f"🤔 Thought: {msg['reason']}")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    ai_resp = generate_response(
        library_choice=st.session_state.library_choice,
        user_message=user_input,
        video_desc=st.session_state.video_desc,
        video_file_path=st.session_state.assets["main_video"],
        assets=st.session_state.assets,
        chat_history=st.session_state.chat_history,
    )

    # Store assistant message
    st.session_state.chat_history.append({"role": "assistant", "content": ai_resp["message"]})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(ai_resp["message"])
        with st.spinner("Generating response..."):
            if ai_resp.get("reason"):
                st.caption(f"🤔 Thought: {ai_resp['reason']}")

        # Handle editing code automatically
        if ai_resp.get("editing_code"):
            st.info("⚙️ Running generated code...")

            retries = 5
            success = False
            error = None
            code_to_run = ai_resp["editing_code"]

            for attempt in range(1, retries + 1):
                try:
                    with st.spinner(f"Attempt-{attempt} to run code..."):
                        local_env = {"assets": st.session_state.assets}
                        if code_to_run:
                            st.session_state["last_code"] = code_to_run
                            with open("generated_edit.py", "w") as f:
                                f.write(code_to_run)

                            # Try executing generated code
                            subprocess.run([sys.executable, "generated_edit.py"], check=True)
                            if Path("output.mp4").exists():
                                out_file = f"output_{int(time.time())}.mp4"
                                os.rename("output.mp4", out_file)
                                st.session_state.last_output = out_file
                                st.success("✅ Edit applied successfully!")
                                st.video(out_file)
                            else:
                                st.success("✅ Code executed successfully (no video output).")

                    success = True
                    break

                except subprocess.CalledProcessError as e:
                    error = str(e)
                    st.warning(f"⚠️ Attempt {attempt} failed: {error}")
                    st.error(f"Error running generated code: {e}")
                    # Retry with AI code fix
                    with st.spinner(f"Regenerating response..."):
                        fix_prompt = (
                            f"The following code failed with error:\n{error}\n\n"
                            f"Here is the broken code:\n{code_to_run}\n\n"
                            "Please return corrected code in JSON schema format."
                        )
                        fix_resp = generate_response(
                            library_choice=st.session_state.library_choice,
                            user_message=fix_prompt,
                            video_desc=st.session_state.video_desc,
                            video_file_path=st.session_state.assets["main_video"],
                            assets=st.session_state.assets,
                            chat_history=st.session_state.chat_history,
                        )
                        code_to_run = fix_resp.get("editing_code")
                    
            if not success:
                st.error("❌ Error occurred during editing. Please clarify your request.")