# 🌍 Finance Management System with AI Voice Assistant

Welcome to the **Finance Management System** – an intelligent voice-enabled assistant designed for financial query routing and analysis. This system combines voice interaction, AI-based decision routing, and Streamlit for a seamless user interface.

---

## 🧠 Features

- 🎙️ **Voice Interaction**: Speak to the assistant and receive voice-based responses.
- 🤖 **AI Routing System**: Uses similarity functions and external routing logic to understand and resolve user queries.
- 🧾 **Finance Functions**: Handles tasks related to financial management (extendable via `src/Functions/`).
- 🌐 **HTML Output Handling**: Capable of rendering HTML responses in chat.
- 🗃️ **Session Memory**: Maintains conversation history during session.
- 💬 **Text or Voice Input**: Input through either chatbox or microphone.

---

## 🛠️ Project Structure

```
.
├── Data
│   ├── Modelfile
│   ├── fields.txt
│   ├── finance.txt
│   ├── financial_DB.db
│   ├── prompts.py
│   ├── tools.py
│   └── vector_db
│       ├── 155734ec-ab09-4ec3-b888-637b4979dbe5
│       │   ├── data_level0.bin
│       │   ├── header.bin
│       │   ├── length.bin
│       │   └── link_lists.bin
│       ├── chroma.sqlite3
│       └── f3792827-91ae-49e1-bd63-0627fc19df38
├── app.py
├── main.py
├── requirements.txt
├── src
│   ├── Brain
│   │   ├── ask_gemini.py
│   │   ├── backup
│   │   │   ├── database.py
│   │   │   ├── new_router.py
│   │   │   ├── router.py
│   │   │   ├── sql_gen.py
│   │   │   └── sql_prc.py
│   │   ├── embd.py
│   │   ├── function_call.py
│   │   ├── query_res.py
│   │   ├── sim_router.py
│   │   └── sql_agent.py
│   ├── Conversations
│   │   ├── text_speech.py
│   │   └── voice_text.py
│   ├── DB_op
│   │   ├── load_db.py
│   │   ├── sql_exe.py
│   │   └── sql_filter.py
│   ├── Functions
│   │   ├── exe_function.py
│   │   ├── finance_news.py
│   │   ├── stock_analysis.py
│   │   └── ticker_symbol.py
│   ├── finance_api
│   │   ├── fin_data.py
│   │   ├── new_fin.py
│   │   └── yh_fn.py
│   └── load_vector
│       └── doc_data.py
├── static
│   └── logo.png
└── test.py

14 directories, 40 files
```

---

## 🧑‍💻 Getting Started

Follow these steps to set up and run the application on your local machine.

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/ganeshnikhil/Finance_AI.git
cd Finance_AI
```

### 2. 🐍 Create a Virtual Environment

```bash
# For Linux/macOS
python3 -m venv venv

# For Windows
python -m venv venv
```

### 3. ✅ Activate the Environment

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. 📥 Install Required Dependencies

```bash
pip install -r requirements.txt
```

Make sure `pysqlite3` and `streamlit` are installed properly (already handled in code dynamically).

---

## 🚀 Run the Application

```bash
streamlit run app.py
```

It will launch a local server (usually at `http://localhost:8501`) where you can interact with the assistant.

---

## 🔧 Configuration Notes

- **Speech-to-Text**: Uses a function from `src/Conversations/voice_text.py` to transcribe audio input.
- **Text-to-Speech**: Converts assistant responses to audio using `text_to_speech_local()`.
- **Routing Engine**: `function_call_gem_gemini_similarity()` decides what financial function to run based on user input.
- **Custom HTML Rendering**: Supports HTML-styled bot responses for better display.

---

## 🧩 Dependencies

Make sure `requirements.txt` includes (if not already):

```txt
streamlit
pysqlite3-binary
openai
speechrecognition
gTTS
pydub
```

Adjust based on your actual implementation in `text_speech.py` and `voice_text.py`.

---

## 💡 Use Case Ideas

- Finance report generation
- Budget tracking via voice
- Assistant-powered investment analysis
- Personal finance queries with voice feedback

---

## 📸 UI Preview

> Sidebar with voice toggle and logo  
> Centered app title: *Finance Management System*  
> Chat interface with voice or text input  
> Responses displayed as markdown or rich HTML

---

## ✨ Custom Styling

Custom CSS is injected via Streamlit to style buttons and checkboxes, improving UX aesthetics and responsiveness.

---

## 📬 Contact

For any queries, feel free to reach out or create an issue in the repository.

---

Would you like me to also generate a `requirements.txt` based on your code?
