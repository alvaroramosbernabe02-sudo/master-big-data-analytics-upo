FROM python:3.12-slim
RUN pip install --no-cache-dir requests google-cloud-storage
COPY main.py /app/main.py
CMD ["python", "/app/main.py"]
