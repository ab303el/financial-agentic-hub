
markdown
# 💼 Enterprise Finance & HR Intelligence Engine

A secure, private, and loop-free Agentic AI dashboard tailored for corporate Finance and HR administrative teams. Built entirely on open-weights models running locally using the **Model Context Protocol (MCP)** and **AgentSpan (Orkes Conductor)**.

## 🏗️ Architecture Blueprint

```text
┌────────────────────────────────────────────────────────┐
│               Streamlit UI / MCP Client                │
└───────────────────────────┬────────────────────────────┘
                            │ (JSON-RPC over Stdio)
                            ▼
┌────────────────────────────────────────────────────────┐
│                      MCP Server                        │
│  ├─ Tool: query_hr_policies (Vector DB Chroma RAG)     │
│  └─ Tool: analyze_financial_ledger (Python Math)       │
└────────────────────────────────────────────────────────┘
                            │
                            ▼
             ┌─────────────────────────────┐
             │ AgentSpan Runtime Engine    │
             │ (Mistral-Nemo 12B / Local)  │
             └─────────────────────────────┘
```

## 🚀 Key Architectural Choices

* **Loop-Free Deterministic Tool Routing:** Bypasses local LLM parser vulnerabilities by managing complex orchestration workflows directly within Python intercept layers, completely eliminating infinite tool-calling loops.
* **Vector Semantic RAG Engine:** Implements localized data ingestion by utilizing `nomic-embed-text` to index corporate text documentation chunks directly into a persistent `ChromaDB` directory.
* **Structured Data Safeguards:** Replaces unpredictable language model arithmetic operations with a pandas data-analysis execution module to enforce absolute statistical accuracy.

## 🛠️ Local Installation & Setup

1. **Prerequisites:** Ensure you have [Ollama](https://ollama.com) installed and the required models pulled locally:
   ```bash
   ollama pull mistral-nemo:12b
   ollama pull nomic-embed-text
   ```

2. **Initialize Workspace Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Launch the Core Ecosystem Application:**
   ```bash
   streamlit run app.py
   ```
Use code with caution.

📦 Step 6: Generate Your Requirements Manifest

To make your repository copy-paste and install friendly for recruiters, freeze your virtual environment package dependencies directly into your config:
bash
pip freeze > requirements.txt

