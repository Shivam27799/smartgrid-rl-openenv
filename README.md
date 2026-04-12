---
title: SmartGrid AI Manager
emoji: ⚡
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
tags:
  - openenv
  - rl-environment
  - llm-agent
  - resource-allocation
---

# ⚡ SmartGrid-v1 (OpenEnv Spec) - Phase 2 Submission

SmartGrid-v1 is a production-oriented Reinforcement Learning and LLM-Agent environment for microgrid management. It follows the **full OpenEnv specification**, utilizing Pydantic for type-safe state/action transitions and an asynchronous FastAPI backend.

## 📖 Environment Description

The AI agent acts as a Grid Controller. Its objective is to balance volatile energy supply (Solar/Wind) against consumer load while avoiding costly energy purchases during market price spikes.

### Why this is a "Real-World" Task:
Energy load balancing is a critical utility task performed by ISOs (Independent System Operators). Agents must evaluate real-time telemetry (Load, Supply, Price) and make precise trade calculations to maintain grid stability without triggering massive financial penalties.

---

## 🛠 Technical Specification

### Action Space (`GridAction`)
Typed Pydantic model:
- `energy_trade`: float [-1.0, 1.0] (Positive = Buy, Negative = Sell)

### Observation Space (`GridObservation`)
Typed Pydantic model returned via `step()` and `state()`:
- `load`: Current demand (0.0-1.0)
- `supply`: Renewable generation (0.0-1.0)
- `price`: Market price (0.0-1.0)

### Reward Function
Calculated at every step:
$$Reward = e^{-5|\beta|} - (\omega \cdot P \cdot \max(0, A) \cdot 10)$$
Where $\beta$ = balance (load - supply), $P$ = market price, $A$ = action magnitude, and $\omega$ = difficulty-based penalty weight.

---

## 🚦 Phase 2: 3-Task Evaluation

| Task     | Difficulty | Noise | Price Penalty | Expected Score |
| -------- | ---------- | ----- | ------------- | -------------- |
| `easy`   | Low        | 0.05  | 0.1           | 0.30 - 0.50    |
| `medium` | Moderate   | 0.20  | 5.0           | 0.40 - 0.60    |
| `hard`   | High       | 0.45  | 25.0          | 0.50 - 0.70    |

---

## 🤖 LLM Agent Architecture (Proxy Integrated)

Unlike static rule-based scripts, this submission features a dynamic LLM Agent designed to pass Hackathon Proxy Validation.

1. **Proxy Injection:** `inference.py` dynamically accepts `API_BASE_URL` and `API_KEY` from the Hackathon validator environment.
2. **Telemetry Prompting:** At every step, the agent parses the FastAPI `GridObservation` and feeds the exact numerical state to the LLM (e.g., `gpt-3.5-turbo`).
3. **Graceful Fallback:** Implements strict `try/except` typing validation to prevent container crashes if the LLM hallucinates non-float responses.

---

## 📁 Project Structure

```text
smartgrid-rl-openenv/
├── server/
│   └── app.py           # FastAPI server & OpenEnv API endpoints
├── inference.py         # LLM agent execution and evaluation script
├── tasks.py             # Grader logic with shielded **kwargs
├── environment.py       # Core grid simulation logic
├── openenv.yaml         # Strict OpenEnv task configuration
├── requirements.txt     # Dependencies (fastapi, pydantic, openai, etc.)
└── Dockerfile           # HF Container config (Port 7860, persistent Uvicorn)

# Terminal 1: Start the Grid Server
uvicorn server.app:app --host 0.0.0.0 --port 7860

# Terminal 2: Run the LLM Agent
export API_KEY="your_test_key"
python inference.py
