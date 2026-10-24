
# Local Enterprise Finance & HR Intelligence Hub

A secure, private, and loop-free Agentic AI dashboard engineered for corporate Finance and HR administrative teams. This system runs completely offline on local hardware, combining open-weights large language models with the **Model Context Protocol (MCP)** standard and **AgentSpan (Orkes Conductor)** for runtime tracking.

## 🧠 Why I Built This (The Architectural Problem)

When deploying lightweight, open-weight models (like `Mistral-Nemo 12B`) into autonomous multi-step agent frameworks, standard autonomous ReAct routing patterns routinely experience **tool-use hallucination**. Because small localized token compilers struggle to reliably emit precise commercial API termination signatures, the orchestration backend can trap the system in expensive, endless `DO_WHILE` processing loops.

To bridge this gap for high-value business roles where data privacy and deterministic mathematical precision are non-negotiable, **I engineered a "Python-First" deterministic routing strategy**. By utilizing explicit Python intent intercept layers, the core application handles data collection and computing tasks before passing structured context packages to the LLM. This guarantees zero execution loops, eliminates math hallucinations, and maintains a highly private infrastructure framework.

## 🏗️ Technical Architecture Blueprint

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

## 🚀 Core Systems Engineering Implemented

### 🛡️ 1. Input Validation & Domain-Specific Guardrails
* **Injection Interception:** Built custom security middleware inside the MCP pipeline to scan raw string parameters for jailbreak attempts (`"ignore previous rules"`, `"override system prompt"`), freezing processing before injection text can pollute the model's context window.
* **Topic Boundary Enforcements:** Enforces semantic scope parameters so the agent blocks non-corporate prompts (e.g., creative writing, coding help, or general queries) at the gate, reserving CPU/GPU computing resources for dedicated corporate workflows.

### 🗄️ 2. Semantic Document RAG (Retrieval-Augmented Generation)
* **Localized Data Ingestion:** Implemented a file parsing pipeline using `langchain-text-splitters` to chunk corporate policy files into 600-character semantic fragments.
* **Vector Vectorization & Storage:** Used `nomic-embed-text` embeddings locally via Ollama to index text blocks into a persistent `ChromaDB` directory for fast, mathematical similarity lookups during HR document searches.

### 📊 3. Deterministic Data Tooling
* **Hallucination Protection:** Intercepted financial calculation requests (e.g., checking averages, max/min margins, or summary totals) and passed them directly to a Python `pandas` engine, ensuring absolute arithmetic data accuracy for Finance Officers.

### 🔌 4. Model Context Protocol Standard
* **Decoupled Architecture:** Replaced legacy, monolithic tool-binding structures with an extensible **MCP Server** (`FastMCP`), exposing all RAG and arithmetic functions as clean, protocol-compliant JSON-RPC tools communicating securely over standard inputs and outputs (stdio).

### 📈 5. Enterprise Observability & Memory Tracking
* **Audit Footprints:** Linked execution pathways to **AgentSpan (Orkes Conductor)** to track exact token consumption, monitor inference performance metrics (`durationMs`), and store thread conversations via unified metadata layers.

## ⚙️ Local Installation & Setup

1. **Prerequisites:** Ensure [Ollama](https://ollama.com) is installed and active on your machine. Pull the open-weights assets:
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

3. **Launch the Engine Interface Dashboard:**
   ```bash
   streamlit run app.py
   ```
Use code with caution.

✅ What to Do Next

Now that your project documentation reads like it was designed by an experienced systems architect, stage your updated file and execute your final push commands:
bash
# Stage the clean documentation update
git add README.md

# Commit the changes
git commit -m "docs: rewrite README to outline core architectural design and safety guardrails"

# Push everything live to your public repository branch
git push -u origin main
Use code with caution.
