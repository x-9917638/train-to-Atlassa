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
from game.utils.styles import Styles, colorprint
import os, subprocess

try:
    # Make sure can use match-case
    match "":
        case _: pass
except:
    raise NotImplementedError("Please use Python >=3.10.0")


def clear_stdout():
    if os.name == "posix":
        subprocess.run(['clear'])
    elif os.name == "nt":
        subprocess.run(['cls'], shell=True)
    else:
        raise NotImplementedError("Unsupported platform. How did you even get here?")

GAME_BANNER = f"""{Styles.fg.lightblue}ooooooooooooo                     o8o                       .                        .o.           .   oooo                                        
8'   888   `8                     `"'                     .o8                       .888.        .o8   `888                                        
     888      oooo d8b  .oooo.   oooo  ooo. .oo.        .o888oo  .ooooo.           .8"888.     .o888oo  888   .oooo.    .oooo.o  .oooo.o  .oooo.   
     888      `888""8P `P  )88b  `888  `888P"Y88b         888   d88' `88b         .8' `888.      888    888  `P  )88b  d88(  "8 d88(  "8 `P  )88b  
     888       888      .oP"888   888   888   888         888   888   888        .88ooo8888.     888    888   .oP"888  `"Y88b.  `"Y88b.   .oP"888  
     888       888     d8(  888   888   888   888         888 . 888   888       .8'     `888.    888 .  888  d8(  888  o.  )88b o.  )88b d8(  888  
    o888o     d888b    `Y888""8o o888o o888o o888o        "888" `Y8bod8P'      o88o     o8888o   "888" o888o `Y888""8o 8""888P' 8""888P' `Y888""8o{Styles.reset}"""


clear_stdout()
while os.get_terminal_size().columns <= 150 or os.get_terminal_size().lines <= 24:
    print(f"{Styles.fg.red}{Styles.bold}Terminal size too small \nTry maximising the window.{Styles.reset}")
    time.sleep(1)
clear_stdout()
print(GAME_BANNER)


game = Game(input(f"{Styles.fg.lightgreen}Enter Player Name: {Styles.reset}").title())
colorprint("Available Professions:", "lightgreen")
for i in Professions:
    colorprint(i.value, "lightgreen")
player_profession = input(f"{Styles.bold}{Styles.fg.lightblue}Choose a profession: {Styles.reset}").upper()
while True:
    try:
        game.player.profession = Professions[player_profession]
        break
    except KeyError:
        print_error("Invalid profession.")
        player_profession = input(f"{Styles.bold}{Styles.fg.lightblue}Choose a profession: {Styles.reset}").upper()
clear_stdout()
game.cmdloop()
# game.player.skill_hand = GENERAL_SKILLS.copy()
# game.initiate_combat(game.player.allies, test_carriage.enemies)





# test_carriage = Carriage(CarriageType.FIGHT, "Test Fight Place", 2)
# test_carriage.generate_entities()
# banana = Consumable("Banana", "A cool banana", status_effects["poison"])
# apple = Consumable("Apple", "Big red apple", status_effects["burn"])
# pear = Consumable("Pear", "A sour pear!", status_effects["shield"])
# game.player.inventory = {banana: 2, apple:7, pear: 1}
