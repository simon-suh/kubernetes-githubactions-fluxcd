FROM python:3.13-slim

WORKDIR /app

COPY app.py .

RUN pip install flask --no-cache-dir

EXPOSE 5000

CMD ["python3", "app.py"]
