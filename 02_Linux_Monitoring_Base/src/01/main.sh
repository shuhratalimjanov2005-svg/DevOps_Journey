#!/bin/bash

# Подключаем наш файл с проверкой (декомпозиция!)
source ./check_input.sh


if [ $# -ne 1 ]; then
    echo "Error: Please provide exactly one parameter."
    exit 1
fi


if check_if_number "$1"; then
    echo "Invalid input: Parameter should not be a number."
else
    
    echo "$1"
fi
