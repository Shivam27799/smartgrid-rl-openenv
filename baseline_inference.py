import os
import numpy as np
from openai import OpenAI
from environment import SmartGridEnv, GridAction

API_BASE_URL = os.getenv("API_BASE_URL", "<your-active-model-base-url>")
MODEL_NAME = os.getenv("MODEL_NAME", "<your-active-model-name>")
HF_TOKEN = os.getenv("HF_TOKEN")

# Optional - if you use from_docker_image():
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_reproducible_baseline():
    print(f"Executing OpenEnv Baseline... (Key: {str(HF_TOKEN)[:4]}***)")
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