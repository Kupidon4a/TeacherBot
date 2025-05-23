FROM python:3.11

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]