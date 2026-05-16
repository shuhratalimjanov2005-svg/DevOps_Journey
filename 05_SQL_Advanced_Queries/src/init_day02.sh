#!/bin/bash

# Цикл от 0 до 10
for i in {00..10}
do
    # Создаем папку ex00, ex01 и т.д.
    folder="ex$i"
    mkdir -p "$folder"
    
    # Создаем внутри файл day02_ex00.sql и т.д.
    # Используем printf, чтобы номер был с нулем (00, 01...)
    filename="day02_ex$i.sql"
    touch "$folder/$filename"
    
    echo "Создана папка $folder с файлом $filename ✅"
done

echo "Уфф, всё готово! Теперь можно спокойно кодить. 🥂✨😻"
