import streamlit as tf
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Import working AgentSpan SDK handlers
from agentspan.agents import Agent, AgentRuntime, ConversationMemory, run

# =====================================================================
# 🛡️ LOCAL CLIENT-SIDE SECURITY GUARDRAIL INFRASTRUCTURE
# =====================================================================
def execute_security_guardrail_check(user_prompt: str) -> dict:
    """
    Implements core safety checks inspired by NeMo Guardrails & Llama Guard.
    Prevents Prompt Injection attacks and strictly enforces Corporate Domain parameters.
    """
    cleaned_input = user_prompt.lower().strip()
    
    # 1. Jailbreak / Injection Mitigation Pattern Check
    injection_signatures = [
        "ignore previous", "system prompt", "override rules", 
        "forget your instructions", "act as a", "you are no longer"
    ]
    if any(sig in cleaned_input for sig in injection_signatures):
        return {
            "safe": False, 
            "reason": "⚠️ SECURITY ALERT: Prompt Injection/System Override Attempt Blocked."
        }
    
    # 2. Topic Boundary Rail (Enforces Finance & HR Domains Only)
    allowed_domains = [
        "policy", "handbook", "leave", "vacation", "rule", "hr", "concept",
        "sum", "average", "mean", "ledger", "max", "min", "finance", "close", 
        "volume", "open", "revenue", "total", "salary", "time", "date"
    ]
    
    # Allow simple short greetings, but block off-topic long questions
    if len(cleaned_input.split()) > 2:
        if not any(domain in cleaned_input for domain in allowed_domains):
            return {
                "safe": False, 
                "reason": "⚠️ POLICY EXCLUSION: Query out of scope. This system is strictly restricted to corporate Finance and HR administrative tasks."
            }
            
    return {"safe": True, "reason": "Passed Safety Scan"}


# 1. Page Configuration and Layout Aesthetics
tf.set_page_config(page_title="Finance & HR Intelligence Hub", layout="wide")
tf.title("💼 Enterprise Finance & HR Intelligence Engine")
tf.subheader("Powered by Local Mistral-Nemo (12B) & Model Context Protocol (MCP)")

# Initialize conversation history state
if "messages" not in tf.session_state:
    tf.session_state.messages = []

# Initialize AgentSpan runtime dashboard connection
runtime = AgentRuntime()
conversational_memory = ConversationMemory(max_messages=20)

# Build the structural definition for AgentSpan tracking metrics
agentspan_assistant = Agent(
    name='financial_hr_dashboard_agent',
    model='ollama/mistral-nemo:12b',
    instructions="You are an expert corporate office analyst. Summarize matching tool data context precisely.",
    memory=conversational_memory
)

# Define connection properties to launch local MCP server as a background subprocess
server_params = StdioServerParameters(
    command="python3",
    args=["mcp_server.py"]
)

async def communicate_with_agent(user_query: str):
    """
    Core Routing Session: Manages the asynchronous handshake between 
    the MCP Server tools and the local Ollama LLM via AgentSpan.
    """
    # CRITICAL SECURITY STEP: Run guardrails FIRST before establishing connection streams
    guard_result = execute_security_guardrail_check(user_query)
    if not guard_result["safe"]:
        tf.sidebar.error("⚠️ Guardrail Intercepted!")
        return guard_result["reason"]

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            tool_response = ""
            # Simple keyword router to map out task intent before processing
            if any(w in user_query.lower() for w in ["policy", "handbook", "leave", "vacation", "rule", "hr", "concept"]):
                tf.sidebar.info("🤖 Routing Task: [HR Policy Vector Search]")
                result = await session.call_tool("query_hr_policies", arguments={"query": user_query})
                if result and hasattr(result, 'content') and isinstance(result.content, list) and len(result.content) > 0:
                    tool_response = result.content[0].text
            elif any(w in user_query.lower() for w in ["sum", "average", "mean", "ledger", "max", "min", "finance", "close", "volume", "open", "revenue", "total", "salary"]):
                tf.sidebar.info("📊 Routing Task: [Deterministic Financial Ledger Analytics]")
                
                op = "sum" if any(w in user_query.lower() for w in ["sum", "total", "revenue"]) else "mean" if "mean" in user_query.lower() or "average" in user_query.lower() else "max" if "max" in user_query.lower() else "min"
                col = "Close" if any(w in user_query.lower() for w in ["close", "revenue", "total"]) else "Volume" if "volume" in user_query.lower() else "Open"
                
                result = await session.call_tool("analyze_financial_ledger", arguments={"column_name": col, "operation": op})
                if result and hasattr(result, 'content') and isinstance(result.content, list) and len(result.content) > 0:
                    tool_response = result.content[0].text

            # Stitch context payload if tool executed successfully
            if tool_response:
                with tf.expander("👁️ View Extracted Context Payload"):
                    tf.markdown(tool_response)
                final_prompt = f"{user_query}\n\n[CONTEXT INTEGRATION LAYER - SECURE DATA]:\n{tool_response}"
            else:
                final_prompt = user_query

            # Generate via AgentSpan so it logs live to your console dashboard
            with tf.spinner("Thinking... (Processing Local Mistral-Nemo Engine via AgentSpan)"):
                try:
                    execution_result = run(agentspan_assistant, final_prompt, runtime=runtime)
                    
                    if hasattr(execution_result, 'output') and isinstance(execution_result.output, dict):
                        if execution_result.output.get('result'):
                            return execution_result.output['result']
                    
                    if hasattr(execution_result, 'messages') and isinstance(execution_result.messages, list) and len(execution_result.messages) > 0:
                        last_msg = execution_result.messages[-1]
                        if isinstance(last_msg, dict) and last_msg.get('message'):
                            return last_msg['message']
                    
                    return str(execution_result)
                except Exception as e:
                    return f"Failed to execute local model runtime handshake: {str(e)}"

# Render active chat history cards cleanly
for msg in tf.session_state.messages:
    with tf.chat_message(msg["role"]):
        tf.markdown(msg["content"])

# User Chat Input Field
if user_input := tf.chat_input("Ask a question about HR policies or financial analytics...", key="mcp_chat_input"):
    tf.session_state.messages.append({"role": "user", "content": user_input})
    with tf.chat_message("user"):
        tf.markdown(user_input)
        
    # Launch asynchronous engine event processing step
    ai_response = asyncio.run(communicate_with_agent(user_input))
    
    tf.session_state.messages.append({"role": "assistant", "content": ai_response})
    with tf.chat_message("assistant"):
        tf.markdown(ai_response)
