import os
from openai import OpenAI
from environment import SmartGridEnv, GridAction

# Requirement: Read from environment variables
API_KEY = os.getenv("OPENAI_API_KEY", "dummy_key")
client = OpenAI(api_key=API_KEY)

def run_inference():
    """
    Standardized inference script for OpenEnv evaluation.
    Updated to include strict structured output logging [START], [STEP], [END].
    """
    task_name = "hard"
    env = SmartGridEnv(difficulty=task_name)
    obs = env.reset()
    total_reward = 0
    max_steps = 24
    
    # 1. MUST print the START block exactly as formatted
    print(f"[START] task={task_name}", flush=True)
    
    # Run for a full 24-step trajectory
    for step in range(1, max_steps + 1):
        # Baseline Logic: Deficit matching (Naive Agent)
        load, supply = obs.load, obs.supply
        action_val = (load - supply) * 0.7  # Inefficient response for Hard mode
        
        action = GridAction(energy_trade=action_val)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        
        # 2. MUST print the STEP block for every single loop iteration
        print(f"[STEP] step={step} reward={reward:.4f}", flush=True)
        
        if done:
            break
            
    final_score = total_reward / max_steps
    
    # 3. MUST print the END block with the final computed metrics
    print(f"[END] task={task_name} score={final_score:.4f} steps={max_steps}", flush=True)

if __name__ == "__main__":
    run_inference()
