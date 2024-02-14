from colorama import init, Fore, Style

init()


def print_colored_and_boxed(message):
    # Создание рамки вокруг сообщения
    border = "═" * (len(message) + 4)
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"╔{border}╗")
    print("║ " + message + "   ║")
    print(f"╚{border}╝" + Style.RESET_ALL)
