#!/bin/bash

# Подключаем старые модули
source ./get_data.sh
source ./colors.sh

# 1. Читаем конфиг. Мы используем 'source', чтобы переменные из файла стали доступны здесь.
if [ -f "config.conf" ]; then
    source ./config.conf
fi

# 2. Устанавливаем дефолтные значения, если в конфиге пусто (Developer's discretion!)
# Используем конструкцию ${VAR:-DEFAULT}
c1_bg=${column1_background:-6}   # default: black
c1_fg=${column1_font_color:-1}   # default: white
c2_bg=${column2_background:-2}   # default: red
c2_fg=${column2_font_color:-6}   # default: black

# 3. Проверка на совпадение
if [ "$c1_bg" == "$c1_fg" ] || [ "$c2_bg" == "$c2_fg" ]; then
    echo "Error: Background and font colors match. Fix config.conf!"
    exit 1
fi

# 4. Назначаем стили
name_style="\033[$(get_color_code $c1_bg bg);$(get_color_code $c1_fg fg)m"
value_style="\033[$(get_color_code $c2_bg bg);$(get_color_code $c2_fg fg)m"
reset="\033[0m"

# 5. Вывод инфы (функция из Part 3)
print_line() {
    echo -e "${name_style}$1${reset} = ${value_style}$2${reset}"
}

print_line "HOSTNAME" "$HOSTNAME"
# ... (добавь остальные строки как в Part 3) ...
print_line "SPACE_ROOT_FREE" "$SPACE_ROOT_FREE"

# 6. Вывод цветовой схемы (через пустую строку)
echo
print_color_name() {
    case $1 in
        1) echo "white" ;;
        2) echo "red" ;;
        3) echo "green" ;;
        4) echo "blue" ;;
        5) echo "purple" ;;
        6) echo "black" ;;
    esac
}

# Функция для вывода статуса цвета (задан или дефолт)
print_scheme_line() {
    local label=$1
    local val=$2
    local def_val=$3
    local color_idx=$4
    
    if [ -z "$val" ]; then
        echo "$label = default ($(print_color_name $def_val))"
    else
        echo "$label = $color_idx ($(print_color_name $color_idx))"
    fi
}

print_scheme_line "Column 1 background" "$column1_background" 6 $c1_bg
print_scheme_line "Column 1 font color" "$column1_font_color" 1 $c1_fg
print_scheme_line "Column 2 background" "$column2_background" 2 $c2_bg
print_scheme_line "Column 2 font color" "$column2_font_color" 6 $c2_fg
