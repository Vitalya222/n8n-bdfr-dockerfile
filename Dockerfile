FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Ставим praw отдельно (нужен для bdfr)
RUN pip install --no-cache-dir praw==7.7.0 flask==2.3.3

# Ставим bdfr прямо из репозитория
RUN pip install --no-cache-dir git+https://github.com/aliparlakci/bulk-downloader-for-reddit.git

COPY app.py .

CMD ["python", "app.py"]
