import os
import shutil
import zipfile

from src.config.settings import WORKING_DIRECTORY

class Operations:
    def __init__(self):
        """
        Инициализация рабочей директории.
        Если директория не существует, она будет создана.
        """
        self.working_dir = os.path.abspath(WORKING_DIRECTORY)
        os.makedirs(self.working_dir, exist_ok=True)
        self.current_path = self.working_dir

    def validate_path(self, path: str) -> str:
        """
        Проверяет, что путь находится внутри рабочей директории.
        Если путь выходит за пределы рабочей директории, выбрасывает исключение.
        """
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(self.working_dir):
            raise PermissionError("Выход за пределы рабочей директории запрещен")
        return abs_path

    def get_relative_path(self, path: str) -> str:
        """
        Возвращает относительный путь относительно рабочей директории.
        """
        return os.path.relpath(path, self.working_dir)

    def create_folder(self, folder_name: str) -> None:
        """
        Создает папку в текущей директории
        """
        try:
            full_path = self.validate_path(os.path.join(self.current_path, folder_name))
            os.makedirs(full_path, exist_ok=True)
            print(f"Создана папка: {folder_name}")
        except Exception as e:
            print("Ошибка при создании папки: " + str(e))

    def delete_folder(self, folder_name: str) -> None:
        """
        Удаляет папку в текущей директории 
        """
        try:
            full_path = self.validate_path(os.path.join(self.current_path, folder_name))
            shutil.rmtree(full_path)
            print(f"Удалена папка: {folder_name}")
        except FileNotFoundError:
            print(f"Папка не найдена: {folder_name}")
        except Exception as e:
            print(str(e))
            
    def navigate(self, direction: str, target: str = None) -> None:
        try:
            if direction == "in" and target:
                new_path = self.validate_path(os.path.join(self.current_path, target))
                if os.path.isdir(new_path):
                    self.current_path = new_path
                    print(f"Переход в: {self.get_relative_path(new_path)}")
                else:
                    print(f"Папка не существует: {target}")
            elif direction == "up":
                parent = os.path.dirname(self.current_path)
                if parent.startswith(self.working_dir):
                    self.current_path = parent
                    print(f"Переход на уровень выше")
                else:
                    print("Достигнут корень рабочей директории")
        except Exception as e:
            print(str(e)) 

    def create_file(self, file_name: str) -> None:
        try:
            full_path = self.validate_path(os.path.join(self.current_path, file_name))
            if os.path.exists(full_path):
                raise FileExistsError("Файл уже существует")
            open(full_path, 'a').close()
            print(f"Создан файл: {file_name}")
        except Exception as e:
            print(str(e))

    def delete_file(self, file_name: str) -> None:
        """
        Удаляет файл в текущей директории или по указанному пути
        """
        try:
            full_path = self.validate_path(os.path.join(self.current_path, file_name))
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"Файл не найден: {file_name}")
            
            os.remove(full_path)
            print(f"Удален файл: {file_name}")
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
        except PermissionError as e:
            print(f"Ошибка доступа: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def write_to_file(self, file_name: str, content: str) -> None:
        try:
            full_path = self.validate_path(os.path.join(self.current_path, file_name))
            with open(full_path, 'a') as f:
                f.write(content + "\n")
            print(f"Записано в файл: {file_name}")
        except Exception as e:
            print(str(e))

    def read_file(self, file_name: str) -> None:
        try:
            full_path = self.validate_path(os.path.join(self.current_path, file_name))
            with open(full_path, 'r') as f:
                print(f"\nСодержимое файла {file_name}:\n{f.read()}")
        except Exception as e:
            print(str(e))

    def file_operation(self, source: str, dest: str, operation: callable) -> None:
        """
        Общая функция для операций с файлами (копирование, перемещение).
        dest должна существовать, иначе будет вызвано исключение.
        """
        try:
            # Проверяем и нормализуем пути
            src_path = self.validate_path(os.path.join(self.current_path, source))
            dest_path = self.validate_path(os.path.join(self.current_path, dest, os.path.basename(source)))

            # Проверяем, существует ли исходный файл/директория
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Файл или директория не найдены: {source}")

            # Проверяем, существует ли целевая директория
            dest_dir = os.path.dirname(dest_path) if os.path.basename(dest_path) else dest_path
            if not os.path.isdir(dest_dir):
                raise FileNotFoundError(f"Целевая директория не существует: {dest}")

            # Выполняем операцию (копирование или перемещение)
            operation(src_path, dest_path)
            print(f"Файл {source} -> {dest}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def find_dest_folders(self, dest: str) -> list[str]:
        """
        Рекурсивно ищет все папки с именем dest, начиная с корневого пути.
        Возвращает список полных путей к найденным папкам.
        """
        dest_folders = []
        for root, dirs, files in os.walk(self.working_dir):
            if dest in dirs:
                dest_folders.append(os.path.join(root, dest))
        return dest_folders

    def copy_file(self, source: str, dest: str) -> None:
        """
        Копирует файл в папку dest. Если найдено несколько папок с именем dest,
        предлагает пользователю выбрать одну из них.
        """
        try:
            # Проверяем и нормализуем путь к исходному файлу
            src_path = self.validate_path(os.path.join(self.current_path, source))
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Файл или директория не найдены: {source}")

            # Ищем все папки с именем dest
            dest_folders = self.find_dest_folders(dest)
            if not dest_folders:
                raise FileNotFoundError(f"Папка с именем {dest} не найдена")

            # Если найдено несколько папок, предлагаем выбрать одну
            if len(dest_folders) > 1:
                print(f"Найдено несколько папок с именем {dest}:")
                for i, folder in enumerate(dest_folders, 1):
                    print(f"{i}. {folder}")
                choice = int(input("Выберите номер папки: ")) - 1
                if choice < 0 or choice >= len(dest_folders):
                    raise ValueError("Неверный выбор")
                dest_folder = dest_folders[choice]
            else:
                dest_folder = dest_folders[0]

            # Формируем полный путь к целевому файлу
            dest_path = os.path.join(dest_folder, os.path.basename(source))

            # Копируем файл
            shutil.copy2(src_path, dest_path)
            print(f"Файл {source} скопирован в {dest_folder}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def move_file(self, source: str, dest: str) -> None:
        """
        Перемещает файл в папку dest. Если найдено несколько папок с именем dest,
        предлагает пользователю выбрать одну из них
        """
        try:
            # Проверяем и нормализуем путь к исходному файлу
            src_path = self.validate_path(os.path.join(self.current_path, source))
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Файл или директория не найдены: {source}")

            # Ищем все папки с именем dest
            dest_folders = self.find_dest_folders(dest)
            if not dest_folders:
                raise FileNotFoundError(f"Папка с именем {dest} не найдена")

            # Если найдено несколько папок, предлагаем выбрать одну
            if len(dest_folders) > 1:
                print(f"Найдено несколько папок с именем {dest}:")
                for i, folder in enumerate(dest_folders, 1):
                    print(f"{i}. {folder}")
                choice = int(input("Выберите номер папки: ")) - 1
                if choice < 0 or choice >= len(dest_folders):
                    raise ValueError("Неверный выбор")
                dest_folder = dest_folders[choice]
            else:
                dest_folder = dest_folders[0]

            # Формируем полный путь к целевому файлу
            dest_path = os.path.join(dest_folder, os.path.basename(source))

            shutil.move(src_path, dest_path)
            print(f"Файл {source} перемещен в {dest_folder}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def rename_file(self, old_name: str, new_name: str) -> None:
        try:
            old_path = self.validate_path(os.path.join(self.current_path, old_name))
            new_path = self.validate_path(os.path.join(self.current_path, new_name))
            os.rename(old_path, new_path)
            print(f"Переименован: {old_name} -> {new_name}")
        except Exception as e:
            print(str(e))
    
    def zip_file_or_folder(self, source: str, archive_name: str) -> None:
        try:
            source_path = self.validate_path(os.path.join(self.current_path, source))
            archive_path = self.validate_path(os.path.join(self.current_path, archive_name))

            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Файл или папка не найдены: {source}")

            with zipfile.ZipFile(archive_path, 'w') as zipf:
                if os.path.isdir(source_path):
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=source_path)
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(source_path, os.path.basename(source_path))

            print(f"Создан архив: {archive_name}")
        except Exception as e:
            print(str(e))

    def unzip_archive(self, archive_name: str, extract_to: str) -> None:
        try:
            archive_path = self.validate_path(os.path.join(self.current_path, archive_name))
            extract_path = self.validate_path(os.path.join(self.current_path, extract_to))

            if not os.path.exists(archive_path):
                raise FileNotFoundError(f"Архив не найден: {archive_name}")

            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(extract_path)

            print(f"Архив {archive_name} разархивирован в {extract_to}")
        except Exception as e:
            print(str(e))

    def list_files(self):
        for root, dirs, files in os.walk(self.current_path):
            for file in files:
                print(os.path.join(root, file))