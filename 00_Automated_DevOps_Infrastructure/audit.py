import os
import shutil
import platform
import getpass
from datetime import datetime
import requests
import psutil
import time
import psycopg2

TOKEN = "8874275515:AAHjSErhnhlcvLqMgq4G8H0UtHHK9nAS9RU"
CHAT_ID = 8278904536 

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        response = requests.get(url)
        print(response.json())
    except Exception as e:
        print(f"❌ Ошибка отправки в ТГ: {e}")

def save_to_db(usage, message):
    try:
        connection = psycopg2.connect(
            user="user_devops",
            password="password123",
            host="db",          # МЕНЯЕМ: Указываем имя сервиса из docker-compose
            port="5432",        # МЕНЯЕМ: Внутри сети Докера порт всегда 5432
            database="monitoring_db"
        )
        cursor = connection.cursor()
        
        # Записываем данные в наш "шкафчик"
        insert_query = "INSERT INTO ram_alerts (ram_usage, message) VALUES (%s, %s)"
        cursor.execute(insert_query, (usage, message))
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Данные успешно сохранены в БД! ")
    except Exception as error:
        print(f"Ошибка при работе с БД: {error}")
    
    

def audit_my_repo():
    # --- ДАННЫЕ СИСТЕМЫ ---
    user = getpass.getuser()
    system = platform.system()
    current_dir = os.getcwd()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- ПРОВЕРКА ПРОЕКТОВ ---
    all_items = os.listdir('.')
    directories = [d for d in all_items if os.path.isdir(d) and not d.startswith('.')]

    # --- МОНИТОРИНГ ЖЕЛЕЗА ---
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)

    # --- МОНИТОРИНГ RAM ---
    memory = psutil.virtual_memory()
    ram_usage = memory.percent # Процент занятой памяти
    free_ram_gb = memory.available // (1024**3) # Свободно в ГБ

    # ... (старый вывод в консоль) ...
    print(f"🧠 Оперативка: {ram_usage}% занято (Свободно: {free_ram_gb} GB)")
    
    # --- ЗАПИСЬ В БАЗУ ПРИ КАЖДОЙ ПРОВЕРКЕ ---
    # Вызываем функцию здесь, а не внутри самой функции!
    save_to_db(ram_usage, f"Отчёт: RAM {ram_usage}%")

    # --- НОВЫЙ АЛЕРТ ---
    if ram_usage > 90:
        print("🔥 КРИТИЧЕСКИЙ УРОВЕНЬ RAM!")
        send_telegram(f"🚨Оперативка забита на {ram_usage}%!")

    # --- КРАСИВЫЙ ВЫВОД В КОНСОЛЬ ---
    print(f"\n{'='*30}")
    print(f" DevOps Report | {now}")
    print(f"{'='*30}")
    print(f"👤 Boss: {user} | 💻 OS: {system}")
    print(f"📁 Projects: {len(directories)} ({', '.join(directories) if directories else 'none'})")
    print(f"💾 Free space: {free_gb} GB")

    # --- ПРОВЕРКА ПАПКИ ЛОГОВ ---
    if not os.path.exists('LOGS'):
        os.mkdir('LOGS')
    
    # --- ЗАПИСЬ В ЛОГ ---
    log_path = os.path.join('LOGS', 'report.txt')
    log_entry = f"[{now}] User: {user} | Free: {free_gb}GB | Projects: {len(directories)}\n"
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    # --- АВТО-ДИАГНОСТИКА И ТЕЛЕГРАМ ---
    if free_gb < 10:
        print("🛑 КРИТИЧЕСКИЙ УРОВЕНЬ! Сигнал в ТГ отправлен.")
        send_telegram(f"🚨 На сервере ({user}) осталось всего {free_gb}GB! Срочно спасаем ситуацию!")
    elif free_gb < 20:
        print("⚠️ ПРЕДУПРЕЖДЕНИЕ: Место заканчивается.")
    else:
        print("✅ ВСЁ ХОРОШО: Кодим дальше! ✨")
    
    print(f"{'='*30}\n")

if __name__ == "__main__":
    while True:
        audit_my_repo()
        time.sleep(300) # Спим 5 минут и по ново
