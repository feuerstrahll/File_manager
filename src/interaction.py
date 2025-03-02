from src.operations import Operations
from colorama import Fore, Style

class FileManager(Operations):  
    def __init__(self):
        super().__init__()
        self.commands = [
            ("mkdir <папка>", "Создать папку"),
            ("rmdir <папка>", "Удалить папка"),
            ("nav in <папка>", "Войти в папку"),
            ("nav up", "Выйти из папки"),
            ("touch <файл>", "Создать файл"),
            ("write <файл> <текст>", "Записать в файл"),
            ("cat <файл>", "Просмотреть файл"),
            ("rm <файл>", "Удалить файл"),
            ("cp <файл> <папка>", "Копировать файл"),
            ("mv <файл> <папка>", "Переместить файл"),
            ("rename <старое> <новое>", "Переименовать файл"),
            ("exit", "Выход"),
            ("zip <файл/папка> <архив>", "Создать ZIP-архив"),
            ("unzip <архив> <папка>", "Разархивировать ZIP-архив")
        ]


    def _show_help(self) -> None:
        print(f"\n{Fore.GREEN}Доступные команды:{Style.RESET_ALL}")
        for cmd, desc in self.commands:
            print(f"  {Fore.CYAN}{cmd.ljust(25)}{Style.RESET_ALL} {desc}") # #  "left justify" (выравнивание по левому краю). 25 — это общая длина, до которой будет расширена строка

    def run(self) -> None:
        print(f"\nФайловый менеджер рабочая директория: {self._get_relative_path(self.working_dir)}")
        self._show_help()
        while True:
            try:
                print(f"\nТекущий путь: {Fore.BLUE}{self.current_path}{Style.RESET_ALL}")
                command = input(">>> ").strip().split()

                if not command:
                    continue

                action = command[0].lower()
                args = command[1:]

                if action == "exit":
                    break
                elif action == "help":
                    self._show_help()
                elif action == "mkdir" and len(args) == 1:
                    self.create_folder(args[0])
                elif action == "rmdir" and len(args) == 1:
                    self.delete_folder(args[0])
                elif action == "nav" and len(args) >= 1:
                    self.navigate(args[0], args[1] if len(args) > 1 else None)
                elif action == "touch" and len(args) == 1:
                    self.create_file(args[0])
                elif action == "write" and len(args) >= 2:
                    self.write_to_file(args[0], ' '.join(args[1:]))
                elif action == "cat" and len(args) == 1:
                    self.read_file(args[0])
                elif action == "rm" and len(args) == 1:
                    self.delete_file(args[0])
                elif action == "cp" and len(args) == 2:
                    self.copy_file(args[0], args[1])
                elif action == "mv" and len(args) == 2:
                    self.move_file(args[0], args[1])
                elif action == "rename" and len(args) == 2:
                    self.rename_file(args[0], args[1])
                elif action == "zip" and len(args) == 2:
                    self.zip_file_or_folder(args[0], args[1])
                elif action == "unzip" and len(args) == 2:
                    self.unzip_archive(args[0], args[1])
                else:
                    print("Неверная команда. Введите 'help' для списка команд")

            except Exception as e:
                self._print_status(f"Ошибка выполнения: {str(e)}", success=False)
    