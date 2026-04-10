import numpy as np
from environment import SmartGridEnv, GridAction

def run_grader(difficulty: str, trajectory=None):
    """
    Runs 5 full episodes and returns the average score.
    The 'trajectory' argument is required by the OpenEnv interface.
    """
    num_episodes = 5
    episode_scores = []
    
    for _ in range(num_episodes):
        env = SmartGridEnv(difficulty=difficulty)
        obs = env.reset()
        total_reward = 0
        done = False
                
        while not done:
            # Handle both object and dict style observations for safety
            load = getattr(obs, 'load', obs.get('load') if isinstance(obs, dict) else 0)
            supply = getattr(obs, 'supply', obs.get('supply') if isinstance(obs, dict) else 0)
            
            deficit = load - supply
            
            # Heuristic Baseline Agent
            if difficulty == "hard":
                action_val = deficit * 0.7 
            elif difficulty == "medium":
                action_val = deficit * 0.9
            else:
                action_val = deficit
                
            action = GridAction(energy_trade=action_val)
            obs, reward, done, _ = env.step(action)
            total_reward += reward
                
        episode_scores.append(total_reward / 24)
        
    return round(float(np.mean(episode_scores)), 4)

# These wrappers must accept 'trajectory' to match the openenv.yaml call
def grader_easy(trajectory=None):
    return run_grader("easy", trajectory)

def grader_medium(trajectory=None):
    return run_grader("medium", trajectory)

def grader_hard(trajectory=None):
    return run_grader("hard", trajectory)
