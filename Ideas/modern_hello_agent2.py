import os
import re
import subprocess
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# --- TARGET REPOSITORY & DIRECTORY CONFIGURATION ---
REPO_ROOT = r"C:\Users\natha\Documents\GitHub\ngwells.github.io"
TARGET_BASE_DIR = os.path.join(REPO_ROOT, "Ideas")
SITE_FOLDER_NAME = "hello_world_site"
OUTPUT_DIR = os.path.join(TARGET_BASE_DIR, SITE_FOLDER_NAME)

# --- LANGGRAPH STATE DEFINITION ---

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_html: str
    reviewed_html: str
    user_prompt: str

# --- SKILL / TEMPLATE FUNCTIONS ---

def get_tailwind_head() -> str:
    """Provides boilerplate head element with Tailwind CSS CDN and Inter typography."""
    return r"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World - Modern Landing</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: { sans: ['Inter', 'sans-serif'] },
                    animation: { 'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite' }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="https://rsms.me/inter/inter.css">
</head>"""

# --- LANGGRAPH NODES ---

def llm_generate_node(state: AgentState) -> dict:
    """Builder Node: Generates modern HTML landing section using Ollama (qwen2.5-coder:7b)."""
    print("🤖 [Node 1: Builder] Requesting layout generation from Ollama (qwen2.5-coder:7b)...")
    
    llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.2)
    
    system_prompt = (
        "You are an expert static web developer. Return ONLY valid HTML (inside a <body> tag) "
        "using modern Tailwind CSS styling (dark mode, glassmorphism, subtle gradients, centered layout) "
        "and client-side JavaScript for interactive elements. "
        "Do NOT include standard <html> or <head> tags. Do NOT wrap output in markdown code fences like ```html."
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{request}")
    ])
    
    chain = prompt_template | llm
    response = chain.invoke({"request": state["user_prompt"]})
    
    return {"raw_html": response.content.strip()}


def llm_review_node(state: AgentState) -> dict:
    """Reviewer Node: Audits markup, strips markdown backticks, and enforces Tailwind quality."""
    print("🔍 [Node 2: Reviewer] Auditing generated code with Ollama...")
    
    llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.1)
    
    review_instruction = (
        "You are a Senior Front-End Code Reviewer. Inspect the provided raw HTML. "
        "Ensure it contains clean Tailwind CSS classes, centered layout, no broken tags, and no markdown formatting wrappers. "
        "Return ONLY the refined <body>...</body> HTML string."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", review_instruction),
        ("user", "Audit and refine this HTML output:\n\n{code}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"code": state["raw_html"]})
    
    # Clean markdown backticks if present
    clean_html = re.sub(r"^```html\s*|^```\s*|```$", "", response.content.strip(), flags=re.MULTILINE)
    return {"reviewed_html": clean_html}


def git_publish_node(state: AgentState) -> dict:
    """Publisher Node: Saves index.html and executes Git commands targeting repo root."""
    print("🚀 [Node 3: Publisher] Assembling site and running Git operations...")
    
    # 1. Ensure target directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Assemble complete document
    head_content = get_tailwind_head()
    full_html = f"<!DOCTYPE html>\n<html lang=\"en\">\n{head_content}\n{state['reviewed_html']}\n</html>"
    
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[✓] Saved file: {index_path}")

    # 3. Execute Git commands against parent repository root
    try:
        rel_output_dir = os.path.relpath(OUTPUT_DIR, REPO_ROOT)

        # Stage relative path in parent repo
        subprocess.run(["git", "add", rel_output_dir], cwd=REPO_ROOT, check=True)
        print(f"[✓] Staged relative path: {rel_output_dir}")

        # Commit changes
        commit_res = subprocess.run(
            ["git", "commit", "-m", f"Add LangGraph/Ollama generated site to {SITE_FOLDER_NAME}"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        
        if "nothing to commit" in commit_res.stdout:
            print("[!] Git Status: No new changes detected to commit.")
        else:
            print(f"[✓] Git Commit Output:\n{commit_res.stdout.strip()}")

        # Dynamically detect active branch (master vs main)
        branch_res = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        active_branch = branch_res.stdout.strip() or "master"

        # Push directly to GitHub
        print(f"📡 Pushing commit to GitHub (origin {active_branch})...")
        push_res = subprocess.run(
            ["git", "push", "origin", active_branch],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        
        stdout_msg = push_res.stdout.strip()
        stderr_msg = push_res.stderr.strip()
        print(f"[✓] Git Push Output:\n{stderr_msg if stderr_msg else stdout_msg if stdout_msg else f'Successfully pushed to {active_branch}.'}")

    except subprocess.CalledProcessError as e:
        print(f"\n[X] Git Command Failed: {' '.join(e.cmd)}")
        print(f"Error output:\n{e.stderr if e.stderr else str(e)}")
    except Exception as e:
        print(f"\n[X] File/Git operation failed: {str(e)}")

    return {}

# --- COMPOSE LANGGRAPH WORKFLOW ---

builder = StateGraph(AgentState)

# Add nodes
builder.add_node("builder_node", llm_generate_node)
builder.add_node("reviewer_node", llm_review_node)
builder.add_node("publisher_node", git_publish_node)

# Flow: START -> Builder -> Reviewer -> Publisher -> END
builder.add_edge(START, "builder_node")
builder.add_edge("builder_node", "reviewer_node")
builder.add_edge("reviewer_node", "publisher_node")
builder.add_edge("publisher_node", END)

graph_agent = builder.compile()

# --- EXECUTION ---

if __name__ == "__main__":
    generation_prompt = (
        "Create a sleek very dark-mode glassmorphism hero section for a modern Hello World landing page. Center the text. "
        "Include a status badge, interactive action button that toggles visibility on a text container, "
        "and clean responsive padding."
    )
    
    print(f"Starting LangGraph agent workflow for target path: {OUTPUT_DIR}...\n")
    
    initial_state = {
        "messages": [HumanMessage(content=generation_prompt)],
        "user_prompt": generation_prompt,
        "raw_html": "",
        "reviewed_html": ""
    }
    
    graph_agent.invoke(initial_state)
    print("\n[✓] All LangGraph agent steps completed successfully!")