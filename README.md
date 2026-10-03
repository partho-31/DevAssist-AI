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

The request is then routed to the appropriate LangChain workflow.

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
Pydantic Output Parser
  │
  ▼
Structured Response
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
├── schemas.py
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

Contains the Pydantic models used to define structured AI responses.

**`prompts.py`**

Contains specialized prompt templates for each development mode.

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
CodeReview Pydantic Parser
   ↓
Structured Review
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