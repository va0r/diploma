from colorama import init, Fore, Style

init()


def print_colored_and_boxed(message, color='LIGHTYELLOW_EX'):
    border = "═" * (len(message) + 4)
    color_code = getattr(Fore, color.upper(), Fore.LIGHTYELLOW_EX)
    print(color_code + Style.BRIGHT + f"╔{border}╗")
    print(color_code + Style.BRIGHT + "║ " + message + "   ║")
    print(color_code + Style.BRIGHT + f"╚{border}╝" + Style.RESET_ALL)
