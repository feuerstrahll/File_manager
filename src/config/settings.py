import os

# ".." означает переход на одну директорию выше. Таким образом, os.path.join(os.path.dirname(__file__), "..") 
# преобразует путь в /project (корень проекта). Это нужно, чтобы рабочая директория data создавалась в корне проекта, а не внутри папки config.
PROJECT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKING_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "data")