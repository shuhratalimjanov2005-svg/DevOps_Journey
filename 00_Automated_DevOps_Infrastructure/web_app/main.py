import psycopg2
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

DB_CONF = {
    "host": "db",
    "database": "monitoring_db",
    "user": "user_devops",
    "password": "password123"
}

@app.get("/metrics", response_class=HTMLResponse)
def get_metrics():
    try:
        conn = psycopg2.connect(**DB_CONF)
        cur = conn.cursor()
        
        # Забираем последние 20 записей, чтобы была видна история
        cur.execute("SELECT id, alert_time, ram_usage, message FROM ram_alerts ORDER BY alert_time DESC LIMIT 20;")
        data = cur.fetchall()
        
        cur.close()
        conn.close()

        # Генерируем строки таблицы динамически из данных БД
        table_rows = ""
        for row in data:
            # Если RAM больше 80%, подсветим красным
            alert_class = "style='color: #f38ba8; font-weight: bold;'" if row[2] > 80 else ""
            table_rows += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td {alert_class}>{row[2]}%</td>
                <td>{row[3]}</td>
            </tr>
            """

        # Сам HTML-шаблон (стильный дарк-мод)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>RAM Monitoring Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e2e; color: #cdd6f4; padding: 30px; margin: 0; }}
                h1 {{ color: #f5c2e7; text-align: center; margin-bottom: 30px; font-weight: 600; }}
                table {{ width: 85%; margin: 0 auto; border-collapse: collapse; background-color: #313244; box-shadow: 0 8px 16px rgba(0,0,0,0.3); border-radius: 8px; overflow: hidden; }}
                th, td {{ padding: 14px 20px; text-align: center; border-bottom: 1px solid #45475a; }}
                th {{ background-color: #11111b; color: #a6e3a1; font-size: 16px; text-transform: uppercase; letter-spacing: 0.5px; }}
                tr:hover {{ background-color: #45475a; transition: 0.2s; }}
                tr:nth-child(even) {{ background-color: #252538; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Система мониторинга оперативной памяти</h1>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Время замера</th>
                            <th>Загрузка RAM</th>
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
        return HTMLResponse(content=f"<h1 style='color:red;'>Ошибка базы данных:</h1><p>{str(e)}</p>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
