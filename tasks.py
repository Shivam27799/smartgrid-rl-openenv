__all__ = ["TASKS", "grader_easy", "grader_medium", "grader_hard"]

def run_grader(difficulty: str, trajectory=None, **kwargs):
    import numpy as np
    from environment import SmartGridEnv, GridAction
    
    num_episodes = 5
    episode_scores = []
    
    for _ in range(num_episodes):
        env = SmartGridEnv(difficulty=difficulty)
        obs = env.reset()
        total_reward = 0
        done = False
                
        while not done:
            load = getattr(obs, 'load', obs.get('load') if isinstance(obs, dict) else 0)
            supply = getattr(obs, 'supply', obs.get('supply') if isinstance(obs, dict) else 0)
            
            deficit = load - supply
            
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


def grader_easy(trajectory=None, **kwargs):
    return run_grader("easy", trajectory, **kwargs)

def grader_medium(trajectory=None, **kwargs):
    return run_grader("medium", trajectory, **kwargs)

def grader_hard(trajectory=None, **kwargs):
    return run_grader("hard", trajectory, **kwargs)


# ✅ ADD THIS PART (THIS IS THE FIX)
def create_env_easy():
    from environment import SmartGridEnv
    return SmartGridEnv(difficulty="easy")

def create_env_medium():
    from environment import SmartGridEnv
    return SmartGridEnv(difficulty="medium")

def create_env_hard():
    from environment import SmartGridEnv
    return SmartGridEnv(difficulty="hard")


TASKS = [
    {
        "name": "smartgrid_easy",
        "env": create_env_easy,
        "grader": grader_easy
    },
    {
        "name": "smartgrid_medium",
        "env": create_env_medium,
        "grader": grader_medium
    },
    {
        "name": "smartgrid_hard",
        "env": create_env_hard,
        "grader": grader_hard
    }
]
