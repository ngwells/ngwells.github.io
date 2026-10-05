import os
import re
import subprocess
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# --- TARGET DIRECTORY & REPOSITORY CONFIGURATION ---
REPO_ROOT = r"C:\Users\natha\Documents\GitHub\ngwells.github.io"
TARGET_BASE_DIR = os.path.join(REPO_ROOT, "Ideas")
SITE_FOLDER_NAME = "hello_world_site"
OUTPUT_DIR = os.path.join(TARGET_BASE_DIR, SITE_FOLDER_NAME)

# --- OLLAMA DYNAMIC GENERATION ---

def generate_hero_with_ollama(user_prompt: str) -> str:
    """Invokes local Ollama (qwen2.5-coder:7b) to dynamically generate modern HTML body content."""
    print("🤖 Requesting layout generation from local Ollama (qwen2.5-coder:7b)...")
    
    llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.2)
    
    system_instruction = (
        "You are an expert static web developer. Return ONLY valid HTML (inside a <body> tag) "
        "using modern Tailwind CSS styling (dark mode, glassmorphism, subtle gradients) "
        "and client-side JavaScript for interactive elements. "
        "Do NOT include standard <html> or <head> tags. Do NOT wrap output in markdown code fences like ```html."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        ("user", "{request}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"request": user_prompt})
    
    # Strip markdown backticks if model includes them
    clean_body = re.sub(r"^```html\s*|^```\s*|```$", "", response.content.strip(), flags=re.MULTILINE)
    return clean_body

# --- SKILLS / TEMPLATES ---

def get_tailwind_head() -> str:
    """Provides head boilerplate with Tailwind CSS and Inter typography dependencies."""
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

def write_commit_and_push_files(html_body: str, output_dir: str, repo_root: str):
    """Saves files locally and runs git commands targeting the main repository root."""
    # 1. Ensure target directory structure exists
    os.makedirs(output_dir, exist_ok=True)

    # 2. Combine head and generated body into complete HTML document
    head_content = get_tailwind_head()
    full_html = f"<!DOCTYPE html>\n<html lang=\"en\">\n{head_content}\n{html_body}\n</html>"
    
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[✓] Saved file: {index_path}")

    # 3. Execute Git commands against parent repository root
    try:
        rel_output_dir = os.path.relpath(output_dir, repo_root)

        # Stage directory in parent repo
        subprocess.run(["git", "add", rel_output_dir], cwd=repo_root, check=True)
        print(f"[✓] Staged relative path: {rel_output_dir}")

        # Commit changes
        commit_res = subprocess.run(
            ["git", "commit", "-m", f"Add Ollama-generated modern site to {SITE_FOLDER_NAME}"],
            cwd=repo_root,
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
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        active_branch = branch_res.stdout.strip() or "master"

        # Push directly to GitHub using active branch
        print(f"🚀 Pushing commit to GitHub (origin {active_branch})...")
        push_res = subprocess.run(
            ["git", "push", "origin", active_branch],
            cwd=repo_root,
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

# --- EXECUTION ENTRYPOINT ---

if __name__ == "__main__":
    print(f"Starting agent workflow for target path: {OUTPUT_DIR}...\n")
    
    # 1. Generate HTML body dynamically using Ollama
    generation_prompt = (
        "Create a sleek very dark-mode glassmorphism hero section for a modern Hello World landing page. center the text. "
        "Include a status badge, interactive action button that toggles visibility on a text container, "
        "and clean responsive padding."
    )
    body_code = generate_hero_with_ollama(generation_prompt)
    
    # 2. Write, commit, and push to GitHub
    write_commit_and_push_files(body_code, OUTPUT_DIR, REPO_ROOT)
    
    print("\n[✓] All steps completed successfully!")