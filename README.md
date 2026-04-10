# ⚡ SmartGrid: AI Power Grid Manager

This project was built for the **Meta PyTorch Hackathon x Scaler School of Technology**. 

It is a simulation of a real-world power grid. The goal of the project is to see if an Artificial Intelligence (AI) can successfully manage a city's electricity. The AI has to look at how much power the city needs, how much power is available, and make smart trading decisions to keep the grid stable without wasting money.

## 📖 How It Works

Think of this project like an automated video game where the AI is the player. 

1. **The Game Board:** We created a virtual environment that mimics a power grid. It has rules, scores, and three difficulty levels (Easy, Medium, and Hard).
2. **The Player:** We wrote a script that connects to an AI (like ChatGPT). The AI looks at the current power levels and decides what to do next.
3. **The Loop:** The AI makes a move, the game calculates the score, and then the AI makes its next move. This repeats until the test is over.

## 📂 What The Files Do

Here is a simple breakdown of the main files in this project and what their jobs are:

* **`openenv.yaml` (The ID Card):** This file tells the Hackathon's grading system exactly what our project is, what difficulty levels are available, and how to start the test.
* **`server/app.py` (The Switchboard):** This is the communication hub. It listens for commands like "Start a new game" or "Make this move" and passes those messages to the game board.
* **`environment.py` (The Game Engine):** This file contains the actual math and rules. It calculates supply, demand, and penalties if the AI makes a bad choice.
* **`tasks.py` (The Referee):** This makes sure the game is set to the correct difficulty level when the grader asks for it.
* **`inference.py` (The AI Player):** This is the brain of the operation. It wakes up, connects to the Hackathon's AI system, asks it for the best move, and sends that move to the Switchboard.
* **`Dockerfile` (The Setup Instructions):** This is a set of instructions that automatically installs all the right software so this project can run on any computer in the world without crashing.

## 🚀 The Grading Process

When the Hackathon's automated system tests this project, here is exactly what happens:

1. The system reads the `openenv.yaml` file to learn how to start the program.
2. It turns on our Switchboard (`app.py`) and wakes up our AI Player (`inference.py`).
3. It asks the AI Player to complete a specific task (like the "Hard" difficulty).
4. The AI Player makes up to 50 moves, printing out its score after every single step.
5. When finished, the AI prints a final "Game Over" message with its average score, and the grader records the results.

## 🛠 Want to run it yourself?

If you download this code to your own computer, you can run it by opening two terminal windows:

**Window 1 (Turn on the game):**
```bash
pip install -r requirements.txt
uvicorn server.app:app --host 127.0.0.1 --port 7860
