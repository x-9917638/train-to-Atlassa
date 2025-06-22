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
