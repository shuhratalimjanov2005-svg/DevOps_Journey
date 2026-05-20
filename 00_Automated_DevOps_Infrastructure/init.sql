CREATE TABLE IF NOT EXISTS ram_alerts (
    id SERIAL PRIMARY KEY,
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ram_usage FLOAT,
    hdd_usage FLOAT DEFAULT 0.0, -- НАША НОВАЯ СОЧНАЯ МОДИФИКАЦИЯ ДЛЯ МЕСТА! 💾
    message TEXT
);
