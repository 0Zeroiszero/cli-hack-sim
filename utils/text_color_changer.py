# TODO: Kita coba gunakan RICH

from colorama import Fore, Style, Back, init

init(autoreset=True)


def red_text(text) -> str:
    return Fore.RED + Style.BRIGHT + str(text) + Style.RESET_ALL


def green_text(text) -> str:
    return Fore.GREEN + Style.BRIGHT + str(text) + Style.RESET_ALL


def yellow_text(text) -> str:
    return Fore.YELLOW + Style.BRIGHT + str(text) + Style.RESET_ALL


def selected_text(text) -> str:
    return Fore.GREEN + Style.BRIGHT + str(text) + Style.RESET_ALL


def side_text(text) -> str:
    return Fore.GREEN + Style.DIM + str(text) + Style.RESET_ALL


def gradient_background_text(
    value: int | float, *, values: list[int | float], text: str | None = None
) -> str:
    if text is None:
        text = str(value)

    if not values:
        return str(text)

    max_value = max(values)
    min_value = min(values)

    if max_value == min_value:
        return Back.GREEN + Fore.WHITE + Style.BRIGHT + str(text) + Style.RESET_ALL

    ratio = (value - min_value) / (max_value - min_value)

    if ratio >= 0.80:
        color = Back.GREEN + Fore.WHITE + Style.BRIGHT
    elif ratio >= 0.60:
        color = Back.GREEN + Fore.BLACK
    elif ratio >= 0.40:
        color = Back.YELLOW + Fore.BLACK + Style.BRIGHT
    elif ratio >= 0.20:
        color = Back.RED + Fore.WHITE
    else:
        color = Back.RED + Fore.WHITE + Style.BRIGHT

    return color + str(text) + Style.RESET_ALL
