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

from .data.effects import STATUS_EFFECTS

from .utils import clear_stdout
from .utils import Styles, typing_print, print_error
from .utils import SkillTarget, Professions

import logging

logger = logging.getLogger(__name__)

import sys
# ESC_KEY: Keycode for the escape key
if sys.platform == "win32":
    logging.debug("Windows detected, using msvcrt.getch().")
    from msvcrt import getch
    ESC_KEY: bytes = b'\x1b'
else:
    try:
        logging.debug("Unix-like detected, using getch.getch.")
        from getch import getch
        ESC_KEY: str = '\x1b'
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f"getch is not installed.\nPlease run{Styles.bold} pip install getch{Styles.reset}")



def start_tutorial():
    """Introduce the player to the game."""

    typing_print("Press [ESC] to skip the tutorial at any time!")
    typing_print("Press any key to continue...")
    if getch() == ESC_KEY: return

    logging.info("Starting tutorial...")
    print(r"""__        __   _                             _          _____          _         _             _   _   _                     _ 
\ \      / /__| | ___ ___  _ __ ___   ___   | |_ ___   |_   _| __ __ _(_)_ __   | |_ ___      / \ | |_| | __ _ ___ ___  __ _| |
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \  | __/ _ \    | || '__/ _` | | '_ \  | __/ _ \    / _ \| __| |/ _` / __/ __|/ _` | |
  \ V  V /  __/ | (_| (_) | | | | | |  __/  | || (_) |   | || | | (_| | | | | | | || (_) |  / ___ \ |_| | (_| \__ \__ \ (_| |_|
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|   \__\___/    |_||_|  \__,_|_|_| |_|  \__\___/  /_/   \_\__|_|\__,_|___/___/\__,_(_)""")
    
    if getch() == ESC_KEY: return
    if sys.platform == "win32":
        typing_print("Note: autocompletions are not available on Windows.")
    else:
        typing_print("Autocompletions are available with [TAB]!")
    
    if getch() == ESC_KEY: return
    typing_print("After saving the Grand City of Citadel, you, the Hero, board the Train to Atlassa...")
 
    if getch() == ESC_KEY: return
    typing_print("Little do you know, the remnant of the monster invasion is waiting...")
    
    if getch() == ESC_KEY: return
    typing_print("A tragic fate awaits those of Atlassa if you fail.")

    if getch() == ESC_KEY: return
    typing_print("Can you save your faithful allies?")

    if getch() == ESC_KEY: return
    typing_print("Can you retake the train from these vile monsters and save Atlassa?")

    if getch() == ESC_KEY: return
    typing_print("Train to Atlassa is a turn-based RPG with a focus on randomness and strategic management.")

    if getch() == ESC_KEY: return
    typing_print("Choose your profession and gain unique skills every playthrough!")

    if getch() == ESC_KEY: return
    typing_print("Lets test your skills with a small tutorial battle.\nThis is your last chance to skip the tutorial: [ESC]")
    if getch() == ESC_KEY: return

    logging.info("Starting tutorial combat.")
    tutor_battle: TutorialCombat = TutorialCombat()
    tutor_battle.start_combat()
    logging.info("Tutorial combat finished.")

class TutorialCombat(CombatSystem):
    """A combat system for the tutorial battle."""
    def __init__(self):
        # Hardcode stats for tutorial
        tutorial_player: Player = Player("Hero")
        tutorial_player.level = 100
        tutorial_player.attack = 5 # Don't one shot the enmy
        tutorial_player.mana = 10000
        tutorial_player.max_mana = 10000
        tutorial_player.health = 10000
        tutorial_player.max_health = 10000
        tutorial_player.skill_deck = [Skill("Mighty Slash", "A powerful slash that cleaves monsters with ease.", 20, 20, SkillTarget.SINGLE_ENEMY, effect=STATUS_EFFECTS["poison"])]
        
        # Hardcode ally for tutorial
        tutorial_ally: Ally = Ally(name="Blarj",description="The System Guide", level=1, section=1, profession=Professions.MAGE)
        tutorial_player.add_ally(tutorial_ally)
        tutorial_ally.skill_deck = [(Skill("Delete", "", 9999999999999, 0, SkillTarget.ALL_ENEMIES))]

        # Hardcode enemy for tutorial
        tutorial_enemy: list[Enemy] = [Enemy(name="Goblin",description="A typical goblin, weak but numerous.", level=1, section=1, exp_amt=10, num_skills=1)]

        super().__init__(tutorial_player, tutorial_player.allies, tutorial_enemy)

    def postcmd(self, stop, line) -> bool:
        if self.triggered_help: # If we got here because of help or error, skip the rest of postcmd.
            self.triggered_help = False
            return False
        
        typing_print("After your turn, the enemies attack.")
        self.enemy_turn()
        typing_print("Press any key to continue...\n")
        getch()

        typing_print("After the enemies' turn, your allies attack.")
        self.ally_turn()
        typing_print("Press any key to continue...\n")
        getch()

        typing_print("Congratulations! Now you've finished the tutorial!")
        getch()

        return True
    
    def _player_turn_setup(self) -> None:
        clear_stdout()
        typing_print("Train to Atlassa implements turn based combat. Each turn, the player chooses their action first, then the enemies attack, then finally, allies.")
        typing_print("During combat, you can attack, use items, rest, or retreat.")
        typing_print("Each turn, a random skill is drawn and placed into the players skill hand. If you choose to attack, you can pick and use a skill from your hand.")
        typing_print("""You can also: 
    - Use consumable items to gain an advantage
    - Rest to heal 10% of max health and 10% of max mana.
    - Retreat to run away from combat.""")
        typing_print("Picking any of these options will end your turn.")
        typing_print("Note that you have an ally: Blarj.")
        typing_print("Allies can attack and help you in combat, but you may only have 2 allies at a time.")
        typing_print("This turn, lets attack!")
        getch()
        super()._player_turn_setup()
        return None

    
    # don't want the player doing anything other than atack in tutorial
    def do_items(self, arg) -> None:
        print_error("Woah there! You don't have any items right now. You need to attack!")
        getch()
        super().do_attack(arg) # Force them to attack
        return None
    
    def do_retreat(self, arg) -> None:
        print_error("Woah there! You can't run from this! You need to attack!")
        getch()
        super().do_attack(arg)
        return None
    
    def do_rest(self, arg) -> None:
        print_error("Woah there! You aren't tired at all... Why not attack instead?")
        getch()
        super().do_attack(arg)
        return None


    
