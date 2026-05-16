#!/bin/bash

# Функция для получения кода цвета (фон или текст)
# $1 - номер цвета (1-6), $2 - тип (bg или fg)
get_color_code() {
    local color=$1
    local type=$2
    
    if [ "$type" == "bg" ]; then
        case $color in
            1) echo "107" ;; # White
            2) echo "41"  ;; # Red
            3) echo "42"  ;; # Green
            4) echo "44"  ;; # Blue
            5) echo "45"  ;; # Purple
            6) echo "40"  ;; # Black
        esac
    else
        case $color in
            1) echo "97" ;; # White
            2) echo "31" ;; # Red
            3) echo "32" ;; # Green
            4) echo "34" ;; # Blue
            5) echo "35" ;; # Purple
            6) echo "30" ;; # Black
        esac
    fi
}
