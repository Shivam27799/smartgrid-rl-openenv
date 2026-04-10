from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from environment import SmartGridEnv, GridAction, GridObservation
from tasks import run_grader
import uvicorn

app = FastAPI(title="SmartGrid-v1 OpenEnv")

# Global environment instance
# We initialize it with 'hard' by default
env = SmartGridEnv(difficulty="hard")

# --- MANDATORY OPENENV API ENDPOINTS ---

@app.get("/state", response_model=GridObservation)
def get_state():
    return env.state()

@app.post("/reset", response_model=GridObservation)
def reset_env(task_id: str = "hard"):
    """
    Requirement: reset() -> returns initial observation.
    Now supports task_id to switch difficulty during evaluation.
    """
    global env
    # Re-initialize the environment with the requested difficulty
    if task_id not in ["easy", "medium", "hard"]:
        task_id = "hard"
    
    env = SmartGridEnv(difficulty=task_id)
    return env.reset()

@app.post("/step")
def step_env(action: GridAction):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

# --- EVALUATION & DASHBOARD ---

@app.get("/evaluate")
def evaluate():
    """Returns scores for the 3 tasks for internal check."""
    return {
        "task_easy": run_grader("easy"),
        "task_medium": run_grader("medium"),
        "task_hard": run_grader("hard")
    }

@app.get("/", response_class=HTMLResponse)
def dashboard():
    # Pass dummy trajectory=None for local dashboard health check
    e = run_grader("easy")
    m = run_grader("medium")
    h = run_grader("hard")
    return f"""
    <html>
        <head>
            <title>SmartGrid Monitor</title>
            <style>
                body {{ font-family: sans-serif; background: #0f172a; color: white; text-align: center; padding: 50px; }}
                .card {{ background: #1e293b; padding: 30px; border-radius: 15px; display: inline-block; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.5); }}
                .bar-bg {{ background: #334155; height: 12px; width: 300px; border-radius: 6px; margin: 10px auto; overflow: hidden; }}
                .bar-fill {{ height: 100%; transition: width 1s; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>⚡ SmartGrid OpenEnv Monitor</h1>
                <p>Easy Score: <b>{e}</b></p><div class="bar-bg"><div class="bar-fill" style="width:{min(e*100, 100)}%; background:#22c55e;"></div></div>
                <p>Medium Score: <b>{m}</b></p><div class="bar-bg"><div class="bar-fill" style="width:{min(m*100, 100)}%; background:#3b82f6;"></div></div>
                <p>Hard Score: <b>{h}</b></p><div class="bar-bg"><div class="bar-fill" style="width:{min(h*100, 100)}%; background:#ef4444;"></div></div>
                <p style="margin-top:20px; font-size: 0.8rem; color: #64748b;">API Status: <b>Live</b> | Port: <b>7860</b></p>
            </div>
        </body>
    </html>
    """

def main():
    """Required Entry Point for OpenEnv Validator."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
