# 1. Берем легкий образ Питона
FROM python:3.9-slim

# 2. Создаем папку внутри контейнера
WORKDIR /app

# 3. Копируем наш скрипт внутрь
COPY audit.py .

# 4. Устанавливаем библиотеки (те самые requests и psutil)
RUN pip install requests psutil psycopg2-binary

# 5. Команда для запуска
CMD ["python", "audit.py"]
