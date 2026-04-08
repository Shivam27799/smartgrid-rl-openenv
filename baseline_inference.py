import os
import numpy as np
from openai import OpenAI
from environment import SmartGridEnv, GridAction

API_KEY = os.getenv("OPENAI_API_KEY", "dummy_key")
client = OpenAI(api_key=API_KEY)

def run_reproducible_baseline():
    print(f"Executing OpenEnv Baseline... (Key: {API_KEY[:4]}***)")
    env = SmartGridEnv(difficulty="hard")
    obs = env.reset()
    total_reward = 0
    
    for i in range(24):
        # Baseline logic: Inefficient buyer
        action_val = (obs.load - obs.supply) * 0.7
        action = GridAction(energy_trade=action_val)
        
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        
    avg_score = total_reward / 24
    print(f"--- REPRODUCIBLE EVALUATION ---")
    print(f"Final Score (Hard): {avg_score:.2f}")

if __name__ == "__main__":
    run_reproducible_baseline()