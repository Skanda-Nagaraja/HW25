FROM python:3.9-slim

WORKDIR /app

COPY vulnerable_app.py .

CMD ["python", "vulnerable_app.py"]