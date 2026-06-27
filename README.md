# CutDost: From Ideas to Edits 🎬

![CutDost Banner](https://img.shields.io/badge/AI-Video%20Editing-blue?style=for-the-badge&logo=openai)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=for-the-badge&logo=streamlit)

CutDost is an AI-powered chatbot designed to make video editing as easy as chatting with a friend. By simply describing what you want—like "start video with fade-in effect" or "turn greyscale when a sad song is being played"—CutDost automatically handles the editing process. It eliminates the need for advanced technical knowledge, allowing users to focus on their creative vision rather than complex editing software.

## 🌟 Features

- **Natural Language Editing**: Describe your edits in plain English, and the AI will execute them.
- **Automated Video Understanding**: Uses Google's Gemini 2.5 Pro to analyze the video and generate a detailed description with accurate timestamps for scenes, dialogues, sound, and visuals.
- **Intelligent Code Generation**: Leverages OpenAI's GPT OSS 120B (via Groq) to understand the editing prompt and generate Python code using MoviePy or Movis.
- **Self-Correcting Execution**: Automatically extracts and runs the generated code. If an error occurs, the error is fed back to the model to fix it, retrying up to 5 times.
- **Interactive Web Interface**: Built with Streamlit for a simple, modern, and user-friendly experience, including file upload, video preview, and real-time chat.

## 🛠️ Tools & Technologies

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Building the simple and modern web interface. |
| **Backend** | Python | Processing logic and calling AI models via API. |
| **Video Analysis AI** | Google Gemini 2.5 Pro | Generating detailed video descriptions and timestamps. |
| **Code Generation AI** | OpenAI GPT OSS 120B (via Groq) | Chatting with the user and generating video editing code. |
| **Video Editing Libraries** | MoviePy / Movis | Performing actual video editing operations (trimming, zooming, filters, etc.). |
| **Video Processing** | OpenCV & FFmpeg | Reading frames, format conversions, and backend video reading/writing. |

## 🚀 How It Works

1. **Upload Video**: The user uploads an MP4 video through the web app.
2. **Video Understanding**: The Gemini model analyzes the video and generates a detailed description + transcript of scenes, dialogues, sound & visuals with accurate timestamps.
3. **AI Editing Process**: This description, along with the user's prompt, is sent to the GPT OSS 120B model, which understands the required edits and creates Python code.
4. **Automatic Editing**: The code is extracted and executed to apply edits on the uploaded video. If the code throws an error, it is fed back to the model for fixing (up to 5 retries).
5. **Final Output**: A preview of the edited video is displayed to the user, ready to download.

### Video Demo:
  [Video link](https://drive.google.com/file/d/1VzGm1x8RLZvMidu-VtmrdjYPBdoSlW8q/view?usp=drivesdk)


## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RudranshJaiswal01/CutDost-From_Ideas_to_Edits.git
   cd CutDost-From_Ideas_to_Edits
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

4. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📂 Project Structure

- `streamlit_app.py`: The main Streamlit application file handling the UI, chat interface, and code execution loop.
- `open_ai.py`: Handles communication with the Groq API (GPT OSS 120B) to generate structured JSON responses containing the editing code.
- `video_descriptor.py`: Handles communication with the Google Gemini API to generate detailed video descriptions.
- `requirements.txt`: Lists all the Python dependencies required to run the project.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have suggestions for improvements or new features.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---
*CutDost truly lives up to its name, a friendly AI companion that understands your creative vision and helps you make it real.*
