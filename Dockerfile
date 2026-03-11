FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Если папка data не нужна — удали эти строки
# Если нужна — сначала создай директорию
RUN mkdir -p /app/data
# RUN echo "some content" > /app/data/config.txt

COPY . .

CMD ["python", "app.py"]
