import os
from openai import OpenAI
from environment import SmartGridEnv, GridAction

# 1. MUST capture the injected Proxy URL and Key from the OpenEnv Grader
API_KEY = os.getenv("API_KEY", "dummy_key")
API_BASE = os.getenv("API_BASE_URL", "https://api.openai.com/v1") 

# 2. Initialize the client using their specific routing
client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE
)

def run_inference():
    task_name = "hard"
    env = SmartGridEnv(difficulty=task_name)
    obs = env.reset()
    total_reward = 0
    max_steps = 24
    
    # Required Structured Logging
    print(f"[START] task={task_name}", flush=True)
    
    for step in range(1, max_steps + 1):
        
        # 3. Create a text prompt for the LLM based on the current state
        prompt = f"Grid State - Load: {obs.load:.2f}, Supply: {obs.supply:.2f}, Price: {obs.price:.2f}. Reply with ONLY a single float number between -1.0 and 1.0 for the energy trade action."
        
        try:
            # 4. ACTUALLY CALL THE PROXY API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # The proxy will intercept and route this
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10
            )
            
            # Parse the LLM's text response back into a float
            result_text = response.choices[0].message.content.strip()
            action_val = float(result_text)
            
        except Exception as e:
            # Fallback constraint: If the proxy fails or LLM outputs words instead of a number,
            # fall back to our heuristic so the trajectory doesn't crash halfway through.
            action_val = (obs.load - obs.supply) * 0.7 
        
        # Step the environment with the Agent's chosen action
        action = GridAction(energy_trade=action_val)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        
        # Required Structured Logging
        print(f"[STEP] step={step} reward={reward:.4f}", flush=True)
        
        if done:
            break
            
    final_score = total_reward / max_steps
    
    # Required Structured Logging
    print(f"[END] task={task_name} score={final_score:.4f} steps={max_steps}", flush=True)

if __name__ == "__main__":
    run_inference()
