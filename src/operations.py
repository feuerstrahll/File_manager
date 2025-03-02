import os
import shutil
import zipfile

from config.settings import WORKING_DIRECTORY

class Operations:
    def __init__(self):
        self.working_dir = os.path.abspath(WORKING_DIRECTORY)
        os.makedirs(self.working_dir, exist_ok=True)
        self.current_path = self.working_dir

    def _validate_path(self, path: str) -> str:
        abs_path = os.path.abspath(path)
        if not abs_path.startswith(self.working_dir):
            raise PermissionError("Выход за пределы рабочей директории запрещен")
        return abs_path

    def _get_relative_path(self, path: str) -> str:
        return os.path.relpath(path, self.working_dir)

    def _print_status(self, message: str, success: bool = True) -> None:
        status = "Успешно" if success else "Ошибка"
        print(f"[{status}] {message}")

    def create_folder(self, folder_name: str) -> None:
        try:
            full_path = self._validate_path(os.path.join(self.current_path, folder_name))
            os.makedirs(full_path, exist_ok=True)
            self._print_status(f"Создана папка: {folder_name}")
        except Exception as e:
            self._print_status(str(e), success=False)

    def delete_folder(self, folder_name: str) -> None:
        try:
            full_path = self._validate_path(os.path.join(self.current_path, folder_name))
            shutil.rmtree(full_path)
            self._print_status(f"Удалена папка: {folder_name}")
        except FileNotFoundError:
            self._print_status(f"Папка не найдена: {folder_name}", False)
        except Exception as e:
            self._print_status(str(e), success=False)

    def navigate(self, direction: str, target: str = None) -> None:
        try:
            if direction == "in" and target:
                new_path = self._validate_path(os.path.join(self.current_path, target))
                if os.path.isdir(new_path):
                    self.current_path = new_path
                    self._print_status(f"Переход в: {self._get_relative_path(new_path)}")
                else:
                    self._print_status(f"Папка не существует: {target}", False)
            elif direction == "up":
                parent = os.path.dirname(self.current_path)
                if parent.startswith(self.working_dir):
                    self.current_path = parent
                    self._print_status(f"Переход на уровень выше")
                else:
                    self._print_status("Достигнут корень рабочей директории", False)
        except Exception as e:
            self._print_status(str(e), success=False) 

    def create_file(self, file_name: str) -> None:
        try:
            full_path = self._validate_path(os.path.join(self.current_path, file_name))
            if os.path.exists(full_path):
                raise FileExistsError("Файл уже существует")
            open(full_path, 'a').close()
            self._print_status(f"Создан файл: {file_name}")
        except Exception as e:
            self._print_status(str(e), success=False)

    def write_to_file(self, file_name: str, content: str) -> None:
        try:
            full_path = self._validate_path(os.path.join(self.current_path, file_name))
            with open(full_path, 'a') as f:
                f.write(content + "\n")
            self._print_status(f"Записано в файл: {file_name}")
        except Exception as e:
            self._print_status(str(e), success=False)

    def read_file(self, file_name: str) -> None:
        try:
            full_path = self._validate_path(os.path.join(self.current_path, file_name))
            with open(full_path, 'r') as f:
                print(f"\nСодержимое файла {file_name}:\n{f.read()}")
        except Exception as e:
            self._print_status(str(e), success=False)

    def delete_file(self, file_name: str) -> None:
        try:
            full_path = self._validate_path(os.path.join(self.current_path, file_name))
            os.remove(full_path)
            self._print_status(f"Удален файл: {file_name}")
        except FileNotFoundError:
            self._print_status(f"Файл не найден: {file_name}", False)
        except Exception as e:
            self._print_status(str(e), success=False)

    def _file_operation(self, source: str, dest: str, operation: callable) -> None:
        try:
            src_path = self._validate_path(os.path.join(self.current_path, source))
            dest_path = self._validate_path(os.path.join(self.current_path, dest, os.path.basename(source)))
            
            if not os.path.exists(src_path):
                raise FileNotFoundError(f"Файл не найден: {source}")
                
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            operation(src_path, dest_path)
            self._print_status(f"Файл {source} -> {dest}")
        except Exception as e:
            self._print_status(str(e), success=False)

    def copy_file(self, source: str, dest: str) -> None:
        self._file_operation(source, dest, shutil.copy2)

    def move_file(self, source: str, dest: str) -> None:
        self._file_operation(source, dest, shutil.move)

    def rename_file(self, old_name: str, new_name: str) -> None:
        try:
            old_path = self._validate_path(os.path.join(self.current_path, old_name))
            new_path = self._validate_path(os.path.join(self.current_path, new_name))
            os.rename(old_path, new_path)
            self._print_status(f"Переименован: {old_name} -> {new_name}")
        except Exception as e:
            self._print_status(str(e), success=False)
    
    def zip_file_or_folder(self, source: str, archive_name: str) -> None:
        try:
            source_path = self._validate_path(os.path.join(self.current_path, source))
            archive_path = self._validate_path(os.path.join(self.current_path, archive_name))

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

            self._print_status(f"Создан архив: {archive_name}")
        except Exception as e:
            self._print_status(str(e), success=False)

    def unzip_archive(self, archive_name: str, extract_to: str) -> None:
        try:
            archive_path = self._validate_path(os.path.join(self.current_path, archive_name))
            extract_path = self._validate_path(os.path.join(self.current_path, extract_to))

            if not os.path.exists(archive_path):
                raise FileNotFoundError(f"Архив не найден: {archive_name}")

            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(extract_path)

            self._print_status(f"Архив {archive_name} разархивирован в {extract_to}")
        except Exception as e:
            self._print_status(str(e), success=False)