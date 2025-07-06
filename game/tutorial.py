#
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

from .game import Game
from .core.combat import CombatSystem
from .core.entities import Player, Enemy, Ally
from .core.skills import Skill
from .core.status_effects import status_effects

from .utils import *

import os
if os.name == "nt":
    from msvcrt import getch
    ESC_KEY = b'\x1b'
else:
    try:
        from getch import getch
        ESC_KEY = '\x1b'
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"getch is not installed.\nPlease run{Styles.bold} pip install getch{Styles.reset}")



def start_tutorial():
    """Introduce the player to the game."""

    print(r"""__        __   _                             _          _____          _         _             _   _   _                     _ 
\ \      / /__| | ___ ___  _ __ ___   ___   | |_ ___   |_   _| __ __ _(_)_ __   | |_ ___      / \ | |_| | __ _ ___ ___  __ _| |
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \  | __/ _ \    | || '__/ _` | | '_ \  | __/ _ \    / _ \| __| |/ _` / __/ __|/ _` | |
  \ V  V /  __/ | (_| (_) | | | | | |  __/  | || (_) |   | || | | (_| | | | | | | || (_) |  / ___ \ |_| | (_| \__ \__ \ (_| |_|
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|   \__\___/    |_||_|  \__,_|_|_| |_|  \__\___/  /_/   \_\__|_|\__,_|___/___/\__,_(_)""")
    
    if getch() == ESC_KEY: return
    if sys.platform == "win32":
        print("Note: autocompletions are not available on Windows.\nPress any key to continue...")
    else:
        print("Autocompletions are available with [TAB]!\nPress [ESC] to skip the tutorial at any time!\nPress any key to continue...")

    
    if getch() == ESC_KEY: return
    typing_print("After saving the Grand City of Citadel, you, the Hero, board the Train to Atlassa...", delay=0.01)
 
    if getch() == ESC_KEY: return
    typing_print("Little do you know, the remnant of the monster invasion is waiting...", delay=0.01)
    
    if getch() == ESC_KEY: return
    typing_print("A tragic fate awaits those of Atlassa if you fail.", delay=0.01)

    if getch() == ESC_KEY: return
    typing_print("Can you save your faithful allies?", delay=0.01)

    if getch() == ESC_KEY: return
    typing_print("Can you retake the train from these vile monsters and save Atlassa?", delay=0.01)

    if getch() == ESC_KEY: return
    typing_print("Train to Atlassa is a turn-based RPG with a focus on randomness and strategic management.", delay=0.01)

    if getch() == ESC_KEY: return
    typing_print("Choose your profession and gain unique skills every playthrough!", delay=0.01)

    if getch() == ESC_KEY: return
    typing_print("Lets test your skills with a small tutorial battle.\nThis is your last chance to skip the tutorial: [ESC]", delay=0.01)
    if getch() == ESC_KEY: return

    tutor_battle = TutorialCombat()
    tutor_battle.start_combat()

class TutorialCombat(CombatSystem):
    """A combat system for the tutorial battle."""
    def __init__(self):
        tutorial_player = Player("Hero")
        tutorial_player.level = 100
        tutorial_player.attack = 5 # Don't one shot the enmy
        tutorial_player.mana = 10000
        tutorial_player.max_mana = 10000
        tutorial_player.health = 10000
        tutorial_player.max_health = 10000
        tutorial_player.skills = [Skill("Mighty Slash", "A powerful slash that cleaves monsters with ease.", 20, 20, SkillTarget.SINGLE_ENEMY, effect=status_effects["poison"])]
        tutorial_ally = Ally("Blarj", "The System Guide", 1, Professions.MAGE)
        tutorial_player.add_ally(tutorial_ally)
        tutorial_ally.skills = [(Skill("Smite", "", 100000000, 0, SkillTarget.ALL_ENEMIES))]
        tutorial_enemy = [Enemy("Goblin", "A typical goblin, weak but numerous.", 1, 10, 1)]
        super().__init__(tutorial_player, tutorial_player.allies, tutorial_enemy)

    def postcmd(self, stop, line):
        if self.triggered_help: # If we got here because of help or error, skip the rest of postcmd.
            self.triggered_help = False
            return False
        
        typing_print("After your turn, the enemies attack.", delay=0.01)
        self.enemy_turn()
        typing_print("Press any key to continue...\n", delay=0.01)
        getch()

        typing_print("After the enemies' turn, your allies attack.", delay=0.01)
        self.ally_turn()
        typing_print("Press any key to continue...\n", delay=0.01)
        getch()

        typing_print("And now it all repeats!\nCongratulations! Now you've finished the tutorial!", delay=0.01)
        getch()

        return True

    def start_combat(self):
        typing_print("It's your turn first!", delay=0.01)
        typing_print("Each turn, you randomly draw one skill that can be used from your \"deck\" of skills", delay=0.01)
        typing_print("This turn, lets attack!", delay=0.01)
        getch()
        return super().start_combat()
    
    # don't want the player doing anything other than atack in tutorial
    def do_items(self, arg):
        print_error("Woah there! You don't have any items right now. You need to attack!")
        getch()
        super().do_attack(arg) # Force them to attack
    
    def do_retreat(self, arg):
        print_error("Woah there! You can't run from this! You need to attack!")
        getch()
        return super().do_attack(arg)
    
    def do_rest(self, arg):
        print_error("Woah there! You aren't tired at all... Why not attack instead?")
        getch()
        return super().do_attack(arg)


if __name__ == "__main__":
    start_tutorial()