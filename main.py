#! /usr/bin/env python

#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU Affero General Public License as published
#       by the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU Affero General Public License for more details.
#
#       You should have received a copy of the GNU Affero General Public License
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    filename="game.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s.%(filename)s:%(levelname)s - %(message)s",
)

import os
from typing import Optional
import time


from game.game import Game, GameData, GameCommandHandler
from game.core.save_handler import handle_load
from game.core.profession_chooser import ProfessionChooser
from game.utils import print_error, typing_print
from game.utils import Styles
from game.utils import clear_stdout, check_terminal_size
from game.tutorial import start_tutorial




GAME_BANNER = fr"""{Styles.bold}{Styles.fg.magenta}ooooooooooooo                     o8o                       .                        .o.           .   oooo
8'   888   `8                     `"'                     .o8                       .888.        .o8   `888                                        
     888      oooo d8b  .oooo.   oooo  ooo. .oo.        .o888oo  .ooooo.           .8"888.     .o888oo  888   .oooo.    .oooo.o  .oooo.o  .oooo.   
     888      `888""8P `P  )88b  `888  `888P"Y88b         888   d88' `88b         .8' `888.      888    888  `P  )88b  d88(  "8 d88(  "8 `P  )88b  
     888       888      .oP"888   888   888   888         888   888   888        .88ooo8888.     888    888   .oP"888  `"Y88b.  `"Y88b.   .oP"888  
     888       888     d8(  888   888   888   888         888 . 888   888       .8'     `888.    888 .  888  d8(  888  o.  )88b o.  )88b d8(  888  
    o888o     d888b    `Y888""8o o888o o888o o888o        "888" `Y8bod8P'      o88o     o8888o   "888" o888o `Y888""8o 8""888P' 8""888P' `Y888""8o{Styles.reset}"""


def setup() -> None:
    try:
        # Make sure can use match-case otherwise the game won't run
        match "":
            case _: pass
    except:
        raise NotImplementedError("Please use Python >= 3.10")
    clear_stdout()
    check_terminal_size()
    clear_stdout()
    return None

def prompt_load_save() -> Optional[GameData]:
    if not os.path.exists("./saves/savegame.pkl"):
        return None    
    choice: str = input(f"{Styles.fg.lightblue}Save found!\nLoad game? [y]es/[N]o{Styles.reset} ").strip().lower()
    
    match choice:
        case "y" | "yes":
            data: GameData = handle_load()
            return data
        case _: # If it's not an explicit yes then we assume no
            typing_print(f"{Styles.fg.lightblue}Starting a new game...{Styles.reset}")
            return None


def tutorial() -> None:
    clear_stdout()
    start_tutorial()
    clear_stdout()
    return None

def check_name(name:str) -> bool:
    alphabet: list[str] = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
   
    if not all(char in alphabet or char.isspace() for char in name) and 0 < len(name) < 40:  
        print_error(f"{Styles.fg.red}Invalid name: {name}. Please use only letters and spaces, and please keep it between 1 and 40 characters.{Styles.reset}")
        return False
    return True


def start_game() -> None:
    player_name: str = input(f"{Styles.fg.lightgreen}Enter Player Name: {Styles.reset}").strip().title()
    while not check_name(player_name):
        player_name = input(f"{Styles.fg.lightgreen}Enter Player Name: {Styles.reset}").strip().title()

    print(GAME_BANNER)

    game: Game = Game(player_name)
    ProfessionChooser(game).cmdloop()
    GameCommandHandler(game).cmdloop()
    
    return None
    

def main():
    setup()
    save_data: Optional[GameData] = prompt_load_save()
    time.sleep(0.3)
    if save_data:
        game: Game = Game("", data=save_data)
        GameCommandHandler(game).cmdloop()
    else:
        tutorial()
        start_game()


if __name__ == "__main__":
    main()



