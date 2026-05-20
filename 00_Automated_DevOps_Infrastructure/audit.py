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

# МОДИФИЦИРОВАНО: Теперь функция принимает и RAM, и HDD
def save_to_db(ram_usage, hdd_usage, message):
    try:
        connection = psycopg2.connect(
            user="user_devops",
            password="password123",
            host="db",          # Имя сервиса из docker-compose
            port="5432",        # Внутри сети Докера порт 5432
            database="monitoring_db"
        )
        cursor = connection.cursor()
        
        
        insert_query = "INSERT INTO ram_alerts (ram_usage, hdd_usage, message) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (ram_usage, hdd_usage, message))
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Данные успешно сохранены в БД! ✅")
    except Exception as error:
        # Если колонка hdd_usage ещё не создана в БД, скрипт не упадёт, а запишет по-старому
        print(f"⚠️ Ошибка БД (возможно, не добавила колонку hdd_usage): {error}")
        print("Пробую записать только RAM...")
        try:
            connection = psycopg2.connect(user="user_devops", password="password123", host="db", port="5432", database="monitoring_db")
            cursor = connection.cursor()
            insert_query = "INSERT INTO ram_alerts (ram_usage, message) VALUES (%s, %s)"
            cursor.execute(insert_query, (ram_usage, f"{message} | HDD: {hdd_usage}%"))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"❌ Полный завал базы: {e}")

def audit_my_repo():
    # --- ДАННЫЕ СИ СТЕМЫ ---
    user = getpass.getuser()
    system = platform.system()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- ПРОВЕРКА ПРОЕКТОВ ---
    all_items = os.listdir('.')
    directories = [d for d in all_items if os.path.isdir(d) and not d.startswith('.')]

    # --- МОНИТОРИНГ ЖЕЛЕЗА (HDD) ---
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    # НОВОЕ: Считаем точный процент занятого диска для сайта!
    hdd_usage = round((used / total) * 100, 2) 

    # --- МОНИТОРИНГ RAM ---
    memory = psutil.virtual_memory()
    ram_usage = memory.percent 
    free_ram_gb = memory.available // (1024**3) 

    # --- ВЫВОД В КОНСОЛЬ ---
    print(f"\n{'='*30}")
    print(f" DevOps Report | {now}")
    print(f"{'='*30}")
    print(f"👤 Boss: {user} | 💻 OS: {system}")
    print(f"📁 Projects: {len(directories)} ({', '.join(directories) if directories else 'none'})")
    print(f"🧠 Оперативка: {ram_usage}% занято (Свободно: {free_ram_gb} GB)")
    print(f"💾 Диск: {hdd_usage}% занято (Свободно: {free_gb} GB из {total_gb} GB)")

    # --- МОДИФИЦИРОВАНО: ОТПРАВКА В БД ДЛЯ САЙТА ---
    # Отправляем и RAM, и HDD, и развёрнутый текстовый отчёт
    db_message = f"Status: RAM {ram_usage}%, HDD {hdd_usage}%"
    save_to_db(ram_usage, hdd_usage, db_message)

    # --- НОВЫЙ АЛЕРТ НА RAM ---
    if ram_usage > 90:
        print("🔥 КРИТИЧЕСКИЙ УРОВЕНЬ RAM!")
        send_telegram(f"🚨 АЛЕРТ: Оперативка на сервере ({user}) забита на {ram_usage}%! Свободно всего {free_ram_gb} GB!")

    # --- МОДИФИЦИРОВАНО: АЛЕРТ НА МЕСТО (HDD) В ТЕЛЕГРАМ ---
    if free_gb < 10:
        print("🛑 КРИТИЧЕСКИЙ УРОВЕНЬ ДИСКА! Сигнал в ТГ отправлен.")
        send_telegram(f"🚨 АЛЕРТ МЕСТА: На сервере ({user}) осталось ВСЕГО {free_gb} GB диска! Занято {hdd_usage}%! Срочно чисти логи!")
    elif free_gb < 20:
        print("⚠️ ПРЕДУПРЕЖДЕНИЕ: Место на диске заканчивается.")
        send_telegram(f"⚠️ ВНИМАНИЕ: На сервере ({user}) свободное место упало до {free_gb} GB ({hdd_usage}% занято).")
    else:
        print("✅ С ДИСКОМ ВСЁ ХОРОШО!")

    # --- ПРОВЕРКА ПАПКИ ЛОГОВ ---
    if not os.path.exists('LOGS'):
        os.mkdir('LOGS')
    
    # --- ЗАПИСЬ В ТЕКСТОВЫЙ ЛОГ ---
    log_path = os.path.join('LOGS', 'report.txt')
    log_entry = f"[{now}] User: {user} | RAM: {ram_usage}% | HDD: {hdd_usage}% (Free: {free_gb}GB) | Projects: {len(directories)}\n"
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    print(f"{'='*30}\n")

if __name__ == "__main__":
    print("🚀 Кастомный DevOps-мониторинг успешно запущен и бдит...")
    while True:
        audit_my_repo()
        time.sleep(300) # Проверка каждые 5 минут
