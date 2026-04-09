from environment import SmartGridEnv, GridAction
import numpy as np

def run_grader(difficulty: str):
    """
    Runs 5 full episodes and returns the average score to 
    ensure deterministic and reproducible grading logic.
    """
    num_episodes = 5
    episode_scores = []

    for _ in range(num_episodes):
        env = SmartGridEnv(difficulty=difficulty)
        obs = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            load, supply, price = obs.load, obs.supply, obs.price
            deficit = load - supply
            
            # Heuristic Baseline Agent (Dumb behavior for Hard/Medium)
            if difficulty == "hard":
                action_val = deficit * 0.7  # Laggy/Incomplete response
            elif difficulty == "medium":
                action_val = deficit * 0.9
            else:
                action_val = deficit # Perfect response
                
            action = GridAction(energy_trade=action_val)
            obs, reward, done, _ = env.step(action)
            total_reward += reward
        
        # Calculate daily average reward
        episode_scores.append(total_reward / 24)
    
    # Return the mean of all episodes
    return round(float(np.mean(episode_scores)), 2)

def grader_easy():
    return run_grader("easy")

def grader_medium():
    return run_grader("medium")

def grader_hard():
    return run_grader("hard")