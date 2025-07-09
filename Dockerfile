FROM python:3.10-slim

WORKDIR /app

COPY lib.txt .
RUN pip install --no-cache-dir -r lib.txt

COPY . .

# Переменные для Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Запуск через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]