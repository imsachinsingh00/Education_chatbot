# Education Chatbot

An educational chatbot web application built with [Flask](https://flask.palletsprojects.com/) and [LangChain](https://github.com/hwchase17/langchain), powered by the **Mistral-7B-Instruct** model on Hugging Face. It provides concise, on-topic answers to students’ questions and even remembers your name!

---

## 🔍 Features

- **Conversational UI**  
  A simple chat interface where students can type questions and get instant answers.
- **Concise Educational Assistance**  
  Uses a custom prompt to keep responses focused and to-the-point.
- **Name Memory**  
  Remembers “My name is X” across sessions by storing it in a local JSON file.
- **Customizable**  
  Easily tweak the prompt template, model parameters, or bring your own HF model.
- **CORS Enabled**  
  Frontend can be served anywhere (e.g. a static host) and still talk to the Flask API.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+**  
- **Hugging Face API Token** – Sign up at [huggingface.co](https://huggingface.co/) and create an access token.

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/imsachinsingh00/Education_chatbot.git
   cd Education_chatbot
