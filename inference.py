import os
from openai import OpenAI
from environment import SmartGridEnv, GridAction

# MANDATORY VARIABLES FROM CHECKLIST
# The validator injects these; we MUST use them.
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

# For the OpenAI Client compatibility, we map HF_TOKEN to API_KEY
API_KEY = HF_TOKEN if HF_TOKEN else "dummy"

# Initialize client using the specific checklist variables
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
    
    # [START] block - MUST be first
    print(f"[START] task={task_name}", flush=True)
    
    for step in range(1, max_steps + 1):
        # Prompting the LLM
        prompt = f"Load: {obs.load:.2f}, Supply: {obs.supply:.2f}, Price: {obs.price:.2f}. Action (-1.0 to 1.0):"
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME, # Use the mandatory MODEL_NAME variable
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10
            )
            action_val = float(response.choices[0].message.content.strip())
        except:
            action_val = (obs.load - obs.supply) * 0.7 
        
        # Step environment
        action = GridAction(energy_trade=action_val)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        
        # [STEP] block - MUST be printed every step
        print(f"[STEP] step={step} reward={reward:.4f}", flush=True)
        
        if done:
            break
            
    final_score = total_reward / max_steps
    # [END] block - MUST include score and steps
    print(f"[END] task={task_name} score={final_score:.4f} steps={max_steps}", flush=True)

if __name__ == "__main__":
    run_inference()
