FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Let's add a placeholder .env variable. Use TELEGRAM_TOKEN at runtime.
# ENV TELEGRAM_TOKEN=""

CMD ["python", "bot.py"]
