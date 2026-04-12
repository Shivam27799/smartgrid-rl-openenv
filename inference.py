import os
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
        except Exception as e:
            print(f"API Error: {e}")
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
