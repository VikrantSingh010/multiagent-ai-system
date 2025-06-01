Perfect! Here's your updated, clean `README.md` in full **copy-paste** format for GitHub—including all your edits and formatting:

---

```markdown
# 🧠 Multi-Format Document Classification & Processing System

This project is a multi-agent AI system capable of classifying and processing input documents in various formats—**Email**, **JSON**, and **PDF**—and routing them to specialized agents based on **intent**. The system uses the **Groq API** for high-performance LLM completions and maintains context using an **SQLite-based shared memory**.

---

## 🗂️ Features

- ✅ **Automatic format detection** (PDF, JSON, Email)  
- ✅ **Intent classification** (Invoice, RFQ, Complaint, Regulation, Other)  
- ✅ **Specialized agents** for Email, JSON, and PDF  
- ✅ **Context-aware processing** via shared memory  
- ✅ **LLM-powered extraction** using Groq’s `llama3-70b-8192`  
- ✅ **Urgency detection** in Emails  
- ✅ **Schema-based extraction** with anomaly detection  

---

## 🧩 Folder Structure

```

.
├── agents/
│   ├── classifier_agent.py
│   ├── email_agent.py
│   ├── json_agent.py
│   └── pdf_agent.py
├── core/
│   ├── groq_client.py
│   └── shared_memory.py
├── orchestrator/
│   └── process_input.py
├── examples/
│   ├── samples.ext
├── main.py
├── app.py
├── .env
├── README.md
├── requirements.txt
└── agents.ipynb

````

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/VikrantSingh010/multiagent-ai-system.git
cd MULTIAGENTAI
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Key

Replace `"Your Groq API Key"` with your actual Groq API key inside the `.env` file.

---

## 🧪 Run the System

You can run sample inputs via `main.py`.

```bash
python main.py
```

* Modify the file to uncomment the type of input (JSON, PDF, Email) you want to test.
* Input sample files are provided inside `MULTIAGENTAI/examples/`.
* You can also run `agents.ipynb` for interactive testing.

---

## 🖥️ Sample Output

Sample outputs are provided in the `MULTIAGENTAI/Output` folder.

---

## 🧠 How It Works

1. **Input is received** (PDF, Email, or JSON)
2. **Classifier agent** determines:

   * The format (e.g., JSON, Email, PDF)
   * The intent (e.g., Complaint, Invoice)
3. Based on format:

   * **PDF agent** extracts text and routes to Email agent
   * **JSON agent** validates schema and flags anomalies
   * **Email agent** extracts urgency, sender, intent, and summary
4. **Shared memory** logs the result and maintains conversation context

---

## 🧠 Agents Overview

| Agent Name         | Purpose                                 |
| ------------------ | --------------------------------------- |
| `classifier_agent` | Detects document format and intent      |
| `email_agent`      | Parses and summarizes emails            |
| `json_agent`       | Extracts and validates JSON payloads    |
| `pdf_agent`        | Extracts text and routes PDF processing |

---

## 🗃️ Shared Memory

* Powered by **SQLite**
* Supports:

  * Context tracking
  * Last extraction memory
  * Conversation history

---

