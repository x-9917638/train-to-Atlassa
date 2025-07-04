from enum import Enum
import sys, time, subprocess, os
import cmd

def typing_print(text, delay: float=0.05):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    
def typing_input(text, delay: float=0.05):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    value = input()  
    return value

class CarriageType(Enum):
    SAFE = "Safe Place"
    REST = "Resting Place"
    FIGHT = "Combat Area"
    CHALLENGE = "Challenge Area"
    BOSS = "Boss Room"

class SkillTarget(Enum):
    SELF = "Self"
    SINGLE_ENEMY = "Single Enemy"
    ALL_ENEMIES = "All Enemies"
    SINGLE_ALLY = "Single Ally"
    ALL_ALLIES = "All Allies"

class Professions(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    PRIEST = "Priest"

class CombatCommand(Enum):
    FIGHT = "attack"
    ITEM = "items"
    REST = "rest"
    RUN = "retreat"

class GeneralCommand(Enum):
    NEXT = "next"
    BACK = "back"
    BAG = ["inv", "inventory"] # Player can type shorthand 'inv' or 'inventory'
    SEARCH = "search"


class Styles:
    """
    Provides text styling via ANSI escape codes.
    Reset all styles with styles.reset.
    """

    reset = "\033[0m"
    bold = "\033[01m"
    dimmed = "\033[02m"
    italics = "\033[03m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        yellow = "\033[33m"
        blue = "\033[34m"
        magenta = "\033[35m"
        cyan = "\033[36m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        yellow = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
    
    
def colorprint(to_print:str, fgcolor: str, bgcolor: str = "", sep: str = "\n"):
    # Apply modifications, print text, then reset.
    print(f"{getattr(Styles.fg, fgcolor)}{getattr(Styles.bg, bgcolor, '')}{to_print}{Styles.reset}", sep=sep)


def print_game_msg(to_print:str):
    # Print a light blue string - for standard system messages or prompts
    print(f"\033[94m{to_print}\033[0m")


def print_error(to_print:str):
    # Print a red colored string - for error messages on invalid actions from the user, etc.
    print(f"\033[31m{to_print}\033[0m")

def clear_stdout():
    if os.name == "posix":
        subprocess.run(['clear'])
    elif os.name == "nt":
        subprocess.run(['cls'], shell=True)
    else:
        raise NotImplementedError("Unsupported platform. How did you even get here?")


def check_terminal_size():
    try:
        while os.get_terminal_size().columns <= 150 or os.get_terminal_size().lines <= 24:
            print(f"{Styles.fg.red}{Styles.bold}Terminal size too small \nTry maximising the window.{Styles.reset}")
            time.sleep(1)
    except OSError:
        raise OSError(f"{Styles.fg.red}{Styles.bold}Please use your dedicated terminal to run this game.{Styles.reset}")


class BaseCommandHandler(cmd.Cmd):
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        clear_stdout()
        print_error('Unknown command: %s\n'%line)
    
    def emptyline(self):
        self.do_help("") # Don't accept empty line = last cmd entered
    

        
