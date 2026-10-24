# 🤖 DevAssist AI

DevAssist AI is a personal **AI-assisted software development chatbot** built with **LangChain** and **Streamlit**.

It helps developers review code, debug errors, generate code from requirements, understand existing code, and optimize implementations through specialized AI workflows.

The application uses **LangChain RunnableBranch** to route each request to the correct workflow based on the mode selected by the user.

---

## ✨ Features

DevAssist AI currently supports the following modes:

### 🔍 Code Review
Analyzes submitted code for:

- Bugs
- Security issues
- Performance issues
- Code quality problems
- Possible improvements
- Corrected code when necessary

### 🐞 Bug Fix
Helps developers:

- Identify the root cause of an error
- Understand why the problem occurs
- Generate corrected code
- Review the changes made

### 💻 Code Generation
Allows users to describe a feature, application idea, or development requirement and receive generated code based on their vision.

### 📖 Code Explanation
Explains existing code in a developer-friendly way, including:

- Purpose
- Important components
- Execution flow
- Programming concepts
- Complex logic

### ⚡ Code Optimization
Analyzes code and suggests improvements related to:

- Performance
- Readability
- Maintainability
- Memory/resource usage
- Code structure

---

## 🧠 How It Works

The user selects a development mode and provides either:

- Source code
- An error description
- A development requirement
- A project idea or vision

The latest request and previous conversation messages are routed to the selected
LangChain workflow. Each mode replies in natural Markdown and supports follow-up
questions about earlier code and answers. Modes guide the assistant's expertise
without requiring a fixed report format.

Enable **Structured report for the next message** to use the selected mode's
custom Pydantic parser and schema. Reports are displayed as readable sections
and code blocks. After a successful report, the toggle turns off automatically
so you can discuss the result in normal chat. Both paths receive the conversation
history.

Changing modes keeps the conversation context. Use **New conversation** in the
sidebar to clear the history and start again. History lasts for the current
Streamlit session and is sent to the model on each turn; long chats can reach the
model's context limit.

```text
User
  │
  ▼
Streamlit UI
  │
  ├── Select Mode
  │
  └── Enter Code / Requirement
  │
  ▼
RunnableBranch
  │
  ├── Code Review Chain
  ├── Bug Fix Chain
  ├── Code Generation Chain
  ├── Code Explanation Chain
  └── Code Optimization Chain
  │
  ▼
LLM
  │
  ▼
StrOutputParser (chat) / Custom Pydantic Parser (report)
  │
  ▼
Markdown Response / Formatted Report
  │
  ▼
Streamlit Chat Interface
```

---

## 🛠️ Technologies Used

- **Python**
- **LangChain**
- **Streamlit**
- **Pydantic**
- **Groq API**
- **ChatGroq**
- **RunnableBranch**
- **StrOutputParser**
- **PydanticOutputParser**
- **python-dotenv**

---

## 📂 Project Structure

```text
DevAssist-AI/
│
├── app.py
├── branch.py
├── chains.py
├── models.py
├── prompts.py
├── parsers.py
├── schemas.py
├── responses.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### File Responsibilities

**`app.py`**

Contains the Streamlit user interface, chat history, mode selector, user input, and response rendering.

**`models.py`**

Configures and initializes the LLM used by the application.

**`schemas.py`**

Defines the Pydantic response models used by the structured report workflows.

**`parsers.py`**

Defines the custom output parsers that validate each mode's structured report.

**`responses.py`**

Formats parsed reports as Markdown sections and code blocks for display and chat history.

**`prompts.py`**

Contains specialized chat prompts for each development mode, including conversation history.

**`chains.py`**

Connects prompts, the LLM, and output parsers to create individual LangChain workflows.

**`branch.py`**

Uses `RunnableBranch` to route requests to the appropriate chain based on the selected mode.

---

## 🔄 Request Flow

For example, when a user selects **Code Review**:

```text
User Code
   ↓
Code Review Mode
   ↓
RunnableBranch
   ↓
Code Review Chain
   ↓
Code Review Prompt
   ↓
LLM
   ↓
StrOutputParser / CodeReview Pydantic Parser
   ↓
Conversational Reply / Formatted Review Report
```

A similar workflow is used for the other modes.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone ""
cd DevAssist-AI
```

### 2. Create a Virtual Environment

```bash
python3 -m venv chatBot_env
```

Activate it:

#### Linux / macOS

```bash
source chatBot_env/bin/activate
```

#### Windows

```bash
chatBot_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Make sure `.env` is included in `.gitignore`.

```gitignore
.env
chatBot_env/
__pycache__/
```

Never push API keys or secrets to GitHub.

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can access DevAssist AI.

---


## 🗂️ Structured Output

Pydantic models are used to keep AI responses predictable and structured.

Example:

```python
class CodeReview(BaseModel):

    summary: str

    bugs: Optional[list[str]]

    security_issues: Optional[list[str]]

    performance_issues: Optional[list[str]]

    improvements: list[str]

    corrected_code: Optional[str]
```

This makes it easier for the Streamlit UI to display different sections of the response independently.

---
---

## ⚠️ Disclaimer

DevAssist AI generates AI-assisted programming suggestions. Generated code and recommendations should be reviewed and tested before being used in production environments.

---

## 👨‍💻 Author

**Partho Kumar Mondal**

Full-Stack Web Developer | Python | FastAPI | Django | React | Next.js | LangChain

---

## 📄 License

This project is currently intended for learning, experimentation, and personal development.

## Local checks

Install development dependencies, then run the offline routing and conversation
regression tests with pytest (no API calls):

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```
