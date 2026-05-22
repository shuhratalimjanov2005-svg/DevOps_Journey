import psycopg2
import os
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Database connection configuration
DB_CONF = {
    "host": "db",
    "database": "monitoring_db",
    "user": "user_devops",
    "password": "password123"
}

# Rate limiting storage and configuration
ALL_REQUESTS = []
LIMIT_REQUESTS = 10
LIMIT_WINDOW = 5
LAST_DB_LOG_TIME = 0  # Cooldown timer to prevent database flooding during attack

@app.get("/metrics", response_class=HTMLResponse)
def get_metrics(request: Request):
    global ALL_REQUESTS, LAST_DB_LOG_TIME
    current_time = time.time()

    # Clear logs older than the time window (5 seconds)
    ALL_REQUESTS = [t for t in ALL_REQUESTS if current_time - t < LIMIT_WINDOW]

    # Register the incoming request timestamp
    ALL_REQUESTS.append(current_time)

    # 🚨 DDoS Detection Logic
    if len(ALL_REQUESTS) > LIMIT_REQUESTS:
        print(f"⚠️ Security Alert: Rate limit exceeded! Requests count: {len(ALL_REQUESTS)}")
        
        # Log incident to DB with a 10-second cooldown interval
        if current_time - LAST_DB_LOG_TIME > 10:
            try:
                conn = psycopg2.connect(**DB_CONF)
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO ram_alerts (ram_usage, hdd_usage, message) VALUES (%s, %s, %s);",
                    (99.9, 99.9, "🚨 КИБЕРАТАКА С ИНТЕРНЕТА! ПОПЫТКА ДДОСА ОТРЕЖЕНА!")
                )
                conn.commit()
                cur.close()
                conn.close()
                LAST_DB_LOG_TIME = current_time
                print("📝 Incident successfully logged into database.")
            except Exception as db_err:
                print(f"❌ Database error logging incident: {db_err}")

        # Return HTTP 403 Forbidden status
        return HTMLResponse(
            content="<h1 style='color:red; text-align:center; margin-top:50px;'>🛑 403 FORBIDDEN: Rate limit exceeded. Connection blocked.</h1>", 
            status_code=403
        )

    # 🟢 Standard Metrics Handler (Normal Operation Mode)
    try:
        conn = psycopg2.connect(**DB_CONF)
        cur = conn.cursor()

        cur.execute("SELECT id, alert_time, ram_usage, hdd_usage, message FROM ram_alerts ORDER BY alert_time DESC LIMIT 20;")
        data = cur.fetchall()

        cur.close()
        conn.close()

        table_rows = ""
        for row in data:
            # High resource usage thresholds markers
            ram_alert = "style='color: #f38ba8; font-weight: bold;'" if row[2] and row[2] > 80 else ""
            hdd_alert = "style='color: #f38ba8; font-weight: bold;'" if row[3] and row[3] > 80 else ""

            # Highlight malicious activity rows
            is_attack = "style='background-color: #585b70; color: #f38ba8; font-weight: bold;'" if row[4] and "КИБЕРАТАКА" in str(row[4]) else ""

            hdd_val = f"{row[3]}%" if row[3] is not None else "0.0%"

            table_rows += f"""
            <tr {is_attack}>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td {ram_alert}>{row[2]}%</td>
                <td {hdd_alert}>{hdd_val}</td>
                <td>{row[4]}</td>
            </tr>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>DevOps System Monitoring Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e2e; color: #cdd6f4; padding: 30px; margin: 0; }}
                h1 {{ color: #f5c2e7; text-align: center; margin-bottom: 30px; font-weight: 600; }}
                table {{ width: 90%; margin: 0 auto; border-collapse: collapse; background-color: #313244; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border-radius: 8px; overflow: hidden; }}
                th, td {{ padding: 14px 20px; text-align: center; border-bottom: 1px solid #45475a; }}
                th {{ background-color: #11111b; color: #a6e3a1; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px; }}
                tr:hover {{ background-color: #45475a; transition: 0.2s; }}
                tr:nth-child(even) {{ background-color: #252538; }}
                .container {{ max-width: 1300px; margin: 0 auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Система мониторинга серверов + 🛡️ Модуль Rate Limiting (DDoS Protection)</h1>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Время замера</th>
                            <th>Загрузка RAM</th>
                            <th>Загрузка HDD (Диск)</th>
                            <th>Статус / Сообщение</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        return HTMLResponse(content=f"<h1 style='color:red;'>Internal Database Error:</h1><p>{str(e)}</p>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
