FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install uv and project dependencies
RUN pip install --no-cache-dir uv
COPY . .
RUN uv pip install --system -r requirements.txt
RUN uv pip install --system .

# Generate the lock file required by the validator
RUN uv lock

# OpenEnv requires port 7860 for Hugging Face
EXPOSE 7860

# This starts the 'server' entry point defined in pyproject.toml
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
