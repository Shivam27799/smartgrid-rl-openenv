---
title: SmartGrid-RL-OpenEnv-v2
emoji: ⚡
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
tags:
  - openenv
  - rl-environment
  - resource-allocation
  - reinforcement-learning
---

# ⚡ SmartGrid-v1 (OpenEnv Spec 2.0) - Phase 2 Submission

SmartGrid-v1 is a production-oriented Reinforcement Learning environment for microgrid management. It follows the **full OpenEnv specification**, utilizing Pydantic for type-safe state/action transitions.

## 📖 Environment Description

The agent acts as a Grid Controller. Its objective is to balance volatile energy supply (Solar/Wind) against consumer load while avoiding costly energy purchases during market price spikes.

### Why this is a "Real-World" Task:

Energy load balancing is a critical utility task performed by ISOs (Independent System Operators). Agents must manage storage and grid-buy actions to maintain stability without excessive costs.

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

Where:

- $\beta$ = balance (load - supply)
- $P$ = market price
- $A$ = action magnitude
- $\omega$ = difficulty-based penalty weight

---

## 🚦 Phase 2: 3-Task Evaluation

| Task     | Difficulty | Noise | Price Penalty | Expected Score |
| -------- | ---------- | ----- | ------------- | -------------- |
| `easy`   | Low        | 0.05  | 0.1           | 0.30 - 0.50    |
| `medium` | Moderate   | 0.20  | 5.0           | 0.40 - 0.60    |
| `hard`   | High       | 0.45  | 25.0          | 0.50 - 0.70    |

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run All Tasks

```bash
python inference.py
```

### Expected Output Format

```
========== RUNNING TASK: EASY ==========
[START] task=easy
[STEP] step=1 reward=0.35
[STEP] step=2 reward=0.42
...
[STEP] step=24 reward=0.38
[END] task=easy score=0.4521 steps=24

========== RUNNING TASK: MEDIUM ==========
[START] task=medium
[STEP] step=1 reward=0.45
...
[END] task=medium score=0.5234 steps=24

========== RUNNING TASK: HARD ==========
[START] task=hard
[STEP] step=1 reward=0.30
...
[END] task=hard score=0.6145 steps=24

[SUMMARY] Completed 3/3 tasks
```

---

## 🤖 Agent Strategy

**Smart Rule-Based Agent** (No external API calls)

### Easy Task

- Simple load-supply balancing
- Minimal price consideration
- Formula: `action = clamp(load_diff * 0.5)`

### Medium Task

- Balance + price awareness
- Moderate aggressiveness
- Formula: `action = clamp(load_diff * 0.6 + price_impact * 0.4)`

### Hard Task

- Advanced multi-factor strategy
- Supply margin detection
- Adaptive aggressiveness based on grid state

---

## 📁 Project Structure

```
smartgrid-rl-openenv-main/
├── inference.py          # Phase 2 submission (3 tasks)
├── environment.py        # SmartGrid environment
├── setup.py             # Package configuration
├── requirements.txt     # Dependencies (numpy, pydantic, gymnasium)
├── README.md            # This file
└── Dockerfile           # Container configuration (optional)
```

---

## ✅ Phase 2 Compliance

- ✅ **3 Independent Tasks** (Easy, Medium, Hard)
- ✅ **Deterministic Output** (No randomness in agent)
- ✅ **Clean Format** ([START], [STEP], [END], [SUMMARY])
- ✅ **Zero External Dependencies** (No LLM APIs)
- ✅ **Robust Error Handling** (Graceful degradation)
- ✅ **Type-Safe** (Pydantic models throughout)

---

## 🔧 Technical Details

### Dependencies

- `numpy>=1.24.0` - Numerical computing
- `pydantic>=2.0.0` - Type validation
- `pyyaml>=6.0` - Configuration
- `gymnasium>=0.29.0` - RL environment framework

### Python Version

- Requires Python 3.9+

---

## 📊 Performance Metrics

Agent performance varies by difficulty:

- **Easy**: Stable performance (>0.40)
- **Medium**: Moderate variance (0.40-0.65)
- **Hard**: High variance due to noise (0.50-0.70)

---

## 📝 Notes

- All tasks run sequentially
- Each task is 24 steps
- Rewards are normalized by max_steps
- No warm-up or training phase required
- Agent strategy is fixed per difficulty

---

## 🎯 For Graders

Simply run:

```bash
python inference.py
```

Output will show:

1. Three sequential task executions
2. Standard [START]/[STEP]/[END] blocks
3. Final summary of completed tasks

No additional setup, credentials, or configuration needed.

---

Last Updated: April 2026
