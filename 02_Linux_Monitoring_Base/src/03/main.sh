#!/bin/bash

# Подключаем наши модули
source ./get_data.sh
source ./colors.sh

# 1. Проверка на количество параметров
if [ $# -ne 4 ]; then
    echo "Error: You must provide exactly 4 parameters (1-6)."
    echo "Example: ./main.sh 1 3 4 5"
    exit 1
fi

# 2. Проверка: все ли параметры — цифры от 1 до 6?
for arg in "$@"; do
    if [[ ! $arg =~ ^[1-6]$ ]]; then
        echo "Error: Parameters must be numbers from 1 to 6."
        exit 1
    fi
done

# 3. Проверка на совпадение фона и шрифта в одной колонке
if [ "$1" == "$2" ] || [ "$3" == "$4" ]; then
    echo "Error: Background and font colors match. It will be unreadable!"
    echo "Please run the script again with different parameters."
    exit 1
fi

# 4. Назначаем стили
# \033[фон;текстm
name_style="\033[$(get_color_code $1 bg);$(get_color_code $2 fg)m"
value_style="\033[$(get_color_code $3 bg);$(get_color_code $4 fg)m"
reset="\033[0m"

# 5. Функция красивого вывода
print_line() {
    echo -e "${name_style}$1${reset} = ${value_style}$2${reset}"
}

# Выводим данные
print_line "HOSTNAME" "$HOSTNAME"
print_line "TIMEZONE" "$TIMEZONE"
print_line "USER" "$USER"
print_line "OS" "$OS"
print_line "DATE" "$DATE"
print_line "UPTIME" "$UPTIME"
print_line "UPTIME_SEC" "$UPTIME_SEC"
print_line "IP" "$IP"
print_line "MASK" "$MASK"
print_line "GATEWAY" "$GATEWAY"
print_line "RAM_TOTAL" "$RAM_TOTAL"
print_line "RAM_USED" "$RAM_USED"
print_line "RAM_FREE" "$RAM_FREE"
print_line "SPACE_ROOT" "$SPACE_ROOT"
print_line "SPACE_ROOT_USED" "$SPACE_ROOT_USED"
print_line "SPACE_ROOT_FREE" "$SPACE_ROOT_FREE"
