import os
import sys
import json
import pandas as pd
from mcp.server.fastmcp import FastMCP
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# 1. Initialize FastMCP
mcp = FastMCP("Finance_HR_Intelligence_Engine")

DB_DIR = os.path.join(os.path.dirname(__file__), "database")
POLICIES_FILE = os.path.join(os.path.dirname(__file__), "data", "policies", "employee_handbook.txt")
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "data", "ledger", "company_ledger.csv")

print("Initializing local Chroma Vector Database...", file=sys.stderr)
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

if os.path.exists(POLICIES_FILE):
    loader = TextLoader(POLICIES_FILE)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print("Vector database populated successfully.", file=sys.stderr)
else:
    print(f"Error: {POLICIES_FILE} not found. RAG functionality disabled.", file=sys.stderr)
    vector_db = None


# =====================================================================
# 🛡️ SECURITY ENTERPRISE GUARDRAIL INFRASTRUCTURE
# =====================================================================
def execute_security_guardrail_check(user_prompt: str) -> dict:
    """
    Implements core safety checks inspired by NeMo Guardrails & Llama Guard.
    Prevents Prompt Injection attacks and strictly enforces Corporate Domain parameters.
    """
    cleaned_input = user_prompt.lower().strip()
    
    # 1. Llama Guard-inspired Jailbreak/Injection Prevention
    injection_signatures = [
        "ignore previous", "system prompt", "override rules", 
        "forget your instructions", "act as a", "you are no longer"
    ]
    if any(sig in cleaned_input for sig in injection_signatures):
        return {
            "safe": False, 
            "reason": "SECURITY ALERT: Prompt Injection/System Override Attempt Blocked."
        }
    
    # 2. NeMo Guardrails-inspired Domain Restrictions (HR & Finance parameters only)
    allowed_domains = [
        "policy", "handbook", "leave", "vacation", "rule", "hr", "concept",
        "sum", "average", "mean", "ledger", "max", "min", "finance", "close", 
        "volume", "open", "revenue", "total", "time", "date", "salary"
    ]
    # Allow general short conversational starters like 'hello', but block off-topic tasks
    if len(cleaned_input.split()) > 2:
        if not any(domain in cleaned_input for domain in allowed_domains):
            return {
                "safe": False, 
                "reason": "POLICY EXCLUSION: Query out of scope. This system is strictly restricted to corporate Finance and HR administrative tasks."
            }
            
    return {"safe": True, "reason": "Passed Security Scan"}


# =====================================================================
# 🔌 PROTOCOL TOOL GATEWAYS WITH BUILT-IN GUARDRAILS
# =====================================================================
@mcp.tool()
def query_hr_policies(query: str) -> str:
    """Searches corporate HR manuals and company policies for specific answers."""
    # Run the safety intercept barrier check first
    guard_result = execute_security_guardrail_check(query)
    if not guard_result["safe"]:
        return guard_result["reason"]
        
    if not vector_db:
        return "HR Knowledge Base is offline. Document source not found."
    
    results = vector_db.similarity_search(query, k=3)
    context_package = "\n---\n".join([doc.page_content for doc in results])
    return f"Relevant HR Policy Excerpts found:\n\n{context_package}"


@mcp.tool()
def analyze_financial_ledger(column_name: str, operation: str) -> str:
    """Performs deterministic analytics on the company financial data ledger."""
    # Ensure tool arguments match schema safety filters
    if not os.path.exists(LEDGER_FILE):
        return "Financial ledger storage database file is unreachable."
    
    try:
        df = pd.read_csv(LEDGER_FILE)
        if column_name not in df.columns:
            available_cols = ", ".join(df.columns)
            return f"Error: Column '{column_name}' missing. Valid options are: {available_cols}"
        
        if operation == "mean":
            result = df[column_name].mean()
        elif operation == "sum":
            result = df[column_name].sum()
        elif operation == "max":
            result = df[column_name].max()
        elif operation == "min":
            result = df[column_name].min()
        else:
            return "Invalid calculation option selected."
            
        return f"Deterministic Financial Analysis Result: The {operation} of {column_name} is {result:,.2f}"
        
    except Exception as e:
        return f"Failed to execute target calculations: {str(e)}"


if __name__ == "__main__":
    mcp.run()
import os
import sys
import json
import pandas as pd
from mcp.server.fastmcp import FastMCP
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# FIXED: Updated import to use the modern, dedicated package
from langchain_ollama import OllamaEmbeddings

# 1. Initialize the FastMCP Framework
mcp = FastMCP("Finance_HR_Intelligence_Engine")

DB_DIR = os.path.join(os.path.dirname(__file__), "database")
POLICIES_FILE = os.path.join(os.path.dirname(__file__), "data", "policies", "employee_handbook.txt")
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "data", "ledger", "company_ledger.csv")

# 2. Setup Vector Database Infrastructure (On Server Initialization)
print("Initializing local Chroma Vector Database...", file=sys.stderr)
# FIXED: Using the modern OllamaEmbeddings class from langchain-ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

if os.path.exists(POLICIES_FILE):
    loader = TextLoader(POLICIES_FILE)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print("Vector database populated successfully.", file=sys.stderr)
else:
    print(f"Error: {POLICIES_FILE} not found. RAG functionality disabled.", file=sys.stderr)
    vector_db = None


# 3. Define the HR RAG Search Tool under the MCP Standard
@mcp.tool()
def query_hr_policies(query: str) -> str:
    """
    Searches corporate HR manuals and company policies for specific answers.
    Use this tool when users ask about rules, guidelines, conditions, or organizational processes.
    """
    if not vector_db:
        return "HR Knowledge Base is offline. Document source not found."
    
    results = vector_db.similarity_search(query, k=3)
    context_package = "\n---\n".join([doc.page_content for doc in results])
    return f"Relevant HR Policy Excerpts found:\n\n{context_package}"


# 4. Define the Financial Ledger Calculation Tool under the MCP Standard
@mcp.tool()
def analyze_financial_ledger(column_name: str, operation: str) -> str:
    """
    Performs deterministic database analytics on the company financial data ledger.
    Options for operation: 'mean', 'sum', 'max', 'min'.
    Common column names include: 'Open', 'High', 'Low', 'Close', 'Volume'.
    """
    if not os.path.exists(LEDGER_FILE):
        return "Financial ledger storage database file is unreachable."
    
    try:
        df = pd.read_csv(LEDGER_FILE)
        
        if column_name not in df.columns:
            available_cols = ", ".join(df.columns)
            return f"Error: Column '{column_name}' missing. Valid options are: {available_cols}"
        
        if operation == "mean":
            result = df[column_name].mean()
        elif operation == "sum":
            result = df[column_name].sum()
        elif operation == "max":
            result = df[column_name].max()
        elif operation == "min":
            result = df[column_name].min()
        else:
            return "Invalid calculation option selected."
            
        return f"Deterministic Financial Analysis Result: The {operation} of {column_name} is {result:,.2f}"
        
    except Exception as e:
        return f"Failed to execute target calculations: {str(e)}"


if __name__ == "__main__":
    mcp.run()

