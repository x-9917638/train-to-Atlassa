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


from game.game import Game
from game.core import *
from game.utils import Styles
from game.utils import clear_stdout, check_terminal_size
from game.tutorial import start_tutorial

GAME_BANNER = f"""{Styles.fg.lightblue}ooooooooooooo                     o8o                       .                        .o.           .   oooo                                        
8'   888   `8                     `"'                     .o8                       .888.        .o8   `888                                        
     888      oooo d8b  .oooo.   oooo  ooo. .oo.        .o888oo  .ooooo.           .8"888.     .o888oo  888   .oooo.    .oooo.o  .oooo.o  .oooo.   
     888      `888""8P `P  )88b  `888  `888P"Y88b         888   d88' `88b         .8' `888.      888    888  `P  )88b  d88(  "8 d88(  "8 `P  )88b  
     888       888      .oP"888   888   888   888         888   888   888        .88ooo8888.     888    888   .oP"888  `"Y88b.  `"Y88b.   .oP"888  
     888       888     d8(  888   888   888   888         888 . 888   888       .8'     `888.    888 .  888  d8(  888  o.  )88b o.  )88b d8(  888  
    o888o     d888b    `Y888""8o o888o o888o o888o        "888" `Y8bod8P'      o88o     o8888o   "888" o888o `Y888""8o 8""888P' 8""888P' `Y888""8o{Styles.reset}"""


def setup():
    try:
        # Make sure can use match-case otherwise the game won't run
        match "":
            case _: pass
    except:
        raise NotImplementedError("Please use Python >= 3.10")
    clear_stdout()
    check_terminal_size()
    clear_stdout()


def tutorial():
    start_tutorial()
    clear_stdout()


def start_game():
    player_name = input(f"{Styles.fg.lightgreen}Enter Player Name: {Styles.reset}").strip().title()
    print(GAME_BANNER)
    # insert save file check here
    game = Game(player_name)
    ProfessionChooser(game).cmdloop()
    game.cmdloop()
    

def main():
    setup()
    tutorial()
    start_game()


if __name__ == "__main__":
    main()



