CREATE TABLE IF NOT EXISTS ram_alerts (
    id SERIAL PRIMARY KEY,
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ram_usage FLOAT,
    message TEXT
);
