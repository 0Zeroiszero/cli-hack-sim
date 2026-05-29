from colorama import Fore, Style, init


init(autoreset=True)


def red_text(text):
    return Fore.RED + Style.BRIGHT + str(text) + Style.RESET_ALL


def green_text(text):
    return Fore.GREEN + Style.BRIGHT + str(text) + Style.RESET_ALL


def yellow_text(text):
    return Fore.YELLOW + Style.BRIGHT + str(text) + Style.RESET_ALL


def selected_text(text):
    return Fore.GREEN + Style.BRIGHT + str(text) + Style.RESET_ALL


def side_text(text):
    return Fore.GREEN + Style.DIM + str(text) + Style.RESET_ALL