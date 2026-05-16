#!/bin/bash

# Функция для проверки, является ли ввод числом
check_if_number() {
   
    if [[ $1 =~ ^[-+]?[0-9]+\.?[0-9]*$ ]]; then
        return 0 
    else
        return 1 
    fi
}
