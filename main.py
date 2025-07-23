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

# Make sure log doesn't become massive.
f = open("game.log", "r")
if not len(["" for _ in f]) > 3000: # Less than 3k lines ("" saves memory)
    pass
else:
    f.close()
    f = open("game.log", "w") # Wipe file
f.close()

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    filename="game.log",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s.%(filename)s:%(levelname)s - %(message)s",
)

logger.info("------------------------NEW SESSION------------------------")

import sys, time
from glob import glob
from typing import Optional


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
    if sys.version_info.major != 3 or sys.version_info.minor < 10:
        raise NotImplementedError("Please use Python >= 3.10")
    clear_stdout()
    check_terminal_size()
    clear_stdout()
    return None

def prompt_load_save() -> Optional[GameData]:
    save_paths: list[str] = glob("./saves/savegame_*.pkl")
    if not save_paths:
        return None    
    choice: str = input(f"{Styles.fg.lightblue}Save(s) found!\nLoad game? [y]es/[N]o{Styles.reset} ").strip().lower()
    
    match choice:
        case "y" | "yes":
            savefile_path = choose_save_file(save_paths)
            data: GameData = handle_load(savefile_path)
            return data
        case _: # If it's not an explicit yes then we assume no
            typing_print(f"{Styles.fg.lightblue}Starting a new game...{Styles.reset}")
            return None

def choose_save_file(paths: list[str]) -> str:
    for i, savefile in enumerate(paths, 1):
        stuff  = savefile.split("_") 
        # name, (day, month), (hours, minutes)
        player_name, date, time = stuff[1], (stuff[2], stuff[3]), (stuff[4], stuff[5][:-4])
        print(f"""{Styles.fg.lightgreen} 
Save #{i}
Player: {player_name}
Date: {date[0]}/{date[1]}
Time: {time[0]}:{time[1]}""")
    typing_print(f"\nPick a save file...{Styles.reset}")
    while True:
        try:
            choice = int(input())
            path_index = choice - 1 if choice > 0 else 0x9999 # If it's negative we can just cause the indexerror
            return paths[path_index]
        except (ValueError, IndexError):
            print_error("Invalid input, please select a valid number!")
        


def tutorial() -> None:
    clear_stdout()
    start_tutorial()
    clear_stdout()
    return None

def is_valid_name(name: str) -> bool:
    lowercase_letters: list[str] = [chr(i) for i in range(97, 123)]
    uppercase_letters: list[str] = [chr(i) for i in range(65, 91)]
    numbers: list[str] = [chr(i) for i in range(48, 58)]
    valid_chararacters: list[str] = uppercase_letters + lowercase_letters + numbers
   
    if not all(char in valid_chararacters for char in name) or not 0 < len(name) < 40:  
        print_error(f"Invalid name. Please use only letters and numbers, with length between 1 and 40 characters.")
        return False
    return True


def start_game() -> None:
    player_name: str = input(f"{Styles.fg.lightgreen}Enter Player Name: {Styles.reset}").strip().title()
    while not is_valid_name(player_name):
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



