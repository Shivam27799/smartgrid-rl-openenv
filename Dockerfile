FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || pip install fastapi uvicorn numpy pydantic openai pyyaml

# Copy files
COPY . .

# Install the project
RUN pip install --no-cache-dir -e .

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
