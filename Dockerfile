FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install uv && uv lock
# Port 7860 is the standard for Hugging Face Spaces
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
