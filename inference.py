import os
from openai import OpenAI
from environment import SmartGridEnv, GridAction

# Requirement: Read from environment variables
API_KEY = os.getenv("OPENAI_API_KEY", "dummy_key")
client = OpenAI(api_key=API_KEY)

def run_inference():
    """
    Standardized inference script for OpenEnv evaluation.
    This script demonstrates a reproducible baseline score.
    """
    # Difficulty set to hard for the baseline requirement
    env = SmartGridEnv(difficulty="hard")
    obs = env.reset()
    total_reward = 0
    
    # Run for a full 24-step trajectory
    for _ in range(24):
        # Baseline Logic: Deficit matching (Naive Agent)
        load, supply = obs.load, obs.supply
        action_val = (load - supply) * 0.7  # Inefficient response for Hard mode
        
        action = GridAction(energy_trade=action_val)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        
        if done:
            break
            
    final_score = total_reward / 24
    print(f"OpenEnv Evaluation Complete.")
    print(f"Final Baseline Score: {final_score:.2f}")

if __name__ == "__main__":
    run_inference()
