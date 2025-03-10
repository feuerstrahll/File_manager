import os

# ".." означает переход на одну директорию выше. Таким образом, os.path.join(os.path.dirname(__file__), "..") 
# преобразует путь в /project (корень проекта). Это нужно, чтобы рабочая директория data создавалась в корне проекта, а не внутри папки config.
# PROJECT_DIRECTORY теперь указывает на ..\File_manager_ССиП\
PROJECT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) # поднимаемся на 2 уровня вверх

# WORKING_DIRECTORY указывает на ..\File_manager_ССиП\data
WORKING_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "data")

# Создаем папку data, если она не существует
os.makedirs(WORKING_DIRECTORY, exist_ok=True)

print(f"Корневая папка проекта: {PROJECT_DIRECTORY}")
print(f"Рабочая папка: {WORKING_DIRECTORY}")