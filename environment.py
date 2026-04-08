import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any, Tuple

class GridObservation(BaseModel):
    load: float
    supply: float
    price: float

class GridAction(BaseModel):
    energy_trade: float 

class SmartGridEnv:
    def __init__(self, difficulty: str = "easy"):
        self.difficulty = difficulty
        self.max_steps = 24
        self._current_state = np.array([0.5, 0.5, 0.5])
        self.step_count = 0

    def state(self) -> GridObservation:
        return GridObservation(
            load=float(self._current_state[0]),
            supply=float(self._current_state[1]),
            price=float(self._current_state[2])
        )

    def reset(self) -> GridObservation:
        self.step_count = 0
        self._current_state = np.array([
            np.random.uniform(0.4, 0.6), 
            np.random.uniform(0.3, 0.7), 
            np.random.uniform(0.2, 0.4)
        ])
        return self.state()

    def step(self, action: GridAction) -> Tuple[GridObservation, float, bool, Dict[str, Any]]:
        action_val = np.clip(action.energy_trade, -1.0, 1.0)
        load, supply, price = self._current_state
        
        balance = (supply + action_val) - load
        stability_reward = np.exp(-5 * abs(balance))

        # Tighter difficulty scaling to prevent score overlap
        if self.difficulty == "hard":
            # Buying at price > 0.55 is extremely punishing
            penalty_weight = 80.0 if (price > 0.55 and action_val > 0) else 2.0
            noise = 0.6 
        elif self.difficulty == "medium":
            penalty_weight = 15.0 if (price > 0.75 and action_val > 0) else 1.0
            noise = 0.25
        else:
            penalty_weight = 0.1
            noise = 0.05

        cost = max(0, action_val) * price
        # Reward function with high signal for partial progress vs penalty
        reward = float(np.clip(stability_reward - (penalty_weight * cost * 25), 0.0, 1.0))

        # Update environment dynamics
        new_load = np.clip(load + np.random.uniform(-noise, noise), 0.1, 1.0)
        new_supply = np.clip(supply + np.random.uniform(-noise, noise), 0.0, 1.0)
        
        # In hard mode, price drift is more volatile
        price_drift = np.random.uniform(0.1, noise) if self.difficulty == "hard" else 0.05
        new_price = np.clip(0.4 * new_load + price_drift, 0.0, 1.0)
        
        self._current_state = np.array([new_load, new_supply, new_price])
        self.step_count += 1
        done = self.step_count >= self.max_steps
        
        return self.state(), reward, done, {"balance": balance}