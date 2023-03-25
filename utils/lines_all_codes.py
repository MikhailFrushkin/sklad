import os
from data.config import path

import os

# Список папок, которые не нужно учитывать
ignore_folders = ['venv', '.git', '.idea']

# Функция для проверки, является ли строка пустой или закомментированной
def is_empty_or_comment(line):
    return line.strip() == '' or line.strip().startswith('#')

# Счетчик строк
total_lines = 0

# Проход по всем файлам с расширением .py в проекте
for root, dirs, files in os.walk(path):
    # Исключение папок, которые не нужно учитывать
    dirs[:] = [d for d in dirs if d not in ignore_folders]

    for file in files:
        if file.endswith('.py'):
            # Открытие файла
            with open(os.path.join(root, file), 'r') as f:
                # Подсчет строк в файле
                for line in f:
                    if not is_empty_or_comment(line):
                        total_lines += 1

print('Общее количество строк: ', total_lines)

