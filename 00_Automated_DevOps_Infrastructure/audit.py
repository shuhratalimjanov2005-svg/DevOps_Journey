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
        print(f"❌ Telegram API Error: {e}")

def check_cyber_attacks():
    try:
        connection = psycopg2.connect(
            user="user_devops",
            password="password123",
            host="db",          
            port="5432",        
            database="monitoring_db"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT message FROM ram_alerts ORDER BY id DESC LIMIT 1;")
        last_log = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if last_log and "КИБЕРАТАКА" in last_log[0]:
            if not hasattr(check_cyber_attacks, "last_alerted_msg") or check_cyber_attacks.last_alerted_msg != last_log[0]:
                print("🚨 Security Event: DDoS Incident detected in logs! Notifying administrator...")
                send_telegram(f"⚠️ SECURITY ALERT: {last_log[0]}")
                check_cyber_attacks.last_alerted_msg = last_log[0]
                
    except Exception as error:
        print(f"❌ Security Scanner DB Error: {error}")

def save_to_db(ram_usage, hdd_usage, message):
    try:
        connection = psycopg2.connect(user="user_devops", password="password123", host="db", port="5432", database="monitoring_db")
        cursor = connection.cursor()
        insert_query = "INSERT INTO ram_alerts (ram_usage, hdd_usage, message) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (ram_usage, hdd_usage, message))
        connection.commit()
        cursor.close()
        connection.close()
        print("Metrics saved to database. ✅")
    except Exception as error:
        print(f"⚠️ DB Error (falling back to single column schema): {error}")
        try:
            connection = psycopg2.connect(user="user_devops", password="password123", host="db", port="5432", database="monitoring_db")
            cursor = connection.cursor()
            insert_query = "INSERT INTO ram_alerts (ram_usage, message) VALUES (%s, %s)"
            cursor.execute(insert_query, (ram_usage, f"{message} | HDD: {hdd_usage}%"))
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"❌ Database fatal failure: {e}")

def audit_my_repo():
    user = getpass.getuser()
    system = platform.system()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_items = os.listdir('.')
    directories = [d for d in all_items if os.path.isdir(d) and not d.startswith('.')]

    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    total_gb = total // (2**30)
    hdd_usage = round((used / total) * 100, 2) 

    memory = psutil.virtual_memory()
    ram_usage = memory.percent 
    free_ram_gb = memory.available // (1024**3) 

    print(f"\n{'='*30}")
    print(f" DevOps System Report | {now}")
    print(f"{'='*30}")
    print(f"👤 Host User: {user} | 💻 OS Platform: {system}")
    print(f"📁 Active Projects Count: {len(directories)}")
    print(f"🧠 Memory Usage: {ram_usage}% (Available: {free_ram_gb} GB)")
    print(f"💾 Storage Usage: {hdd_usage}% (Free: {free_gb} GB / Total: {total_gb} GB)")

    db_message = f"Status: RAM {ram_usage}%, HDD {hdd_usage}%"
    save_to_db(ram_usage, hdd_usage, db_message)

    if ram_usage > 90:
        print("🔥 Critical RAM overhead alert triggered.")
        send_telegram(f"🚨 RESOURCE ALERT: High Memory Usage ({ram_usage}%) detected on server ({user})!")

    if free_gb < 10:
        print("🛑 Critical Disk Space deficit.")
        send_telegram(f"🚨 RESOURCE ALERT: Critical disk space level! Free storage left: {free_gb} GB!")
    elif free_gb < 20:
        print("⚠️ Warning: Storage capacity dropping.")
        send_telegram(f"⚠️ RESOURCE WARNING: Free disk space dropped to {free_gb} GB.")
    else:
        print("✅ Storage system functions normally.")

    if not os.path.exists('LOGS'):
        os.mkdir('LOGS')
    
    log_path = os.path.join('LOGS', 'report.txt')
    log_entry = f"[{now}] User: {user} | RAM: {ram_usage}% | HDD: {hdd_usage}%\n"
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(f"{'='*30}\n")

if __name__ == "__main__":
    print("🚀 DevOps Monitoring daemon successfully initialized...")
    
    loop_count = 0
    while True:
        check_cyber_attacks()
        
        if loop_count % 100 == 0:
            audit_my_repo()
            
        loop_count += 1
        time.sleep(3)
