import requests
import time

# Эндпоинт твоего FastAPI, который мы будем флудить запросами
# Меняем на двойку, раз твой FastAPI задеплоен именно там!
URL = "http://127.0.0.2:8000/metrics"

print("😈 ХАКЕРСКИЙ ШТУРМ ЗАПУЩЕН! по локалхосту... 🚀")

success_count = 0
blocked_count = 0

while True:
    try:
        start_time = time.time()
        response = requests.get(URL, timeout=2)
        
        if response.status_code == 200:
            success_count += 1
            print(f"🟢 [ОК] Запрос прошел! Сервер отвечает. Всего: {success_count}")
        elif response.status_code == 403:
            blocked_count += 1
            print(f"🛑 [БАН]  Ошибка 403 Forbidden! Всего банов: {blocked_count}")
            
    except Exception as e:
        print(f"💀 СЕРВЕР ЛЁГ! Мы его уронили: {e}")
        break
        
    time.sleep(0.3) # Лупим каждые 50 миллисекунд, чтоб кукуха сервера закипела!
