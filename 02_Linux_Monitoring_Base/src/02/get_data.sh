#!/bin/bash

# Собираем данные
HOSTNAME=$(hostname)
TIMEZONE="$(cat /etc/timezone) $(date +'%Z %:z')"
USER=$(whoami)
OS=$(cat /etc/issue | awk '{print $1, $2, $3}' | head -n 1)
DATE=$(date +"%d %b %Y %H:%M:%S")
UPTIME=$(uptime -p)
UPTIME_SEC=$(awk '{print $1}' /proc/uptime)

# Сеть (берем первый попавшийся интерфейс, кроме петли)
IP=$(hostname -I | awk '{print $1}')
MASK=$(ifconfig | grep -A 1 "$IP" | tail -n 1 | awk '{print $4}')
GATEWAY=$(ip route | grep default | awk '{print $3}')

# Память (считаем в ГБ с точностью до 3 знаков)
RAM_TOTAL=$(free -g | awk '/Mem:/{printf "%.3f GB", $2}')
RAM_USED=$(free -g | awk '/Mem:/{printf "%.3f GB", $3}')
RAM_FREE=$(free -g | awk '/Mem:/{printf "%.3f GB", $4}')

# Место на диске (в МБ с точностью до 2 знаков)
SPACE_ROOT=$(df / | awk 'NR==2{printf "%.2f MB", $2/1024}')
SPACE_ROOT_USED=$(df / | awk 'NR==2{printf "%.2f MB", $3/1024}')
SPACE_ROOT_FREE=$(df / | awk 'NR==2{printf "%.2f MB", $4/1024}')
