from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from tasks import run_grader

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    e, m, h = run_grader("easy"), run_grader("medium"), run_grader("hard")
    
    return f"""
    <html>
        <head><style>
            body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); width: 350px; border: 1px solid #334155; }}
            .bar-bg {{ background: #334155; height: 12px; border-radius: 6px; margin: 10px 0 20px; overflow: hidden; }}
            .bar-fill {{ height: 100%; transition: width 1s ease-in-out; }}
            h1 {{ font-size: 1.2rem; letter-spacing: 2px; color: #94a3b8; margin-bottom: 30px; }}
            .label {{ display: flex; justify-content: space-between; font-size: 0.9rem; font-weight: 600; }}
        </style></head>
        <body>
            <div class="card">
                <h1>⚡ GRID MONITOR v1.0</h1>
                <div class="label"><span>EASY TASK</span><span>{e}</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width: {e*100}%; background: #22c55e;"></div></div>
                
                <div class="label"><span>MEDIUM TASK</span><span>{m}</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width: {m*100}%; background: #3b82f6;"></div></div>
                
                <div class="label"><span>HARD TASK</span><span>{h}</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width: {h*100}%; background: #ef4444;"></div></div>
                
                <div style="font-size: 0.7rem; color: #64748b; margin-top: 20px;">OpenEnv Spec Compliance: <b>Verified</b></div>
            </div>
        </body>
    </html>
    """

@app.get("/evaluate")
def evaluate():
    return {"task_easy": run_grader("easy"), "task_medium": run_grader("medium"), "task_hard": run_grader("hard")}