---
title: SmartGrid-RL-v1
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
---

# ⚡ SmartGrid-v1 (OpenEnv Spec 2.0)

SmartGrid-v1 is a production-oriented Reinforcement Learning environment for microgrid management. It follows the **full OpenEnv specification**, utilizing Pydantic for type-safe state/action transitions and WebSocket-ready logic.

## 📖 Environment Description
The agent acts as a Grid Controller. Its objective is to balance volatile energy supply (Solar/Wind) against consumer load while avoiding costly energy purchases during market price spikes.

### Why this is a "Real-World" Task:
Energy load balancing is a critical utility task performed by ISOs (Independent System Operators). Human operators must manage storage and grid-buy actions to maintain 50/60Hz stability without bankrupting the utility provider.

---

## 🛠 Technical Specification

### Action Space (`GridAction`)
Typed Pydantic model:
- `energy_trade`: float [-1.0, 1.0]. (Positive = Buy, Negative = Sell).

### Observation Space (`GridObservation`)
Typed Pydantic model returned via `step()` and `state()`:
- `load`: Current demand (0.0-1.0)
- `supply`: Renewable generation (0.0-1.0)
- `price`: Market price (0.0-1.0)

### Reward Function (Partial Progress)
Calculated at every step:
$$Reward = e^{-5|\beta|} - (\omega \cdot P \cdot \max(0, A) \cdot 10)$$
*Where $\beta$ is balance, $P$ is price, $A$ is action, and $\omega$ is the difficulty-based penalty weight.*

---

## 🚦 Tasks & Baselines

| Task ID | Difficulty | Noise Level | Price Penalty | Baseline Score |
| :--- | :--- | :--- | :--- | :--- |
| `easy` | Low | 0.05 | 0.1 | **~0.95** |
| `medium` | Moderate | 0.20 | 5.0 | **~0.65** |
| `hard` | High | 0.45 | 25.0 | **~0.30** |

---

## 🚀 Setup and Usage

### Containerized Execution
This environment is fully containerized. To run locally:
```bash
docker build -t smartgrid-env .
docker run -p 7860:7860 smartgrid-env