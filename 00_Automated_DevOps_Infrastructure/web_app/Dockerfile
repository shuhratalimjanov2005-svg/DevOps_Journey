FROM python:3.9-slim

WORKDIR /app

# Устанавливаем нужные библиотеки
RUN pip install fastapi uvicorn psycopg2-binary

COPY . .

# Запускаем сервер на порту 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
