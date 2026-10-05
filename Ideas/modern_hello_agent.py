import os
import re
import subprocess
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# --- TARGET DIRECTORY & PATH CONFIGURATION ---
TARGET_BASE_DIR = r"C:\Users\natha\Documents\GitHub\ngwells.github.io\Ideas"
SITE_FOLDER_NAME = "hello_world_site"
OUTPUT_DIR = os.path.join(TARGET_BASE_DIR, SITE_FOLDER_NAME)

# --- SKILLS / TOOLS ---

@tool
def inject_tailwind_design_system() -> str:
    """Provides standard HTML head setup including Tailwind CSS CDN, Google Fonts, and custom theme configs."""
    return r"""
<head>
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
</head>
"""

@tool
def build_modern_hello_hero() -> str:
    """Returns HTML/Tailwind structure for a modern dark-mode glassmorphism hero section with interactive JS."""
    return r"""
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col justify-between antialiased selection:bg-indigo-500 selection:text-white">
    <!-- Ambient background radial glow -->
    <div class="fixed inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.25),rgba(255,255,255,0))] pointer-events-none"></div>

    <main class="flex-grow flex items-center justify-center p-6 relative z-10">
        <div class="max-w-2xl w-full text-center space-y-8 bg-slate-900/50 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-10 shadow-2xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-medium">
                <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
                Static GitHub Pages Ready
            </div>
            
            <h1 class="text-5xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Hello, World.
            </h1>

            <p class="text-slate-400 text-lg leading-relaxed max-w-lg mx-auto">
                A minimal, modern static landing template generated dynamically via a local Ollama agent with skill tools.
            </p>

            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
                <button onclick="toggleStatus()" class="w-full sm:w-auto px-6 py-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition duration-200 shadow-lg shadow-indigo-600/20 active:scale-95">
                    Test Interactivity
                </button>
                <a href="https://github.com" target="_blank" class="w-full sm:w-auto px-6 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-medium transition duration-200">
                    GitHub Docs
                </a>
            </div>

            <div id="status-box" class="hidden text-sm text-indigo-300 bg-indigo-950/40 border border-indigo-800/50 rounded-lg p-3">
                ✨ Client-side JavaScript running statically without a backend server!
            </div>
        </div>
    </main>

    <footer class="py-6 text-center text-slate-500 text-sm relative z-10">
        Generated with Ollama Agent • Ready for Deployment
    </footer>

    <script>
        function toggleStatus() {
            const box = document.getElementById('status-box');
            box.classList.toggle('hidden');
        }
    </script>
</body>
"""

@tool
def write_file_and_commit(html_content: str, folder_path: str = OUTPUT_DIR) -> str:
    """
    Creates necessary target directories, writes index.html and a GitHub Actions workflow,
    then initializes Git (if needed) and commits the code.
    """
    # 1. Ensure target directory structure exists
    os.makedirs(os.path.join(folder_path, ".github", "workflows"), exist_ok=True)

    # 2. Clean LLM markdown artifacts and save index.html
    clean_html = re.sub(r"^```html\s*|^```\s*|```$", "", html_content.strip(), flags=re.MULTILINE)
    index_path = os.path.join(folder_path, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html lang=\"en\">\n{clean_html}\n</html>")

    # 3. Add standard GitHub Pages workflow file
    workflow_yaml = """name: Deploy Static Site to Pages

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    workflow_path = os.path.join(folder_path, ".github", "workflows", "static.yml")
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(workflow_yaml)

    # 4. Execute Git commands inside the target output directory
    try:
        git_dir = os.path.abspath(folder_path)
        
        # Check if git repository exists, initialize if not
        if not os.path.exists(os.path.join(git_dir, ".git")):
            subprocess.run(["git", "init"], cwd=git_dir, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=git_dir, check=True)

        # Stage files and commit
        subprocess.run(["git", "add", "."], cwd=git_dir, check=True)
        commit_res = subprocess.run(
            ["git", "commit", "-m", "Initial commit: Add modern Hello World site"],
            cwd=git_dir,
            capture_output=True,
            text=True
        )
        
        return f"Files written and Git commit created in '{folder_path}'. Git Output: {commit_res.stdout.strip()}"
    except Exception as e:
        return f"Files written to '{folder_path}', but Git operation failed: {str(e)}"

# --- LANGGRAPH AGENT SETUP ---

tools = [inject_tailwind_design_system, build_modern_hello_hero, write_file_and_commit]
tools_by_name = {t.name: t for t in tools}

# System prompt directly bound to LLM context
SYSTEM_INSTRUCTION = f"""You are an AI Web Development Agent that builds static websites using modular tool skills.
Your target output folder is: {OUTPUT_DIR}

To complete requests:
1. Call `inject_tailwind_design_system` to fetch design dependencies.
2. Call `build_modern_hello_hero` to fetch structural HTML components.
3. Combine both outputs into complete HTML structure.
4. Call `write_file_and_commit` to output the files into `{OUTPUT_DIR}` and create a Git commit.
"""

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.1).bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def call_model(state: AgentState):
    # Prepend system instruction to the active message list for context awareness
    messages = [SystemMessage(content=SYSTEM_INSTRUCTION)] + list(state["messages"])
    response = llm.invoke(messages)
    return {"messages": [response]}

def execute_tools(state: AgentState):
    last_message = state["messages"][-1]
    tool_responses = []
    
    for tool_call in last_message.tool_calls:
        tool_fn = tools_by_name[tool_call["name"]]
        observation = tool_fn.invoke(tool_call["args"])
        tool_responses.append(
            ToolMessage(content=str(observation), name=tool_call["name"], tool_call_id=tool_call["id"])
        )
    return {"messages": tool_responses}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    return "tools" if getattr(last_message, "tool_calls", None) else END

# Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", execute_tools)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, ["tools", END])
builder.add_edge("tools", "agent")

agent = builder.compile()

# --- EXECUTION ---

if __name__ == "__main__":
    prompt = HumanMessage(content=f"Create a modern dark-mode Hello World page, place it in '{OUTPUT_DIR}', and commit it.")
    
    print(f"Starting agent loop (Target Path: {OUTPUT_DIR})...")
    result = agent.invoke({"messages": [prompt]})
    
    print("\n--- AGENT EXECUTION SUMMARY ---")
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage):
            print(f"[{msg.name}]: {msg.content}")