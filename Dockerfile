# Use a lightweight Python 3.9 base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Upgrade pip to avoid installation errors
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy just the requirements first (to cache this layer and speed up future builds)
COPY requirements.txt .

# Install dependencies. The || provides a fallback in case requirements.txt misses something core.
RUN pip install --no-cache-dir -r requirements.txt || pip install fastapi uvicorn numpy pydantic openai pyyaml requests

# Copy the rest of your project files into the container
COPY . .

# Install your project in editable mode (links the pyproject.toml logic)
RUN pip install --no-cache-dir -e .

# Hugging Face strictly requires traffic on port 7860
EXPOSE 7860

# --- THE CRITICAL ENTRY POINT ---
# 1. Start uvicorn in the background using '&'
# 2. Wait 15 seconds to guarantee the server is fully awake and listening
# 3. Run the inference script to trigger the task evaluation
CMD uvicorn server.app:app --host 0.0.0.0 --port 7860 & sleep 15 && python inference.py && tail -f /dev/null
