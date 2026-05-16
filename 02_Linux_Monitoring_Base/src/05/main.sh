#!/bin/bash

# Засекаем время начала
start_time=$(date +%s.%N)

# 1. Проверка на наличие параметра и наличие '/' в конце
if [ $# -ne 1 ]; then
    echo "Error: Path to directory is required."
    exit 1
fi

if [[ ! "$1" =~ /$ ]]; then
    echo "Error: The path must end with '/'."
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Error: Directory does not exist."
    exit 1
fi

path=$1

echo "Total number of folders (including all nested ones) = $(find "$path" -type d | wc -l)"

echo "TOP 5 folders of maximum size arranged in descending order (path and size):"
# du -h считает размер, sort -rh сортирует, head -5 берет первые пять
du -h "$path"* 2>/dev/null | sort -rh | head -5 | awk '{print NR " - " $2 "/, " $1}'

echo "Total number of files = $(find "$path" -type f | wc -l)"

echo "Number of:"
echo "Configuration files (with the .conf extension) = $(find "$path" -type f -name "*.conf" | wc -l)"
echo "Text files = $(find "$path" -type f -exec file {} + | grep -c "text")"
echo "Executable files = $(find "$path" -type f -executable | wc -l)"
echo "Log files (with the extension .log) = $(find "$path" -type f -name "*.log" | wc -l)"
echo "Archive files = $(find "$path" -type f \( -name "*.zip" -o -name "*.tar" -o -name "*.gz" -o -name "*.rar" \) | wc -l)"
echo "Symbolic links = $(find "$path" -type l | wc -l)"

echo "TOP 10 files of maximum size arranged in descending order (path, size and type):"
find "$path" -type f -exec du -h {} + 2>/dev/null | sort -rh | head -10 | awk '{
    split($2, a, "."); 
    ext=a[length(a)]; 
    if (ext == $2) ext="no extension";
    printf "%d - %s, %s, %s\n", NR, $2, $1, ext
}'

echo "TOP 10 executable files of the maximum size arranged in descending order (path, size and MD5 hash of file):"
# Ищем исполняемые, сортируем, берем 10 и для каждого считаем md5
exec_files=$(find "$path" -type f -executable -exec du -h {} + 2>/dev/null | sort -rh | head -10)
if [ -z "$exec_files" ]; then
    echo "No executable files found."
else
    echo "$exec_files" | awk '{printf "%d - %s, %s, ", NR, $2, $1; system("md5sum " $2 " | awk \047{print $1}\047")}'
fi

# Считаем время выполнения
end_time=$(date +%s.%N)
execution_time=$(echo "$end_time - $start_time" | bc)
printf "Script execution time (in seconds) = %.2f\n" "$execution_time"
