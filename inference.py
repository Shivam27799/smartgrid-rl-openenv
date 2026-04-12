import os
import sys
from environment import SmartGridEnv, GridAction

def clamp_action(value: float) -> float:
    """Clamp action to valid range [-1.0, 1.0]."""
    return max(-1.0, min(1.0, value))

def smart_agent(obs, task_difficulty: str):
    """
    Smart rule-based agent - works without API calls.
    Adapts strategy based on difficulty level.
    """
    load_diff = obs.load - obs.supply
    
    if task_difficulty == "easy":
        action = clamp_action(load_diff * 0.5)
    elif task_difficulty == "medium":
        price_impact = (obs.price - 0.5) * 0.4
        action = clamp_action(load_diff * 0.6 + price_impact)
    else:
        price_impact = (obs.price - 0.5) * 0.3
        supply_margin = abs(obs.load - obs.supply)
        if supply_margin > 0.5:
            action = clamp_action(load_diff * 0.8 + price_impact)
        else:
            action = clamp_action(load_diff * 0.4 + price_impact * 0.5)
    
    return action

def run_task(task_name: str):
    """Run a single task."""
    max_steps = 24
    step = 0
    
    try:
        env = SmartGridEnv(difficulty=task_name)
        obs = env.reset()
    except Exception as e:
        print(f"[ERROR] Environment initialization failed: {e}", file=sys.stderr)
        return None
    
    total_reward = 0.0
    
    print(f"[START] task={task_name}", flush=True)
    
    for step in range(1, max_steps + 1):
        try:
            action_val = smart_agent(obs, task_name)
            action = GridAction(energy_trade=action_val)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            
            print(f"[STEP] step={step} reward={reward:.4f}", flush=True)
            
            if done:
                break
        except Exception as e:
            print(f"[ERROR] Step {step} failed: {e}", file=sys.stderr)
            break
    
    final_score = total_reward / max_steps
    print(f"[END] task={task_name} score={final_score:.4f} steps={step}", flush=True)
    
    return final_score

def run_all_tasks():
    """Run all 3 tasks."""
    tasks = ["easy", "medium", "hard"]
    results = []
    
    for task_name in tasks:
        print(f"\n========== RUNNING TASK: {task_name.upper()} ==========", file=sys.stderr)
        try:
            score = run_task(task_name)
            if score is not None:
                results.append({"task": task_name, "score": score})
        except Exception as e:
            print(f"[ERROR] Task {task_name} failed: {e}", file=sys.stderr)
    
    print(f"\n[SUMMARY] Completed {len(results)}/3 tasks", flush=True)
    return results

if __name__ == "__main__":
    try:
        run_all_tasks()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[INTERRUPTED]", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)
