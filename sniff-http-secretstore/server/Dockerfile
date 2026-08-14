FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

# plain HTTP on :80 — this is the point of the challenge
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:80", "app:app"]
