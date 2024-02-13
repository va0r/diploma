import os


def print_directory_structure(directory, gitignore_rules, indent=0, file=None):
    if file is None:
        file = open("directory_structure.txt", "w", encoding="utf-8")
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            if not any(rule in os.path.join(directory, item) for rule in gitignore_rules):
                file.write("    " * indent + f"📁 {item}\n")
                print_directory_structure(os.path.join(directory, item), gitignore_rules, indent + 1, file)
        else:
            if not any(rule in os.path.join(directory, item) for rule in gitignore_rules):
                file.write("    " * indent + f"📄 {item}\n")

    if indent == 0:
        file.close()


# Укажите путь к каталогу, структуру которого вы хотите вывести
directory_path = "../"
gitignore_path = "../.gitignore"

# Парсим файл .gitignore
with open(gitignore_path, 'r') as f:
    gitignore_rules = f.read().splitlines()

print_directory_structure(directory_path, gitignore_rules)
print("Структура приложения успешно записана в файл 'directory_structure.txt'")
