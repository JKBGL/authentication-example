from dataclasses import dataclass
import colorama, datetime

@dataclass
class Colors:
    BLACK = colorama.Fore.BLACK
    GRAY = colorama.Fore.LIGHTBLACK_EX
    YELLOW = colorama.Fore.YELLOW
    GREEN = colorama.Fore.GREEN
    LIGHT_GREEN = colorama.Fore.LIGHTGREEN_EX
    BLUE = colorama.Fore.BLUE
    CYAN = colorama.Fore.CYAN
    RED = colorama.Fore.RED
    GOLD = colorama.Fore.LIGHTYELLOW_EX
    LIGHT_RED = colorama.Fore.LIGHTRED_EX
    LIGHT_MAGENTA = LIGHT_PURPLE = colorama.Fore.LIGHTMAGENTA_EX
    MAGENTA = PURPLE = colorama.Fore.MAGENTA
    DARK_BLUE = colorama.Fore.LIGHTBLUE_EX
    WHITE = colorama.Fore.WHITE
    RESET = colorama.Style.RESET_ALL

Color = Colors

def __timestamp():
    time = "{:%H:%M:%S}".format(datetime.datetime.now())
    formatted_time = f"{Color.WHITE}[{Color.CYAN}{time}{Color.WHITE}]{Color.RESET}"
    return formatted_time

def __log_type(type):
    rest = {
        0: ("INFO", Color.LIGHT_GREEN),
        1: ("WARNING", Color.YELLOW),
        2: ("ERROR", Color.RED),
    }[type]
        
    return f"{Color.WHITE}[{Color.GREEN}{rest[1]}{rest[0]}{Color.WHITE}]{Color.RESET}"
        

def __colored_print(message : str, color : Color = None, l_type : int = 0):
    if color:
        print(f"{__timestamp()} {__log_type(l_type)} {color}{message}{Color.RESET}")
    else:
        print(f"{__timestamp()} {__log_type(l_type)} {Color.WHITE}{message}")

def log(message, color = None):
   __colored_print(message, color, 0)
        
def warn(message, color = None):
    __colored_print(message, color, 1)
    
def err(message, color = None):
    __colored_print(message, color, 2)

info = log
warning = warn
error = err
