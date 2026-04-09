import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from environment import SmartGridEnv, GridAction, GridObservation
from tasks import run_grader
import uvicorn  # <-- NEW: Required for the main() function

app = FastAPI(title="SmartGrid-v1 OpenEnv")

# Global environment instance to persist state between API calls
env = SmartGridEnv()

# --- MANDATORY OPENENV API ENDPOINTS ---
@app.get("/state", response_model=GridObservation)
def get_state():
    """Requirement: state() -> returns current state."""
    return env.state()

@app.post("/reset", response_model=GridObservation)
def reset_env():
    """Requirement: reset() -> returns initial observation."""
    return env.reset()

@app.post("/step")
def step_env(action: GridAction):
    """Requirement: step(action) -> returns obs, reward, done, info."""
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
    """Returns programmatic scores for all 3 tasks."""
    return {
        "task_easy": run_grader("easy"),
        "task_medium": run_grader("medium"),
        "task_hard": run_grader("hard")
    }

@app.get("/", response_class=HTMLResponse)
def dashboard():
    """The Visual Monitor for Human Reviewers."""
    e, m, h = run_grader("easy"), run_grader("medium"), run_grader("hard")
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: sans-serif; background: #0f172a; color: white; text-align: center; padding: 50px; }}
                .card {{ background: #1e293b; padding: 30px; border-radius: 15px; display: inline-block; }}
                .bar-bg {{ background: #334155; height: 12px; width: 300px; border-radius: 6px; margin: 10px auto; overflow: hidden; }}
                .bar-fill {{ height: 100%; transition: width 1s; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>⚡ SmartGrid OpenEnv Monitor</h1>
                <p>Easy: {e}</p><div class="bar-bg"><div class="bar-fill" style="width:{e*100}%; background:#22c55e;"></div></div>
                <p>Medium: {m}</p><div class="bar-bg"><div class="bar-fill" style="width:{m*100}%; background:#3b82f6;"></div></div>
                <p>Hard: {h}</p><div class="bar-bg"><div class="bar-fill" style="width:{h*100}%; background:#ef4444;"></div></div>
                <p style="margin-top:20px; font-size: 0.8rem; color: #64748b;">API Status: <b>Ready</b> | Spec: <b>OpenEnv 2.0</b></p>
            </div>
        </body>
    </html>
    """

# --- NEW: REQUIRED ENTRY POINT ---
def main():
    """This is the main function the OpenEnv validator is looking for."""
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
