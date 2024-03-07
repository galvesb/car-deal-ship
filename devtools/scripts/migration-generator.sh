#!/bin/sh

file_name=migration_example.py

current_time=$(date "+%Y%m%d%H%M")

new_file_name="${current_time}_$1.py"

cp ./devtools/scripts/$file_name ./migrations/$new_file_name
echo "Novo arquivo de migration gerado: $new_file_name"
