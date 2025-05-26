# 🎓 Education Chatbot (Streamlit + Hugging Face)

A Streamlit-based educational chatbot powered by the `deepseek-ai/DeepSeek-R1` model. It provides intelligent, conversational answers to student queries using the Hugging Face Inference API.

## 🚀 Features

- Clean conversational UI with chat bubbles
- Real-time question answering
- Chat history memory during session
- Tag removal (cleans unwanted <think> tags from model output)
- Streamlit-based deployment with Hugging Face integration

## 📁 Project Structure

```
.
├── app.py              # Streamlit app logic
├── .env                # Contains Hugging Face API token
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## ⚙️ Setup Instructions

1. **Clone the repository**
```bash
git clone <repo-url>
cd Education_chatbot-main
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add Hugging Face API key**
Create a `.env` file in the root directory:
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

5. **Run the chatbot**
```bash
streamlit run app.py
```

## 🧠 Model Used

- `deepseek-ai/DeepSeek-R1` (via Hugging Face Inference API)

## 📦 Dependencies

- `streamlit`
- `huggingface_hub`
- `python-dotenv`
- `re`, `os`

## 📝 Notes

- All interaction history is maintained per session.
- `<think>` tags from model response are removed automatically.

## 📄 License

MIT License.
