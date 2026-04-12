import os
import time
import requests
from openai import OpenAI

# 1. Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv("API_KEY", "hf_placeholder")

# 2. Initialize the client
client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
SERVER_URL = "http://0.0.0.0:7860"
TASK_ID = os.getenv("TASK_ID", "hard")

def wait_for_server():
    for _ in range(30):
        try:
            if requests.get(f"{SERVER_URL}/").status_code == 200:
                return True
        except requests.ConnectionError:
            time.sleep(1)
    raise RuntimeError("FastAPI Server did not start in time.")

def run_inference():
    wait_for_server()
    print(f"[START] task={TASK_ID}", flush=True)
    
    try:
        # GET INITIAL STATE
        reset_resp = requests.post(f"{SERVER_URL}/reset?task_id={TASK_ID}").json()
        current_obs = reset_resp
        
        total_reward = 0.0
        done = False
        step = 1
        
        while not done and step <= 50:
            
            # Extract current grid conditions
            load = current_obs.get('load', 0.0)
            supply = current_obs.get('supply', 0.0)
            price = current_obs.get('price', 0.0)
            
            # --- FEED THE ACTUAL DATA TO THE LLM ---
            prompt_text = (
                f"Step {step}. Grid Status -> Load: {load:.4f}, Supply: {supply:.4f}, Price: {price:.4f}. "
                "Calculate the optimal energy_trade value to balance supply and load exactly. "
                "Reply ONLY with a single float number between -1.0 and 1.0."
            )

            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": "You are a highly precise mathematical smart grid controller."},
                        {"role": "user", "content": prompt_text}
                    ],
                    max_tokens=10,
                    temperature=0.0
                )
                
                llm_output = response.choices[0].message.content.strip()
                action_val = float(llm_output)
                    
            except Exception as e:
                print(f"LLM API Error: {e}", flush=True)
                action_val = 0.0
            
            # Send action to environment
            action_payload = {"energy_trade": action_val} 
            step_resp = requests.post(f"{SERVER_URL}/step", json=action_payload).json()
            
            # UPDATE STATE FOR NEXT TURN
            current_obs = step_resp.get("observation", {})
            reward = step_resp.get("reward", 0.0)
            done = step_resp.get("done", False)
            total_reward += reward
            
            print(f"[STEP] step={step} reward={reward:.4f}", flush=True)
            step += 1
            
    except Exception as e:
        print(f"Script Error: {e}", flush=True)
        total_reward = 0.0

    actual_steps = max(1, step - 1)
    avg_score = total_reward / actual_steps
    
    print(f"[END] task={TASK_ID} score={avg_score:.4f} steps={actual_steps}", flush=True)

if __name__ == "__main__":
    run_inference()
