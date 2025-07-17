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

from ..utils import SkillTarget, Professions
from ..utils import Styles, colorprint, print_error, print_game_msg, typing_print
from ..utils import BaseCommandHandler
from ..utils import clear_stdout

from .items import Consumable

import os, logging
import time
import random as rand

logger = logging.getLogger(__name__)

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .entities import Entity, Player, Ally, Enemy
    from .skills import Skill
    from .items import Item


RETREAT_FAILURE_MESSAGES = [
    "You attempt a heroic leap backwards ... only to get your cloak caught on a discarded spear. So much for a grand exit.",
    "You try to cast 'Flee Like the Wind', but mispronounce it as 'Kneel Like the Twig' and faceplant instead.",
    "A valiant retreat! Or it would be, if you hadn't backed straight into a wall. Oops.",
    "You sprint away — directly into the arms of a very confused ogre who was just trying to take a nap.",
    "Your dramatic exit is ruined when an unseen fairy trips you with an invisible string. Cheeky little sprites!",
    "You yell 'Tactical withdrawal!' but your legs betray you, choosing this moment to remember they're made of jelly.",
    "You try to vanish in a puff of smoke ... but forgot to buy smoke pellets. Now you're just waving your arms awkwardly.",
    "You attempt to roll away like a rogue, but you land so loudly it attracts MORE enemies.",
    "You try to teleport but only succeed in swapping places with the enemy. This is ... not better.",
    "You cast 'Expeditious Retreat', but the spell misfires and now your legs are running ... in opposite directions.",
]


PLAYER_TURN_BANNER = r""" ____  _                         _____                 
|  _ \| | __ _ _   _  ___ _ __  |_   _|   _ _ __ _ __  
| |_) | |/ _` | | | |/ _ \ '__|   | || | | | '__| '_ \ 
|  __/| | (_| | |_| |  __/ |      | || |_| | |  | | | |
|_|   |_|\__,_|\__, |\___|_|      |_| \__,_|_|  |_| |_|
               |___/                                   """


class CombatSystem(BaseCommandHandler):
    prompt = f"{Styles.fg.pink}> {Styles.reset}"

    def __init__(self, player: "Player", allies: list["Ally"], enemies: list["Enemy"]):
        super().__init__()
        self.player: "Player" = player
        self.allies: list["Ally"] = allies
        self.enemies: list["Enemy"] = enemies
        self.triggered_help = False
        self.num_skills_owed = 0 # Number of skills owed to the player after the battle, +1 skill per level

    def postcmd(self, stop, line) -> bool:
        if self.triggered_help: # If we got here because of help or unknown cmd, skip the rest of postcmd.
            self.triggered_help = False
            return False
        
        self._allocate_experience()
        if self.player.check_level_up():
            self.num_skills_owed += 1

        if not any(enemy.is_alive() for enemy in self.enemies):
            logger.info("All enemies defeated.")
            colorprint("Room Clear", "lightgreen")
            return True
        
        self.enemy_turn()

        if not self.player.is_alive():
            logger.info("Player died.")
            print_error("You died...\nGame Over!")
            return True
        
        self.ally_turn()

        input(f"{Styles.fg.lightblue}Press Enter to continue...{Styles.reset}")
        
        self._allocate_experience()
        self.player.check_level_up()
        
        if not any(enemy.is_alive() for enemy in self.enemies):
            colorprint("Room Clear", "lightgreen")
            return True
        
        self._player_turn_setup()
        return False


    def do_attack(self, arg):
        logger.info(f"Player {self.player.name} chooses to attack.")

        skill: Optional["Skill"] = self._get_skill()
        logger.debug(f"Player {self.player.name} chose skill: {skill.name if skill else 'None'}.")
        
        if skill:
            targets = self._get_targets(skill)
            results = skill.use(self.player, targets)
            logger.debug(f"Skill used: {skill.name}, hit: {results[1]}.")

            if results[1]:  # If hit
                colorprint(results[0] + "\n", "lightgreen", delay=0.01)
            else:
                print_error(results[0] + "\n")
        return False


    def do_rest(self, arg):
        logger.info(f"Player {self.player.name} chooses to rest.")
        colorprint(f"{self.player.name} takes a nap.", "lightgreen")
        self.player.rest()


    def do_items(self, arg) -> None:
        logger.info(f"Player {self.player.name} chooses to use an item.")
        # Only consumables can be used during combat
        items = [item for item in self.player.inventory if isinstance(item, Consumable)] 
        
        if not items:
            logger.info(f"Cancelled item selction: No valid items for {self.player.name}.")
            print_error("You have no items to use.")
            return None

        self._display_items()

        print_game_msg(f"Pick an item...\n")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}").strip()

        try:
            chosen_index = int(chosen) - 1
            item = items[chosen_index]
            item.consume(self.player)
            
            inv = self.player.inventory.keys()

            logger.debug(f"Player {self.player.name} inventory before item use: {inv}.")

            self.player.remove_item_from_inventory(item)

            logger.debug(f"Player {self.player.name} inventory after item use: {inv}.")
            

        except (ValueError, IndexError):
            logger.info(f"Player {self.player.name} made an invalid selection.")
            print_error("Invalid selection \nPlease try again")
            return self.do_items(arg) # If invalid input then we ask again
        return None
        

    def do_retreat(self, arg):
        logger.info(f"Player {self.player.name} chooses to retreat.")
        self._run_away()


    def do_help(self, arg):
        help_text = f"""
{Styles.bold}Available commands:{Styles.reset}
{Styles.fg.lightgreen}
  attack            - Use a skill
  rest              - Heal 20% max HP, 10% max MP
  items             - Use a consumable item
  retreat           - Retreat (33% success rate)
  help, h           - Show this help
{Styles.reset}
"""
        if os.name != "nt":
            help_text += f"{Styles.fg.lightblue}  [TAB]            - Autocomplete commands{Styles.reset}"
        print(help_text)
        self.triggered_help = True
        
    def do_h(self, arg):
        self.do_help(arg)


    def start_combat(self) -> None:
        logger.info(f"Starting combat with player: {self.player.name}, allies: {', '.join(ally.name for ally in self.allies)}, enemies: {', '.join(enemy.name for enemy in self.enemies)}")
        self._player_turn_setup()
        self.cmdloop()
        return None


    def _player_turn_setup(self) -> None:
        logger.info(f"Player {self.player.name}'s turn begins.")
        clear_stdout()
        colorprint(Styles.bold + PLAYER_TURN_BANNER, "green", delay=0)
        time.sleep(0.3)
        clear_stdout()
        colorprint(f"{Styles.bold}Health: {self.player.health}/{self.player.max_health}", "magenta")
        colorprint(f"{Styles.bold}Mana: {self.player.mana}/{self.player.max_mana}\n", "cyan")

        [effect.apply(self.player) for effect in self.player.effects if self.player.effects]
        self.player.draw_skills()
        

        typing_print(f"{Styles.bold}Enemies:{Styles.reset}")
        colorprint(self._display_enemies() + "\n", "red", delay=0.002)

        if self.allies:
            typing_print(f"{Styles.bold}Allies:{Styles.reset}")
            colorprint(self._display_allies() + "\n", "green", delay=0.002)

        colorprint("Choose an action...", "lightblue")
        print("{red}Attack{reset} | {green}Rest{reset} | {yellow}Items{reset} | {blue}Retreat{reset}".format(
            red=Styles.fg.red,
            reset=Styles.reset,
            yellow=Styles.fg.yellow,
            green=Styles.fg.green,
            blue=Styles.fg.blue,
            pink=Styles.fg.lightblue))
        return None
    

    def _display_enemies(self) -> str:
        return "\n".join(
            [f"{i + 1}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})" for i, enemy in enumerate(self.enemies) if
             enemy.is_alive()])


    def _display_skills(self) -> None:
        for i, skill in enumerate(self.player.skill_hand):
            time.sleep(0.2)
            if skill.mana_cost > self.player.mana: # Print in red / green
                print(
                    f"""{i + 1}. {Styles.fg.red} {skill.name} 
Cost: {skill.mana_cost} MP
Description: {skill.description}
Power: {skill.power}
Target: {skill.target.value}
Accuracy: {skill.accuracy * 100}%{Styles.reset}
"""
                )
            else:
                print(
                    f"""{i + 1}. {Styles.fg.lightgreen} {skill.name} 
Cost: {skill.mana_cost} MP
Description: {skill.description}
Power: {skill.power}
Target: {skill.target.value}
Accuracy: {skill.accuracy * 100}%{Styles.reset}
"""
                )
        return None
    

    def _get_skill(self) -> Optional["Skill"]:
        if not self.player.skill_hand:
            print_error("You have no skills in your hand...")
            return None

        clear_stdout()
        self._display_skills()
        print_game_msg(f"Pick a skill...\n")

        options = [i for i in range(1, len(self.player.skill_hand) + 1)]
        while True:
            try:
                chosen = int(input(f"{Styles.fg.pink}> {Styles.reset}").strip())
                break
            except ValueError:
                print_error("Invalid input.")

        while chosen not in options:
            print_error("Invalid input.")
            try:
                chosen = int(input(f"{Styles.fg.pink}> {Styles.reset}").strip())
            except ValueError:
                pass
        skill = self.player.skill_hand[chosen - 1]
        self.player.discard_skill(skill)
        return skill


    def _display_items(self) -> None:
        items = [item for item in self.player.inventory if isinstance(item, Consumable)] 
        for i, item in enumerate(items, 1):
            quantity = self.player.inventory[item]
            print(f"{Styles.fg.green}{i}. {item.name} x{quantity} - {item.description} {Styles.reset}")
            time.sleep(0.01)
        return None


    def _get_targets(self, skill: "Skill") -> list["Entity"]:
        clear_stdout()
        match skill.target:
            case SkillTarget.SINGLE_ENEMY:
                typing_print(f"{Styles.fg.lightblue}{Styles.bold}{skill.name} selected.{Styles.reset}")
                colorprint(self._display_enemies(), "red", delay=0.002)
                try:
                    chosen_enemy = int(input(
                        f"{Styles.fg.lightblue}Pick an enemy.\n{Styles.reset}{Styles.fg.pink}> {Styles.reset}").strip())
                    target = [self.enemies[chosen_enemy - 1]]
                except (IndexError, ValueError):
                    print_error("Invalid target.")
                    return self._get_targets(skill)
            case SkillTarget.ALL_ENEMIES:
                target = self.enemies
            case SkillTarget.SELF:
                target = [self.player]
            case SkillTarget.ALL_ALLIES:
                if self.allies:
                    target = self.allies
                else:
                    target = []
            case SkillTarget.SINGLE_ALLY:
                typing_print(f"{Styles.fg.lightblue}{skill.name} selected.{Styles.reset}")
                colorprint(self._display_allies(), "lightgreen", delay=0.002)
                if self.allies:
                    try:
                        chosen_ally = int(input(
                            f"{Styles.fg.lightblue}Pick an ally.\n{Styles.reset}{Styles.fg.pink}> {Styles.reset}").strip())
                        target = [self.allies[chosen_ally - 1]]
                    except (IndexError, ValueError):
                        print_error("Invalid target.")
                        return self._get_targets(skill)
                else:
                    target = []
            case _:
                raise ValueError(
                    "Skill initialised incorrectly: error in target.\nThis should never happen. Please report this.")
        return target  # type: ignore


    def _run_away(self) -> None:
        penalty = int(0.1 * self.player.health)

        if rand.choice((False, False, True)): # 33% success
            print_game_msg(f"You manage to flee.")  # 33/66 chance of success when trying to run away
            for enemy in self.enemies:
                enemy.health = 0
            return None

        self.player.health -= penalty
        print_error(f"{rand.choice(RETREAT_FAILURE_MESSAGES)}\nYou lose: \u2014{penalty}HP")  # \u2014: em dash
        
        return None

    def enemy_turn(self) -> None:
        for enemy in self.enemies:
            # Do status effects
            [effect.apply(enemy) for effect in enemy.effects if enemy.effects]

        [self._enemy_action(enemy) for enemy in self.enemies if enemy.is_alive]
        logger.info("Enemies have taken their turn.")
        return None


    def _enemy_action(self, enemy: "Enemy") -> None:
        # Check for any skills that will kill the player, if none found just choose a random skill
        fatal_skills = [skill for skill in enemy.skill_deck if max(1, enemy.attack // 6) * skill.power >= self.player.health]
        if any(fatal_skills):
            chosen_skill = rand.choice(fatal_skills)
            targets = self.npc_choose_target(chosen_skill, enemy)
            logger.debug(f"Enemy {enemy.name} detected and used a fatal skill")

        else:
            chosen_skill = rand.choice(enemy.skill_deck)
            targets = self.npc_choose_target(chosen_skill, enemy)
            logger.debug(f"Enemy {enemy.name} chose a random skill.")

        results = chosen_skill.use(enemy, targets)
        if results[1]:  # If hit
            colorprint(results[0], "red")
        else:
            colorprint(results[0], "lightgreen")
        return None


    def ally_turn(self) -> None:
        if not self.allies:
            logger.info("No allies to take a turn.")
            return None
        
        for ally in self.allies.copy():
            if not ally.is_alive:
                self.allies.remove(ally)
                self.player.allies.remove(ally)
                continue
            # Do status effects
            [effect.apply(ally) for effect in ally.effects if ally.effects]

        [self._ally_action(ally) for ally in self.allies if ally.is_alive]
        
        logger.info("Allies have taken their turn.")
        return None


    def _ally_action(self, ally: "Ally") -> None:
        results = self._use_ally_skill(ally)
        if results[1]:  # If hit
            colorprint(results[0], "lightgreen")
        else:
            print_error(results[0])
        return None


    def _use_ally_skill(self, ally: "Ally") -> tuple[str, bool]:
        """
        :return: Tuple containing the result message and whether the skill hit or not.
        """
        chosen_skill: "Skill" = rand.choice(ally.skill_deck)
        logger.debug(f"Ally {ally.name} chose skill {chosen_skill.name}.")
        targets = self.npc_choose_target(chosen_skill, ally)
        return chosen_skill.use(ally, targets)


    def npc_choose_target(self, skill: "Skill", user: "Entity") -> list["Entity"]:
        allies = self.allies.copy()
        allies.append(self.player)
        match skill.target:
            case SkillTarget.SINGLE_ALLY: # Only used by allies
                logger.debug(f"Ally {user.name} chose target {self.player.name}.")
                return [self.player]
            
            case SkillTarget.ALL_ALLIES: # Only used by allies
                logger.debug(f"Ally {user.name} chose targets {" ".join(ally.name for ally in allies)}.")
                return allies
            
            case SkillTarget.SELF: # Only used by allies
                logger.debug(f"Ally {user.name} chose self as target.")
                return [user]
            
            case SkillTarget.SINGLE_ENEMY:
                if user.profession != Professions.ENEMY:
                    chosen_enemy = rand.choice(self.enemies)
                    logger.debug(f"Ally {user.name} chose target {chosen_enemy.name}.")
                else:
                    chosen_enemy = rand.choice([friendly_entity for friendly_entity in allies])
                    logger.debug(f"Enemy {user.name} chose target {chosen_enemy.name}.")
                return [chosen_enemy]
            
            case SkillTarget.ALL_ENEMIES:
                if user.profession != Professions.ENEMY:
                    return self.enemies
                
                logger.debug(f"Ally {user.name} chose targets {" ".join(enemy.name for enemy in self.enemies)}.")
                return [friendly_entity for friendly_entity in allies]


    def _display_allies(self) -> str:
        return "\n".join(
            [f"{i + 1}. {ally.name} (HP: {ally.health}/{ally.max_health})" for i, ally in enumerate(self.allies) if
             ally.is_alive()])


    def _allocate_experience(self) -> None:
        logger.debug(f"Player experience {self.player.experience}.")
        for enemy in self.enemies:
            if enemy.is_alive():
                continue
            self.player.experience += enemy.exp_amt
            logger.debug(f"Enemy {enemy.name} dead. Added {enemy.exp_amt} experience.")
            self.enemies.remove(enemy)
        logger.debug(f"New experience: {self.player.experience}.")
        return None


    def default(self, line) -> None:
        self.triggered_help = True
        return super().default(line)