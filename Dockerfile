FROM python:3.12-slim

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY . .

# Создаём нужные файлы внутри контейнера (если надо)
RUN echo "some content" > /app/data/config.txt

CMD ["python", "app.py"]
