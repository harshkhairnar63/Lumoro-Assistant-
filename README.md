# 🚀 Lumoro Assistant

Lumoro Assistant is an intelligent AI-powered chatbot built using **LangGraph**, **LangChain**, **Groq LLMs**, and **Streamlit**. The project combines conversational AI, persistent memory, tool calling, internet search, weather retrieval, and agentic workflows into a single modern assistant inspired by Apple's clean and minimal design philosophy.

## ✨ Features

### 💬 Conversational AI

* Natural language conversations powered by Groq-hosted LLMs.
* Multi-turn contextual interactions.
* Human-like responses with low-latency inference.

### 🧠 Persistent Memory

* Built using LangGraph checkpointing.
* SQLite-backed conversation storage.
* Chat history remains available across sessions.
* Multiple conversation threads supported.

### 🌐 Internet Search Tool

* Real-time web search using DuckDuckGo.
* Retrieves current information unavailable in LLM training data.
* Enables fact-based responses and research assistance.

### 🌦️ Weather Tool

* Real-time weather information using Open-Meteo APIs.
* Automatic geocoding from city names to coordinates.
* Current temperature and wind-speed retrieval.

### 🗂️ Multi-Thread Conversations

* Create unlimited chat sessions.
* Switch between historical conversations.
* Resume previous discussions instantly.

### 🎨 Premium User Interface

* Apple-inspired design system.
* Clean typography and minimal layout.
* Modern chat experience built with Streamlit.
* Responsive conversation interface.

### 🔄 Streaming Responses

* Token-by-token response generation.
* Improved user experience through real-time output streaming.

### 🛠️ Tool-Augmented Architecture

* Dynamic tool selection through LangGraph workflows.
* Supports external APIs and future MCP integrations.
* Easily extensible with additional tools.

---

## 🏗️ Architecture

User Query

↓

LangGraph Workflow

↓

Groq LLM

↓

Tool Router

↙ ↘

Weather Tool Search Tool

↓

Response Generator

↓

Streamlit UI

↓

SQLite Memory

---

## 🧰 Technology Stack

### AI & Agent Frameworks

* LangChain
* LangGraph
* Groq API

### Frontend

* Streamlit
* Custom CSS

### Database

* SQLite
* LangGraph Checkpointing

### Tools

* DuckDuckGo Search
* Open-Meteo Weather API

### Future Integrations

* MCP (Model Context Protocol)
* GitHub MCP Server
* Filesystem MCP Server
* PostgreSQL MCP Server
* Gmail MCP Server

---

## 📂 Project Structure

```bash
Lumoro-Assistant/
│
├── streaming_frontend.py
├── langgraph_database_backend.py
├── Lumoro.db
├── requirements.txt
├── .env
├── .gitignore
│
└── assets/
```

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Lumoro-Assistant.git

cd Lumoro-Assistant
```

### Create Virtual Environment

```bash
python -m venv myenv
```

### Activate Environment

Windows:

```bash
myenv\Scripts\activate
```

Linux/Mac:

```bash
source myenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_TRACING_V2=false
```

### Run Application

```bash
streamlit run streaming_frontend.py
```

---

## 📈 Future Roadmap

* Calculator Tool
* Stock Market Tool
* PDF Chat (RAG)
* Resume Analyzer Agent
* YouTube Transcript Summarizer
* GitHub Repository Analyzer
* MCP Integration
* Multi-Agent Architecture
* Voice Assistant Support

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Agentic AI Systems
* LangGraph Workflows
* Stateful AI Applications
* Tool Calling
* Persistent Memory
* LLM Integration
* Prompt Engineering
* API Integration
* Streamlit Development
* AI Application Architecture

---

## 👨‍💻 Author

**Harshwardhan Khairnar**

B.Tech Computer Engineering
MPSTME, NMIMS University

Focused on:

* Generative AI
* Agentic AI
* LangGraph
* LangChain
* Computer Vision
* Full Stack AI Applications

---

## ⭐ Why This Project?

Most chatbots simply generate text. Lumoro Assistant goes beyond that by combining:

* Memory
* Tools
* Real-time data
* Workflow orchestration
* Modern UI

to create a foundation for a production-ready AI assistant capable of evolving into a fully autonomous agentic system.
