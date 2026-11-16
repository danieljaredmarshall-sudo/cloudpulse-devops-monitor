FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py monitor.py ./
COPY templates/ ./templates/
EXPOSE 5000
ENV PORT=5000 CHECK_INTERVAL=60
CMD ["python", "app.py"]
