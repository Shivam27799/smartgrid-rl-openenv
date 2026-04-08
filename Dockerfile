FROM python:3.9-slim

WORKDIR /app

# Install system dependencies needed for some python packages
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Install the current project in editable mode to satisfy the 'server' entry point
RUN pip install -e .

# OpenEnv/Hugging Face Port
EXPOSE 7860

# Start the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
