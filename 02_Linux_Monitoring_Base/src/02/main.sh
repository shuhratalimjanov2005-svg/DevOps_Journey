#!/bin/bash

# Подключаем сборщик данных
source ./get_data.sh

# Функция вывода данных
print_data() {
    echo "HOSTNAME = $HOSTNAME"
    echo "TIMEZONE = $TIMEZONE"
    echo "USER = $USER"
    echo "OS = $OS"
    echo "DATE = $DATE"
    echo "UPTIME = $UPTIME"
    echo "UPTIME_SEC = $UPTIME_SEC"
    echo "IP = $IP"
    echo "MASK = $MASK"
    echo "GATEWAY = $GATEWAY"
    echo "RAM_TOTAL = $RAM_TOTAL"
    echo "RAM_USED = $RAM_USED"
    echo "RAM_FREE = $RAM_FREE"
    echo "SPACE_ROOT = $SPACE_ROOT"
    echo "SPACE_ROOT_USED = $SPACE_ROOT_USED"
    echo "SPACE_ROOT_FREE = $SPACE_ROOT_FREE"
}

# Выводим информацию
print_data

# Спрашиваем про запись в файл
echo
read -p "Do you want to save this data to a file? (Y/N): " answer

if [[ "$answer" == "Y" || "$answer" == "y" ]]; then
    # Генерируем имя файла по маске DD_MM_YY_HH_MM_SS.status
    FILENAME=$(date +"%d_%m_%y_%H_%M_%S.status")
    # Записываем всё в файл
    print_data > "$FILENAME"
    echo "Data saved to $FILENAME"
else
    echo "Data was not saved."
fi
