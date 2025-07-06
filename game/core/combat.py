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

import random as rand
from typing import Optional
from .entities import *
from .skills import Skill
from .items import Item
from ..utils import SkillTarget, Professions
from ..utils import Styles, colorprint, print_error, print_game_msg
from ..utils import BaseCommandHandler
import os, subprocess
import time


def clear_stdout():
    if os.name == "posix":
        subprocess.run(['clear'])
    elif os.name == "nt":
        subprocess.run(['cls'], shell=True)
    else:
        raise NotImplementedError("Unsupported platform. How did you even get here?")


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

    def __init__(self, player: Player, allies: list[Ally], enemies: list[Enemy]):
        super().__init__()
        self.player = player
        self.allies = allies
        self.enemies = enemies
        self.triggered_help = False

    def postcmd(self, stop, line) -> bool:
        if self.triggered_help: # If we got here because of help or unknown cmd, skip the rest of postcmd.
            self.triggered_help = False
            return False
        
        self._allocate_experience()
        self.player.check_level_up()

        if not any(enemy.is_alive() for enemy in self.enemies):
            colorprint("Room Clear", "lightgreen")
            return True
        
        self.enemy_turn()

        if not self.player.is_alive():
            print_error("You died...\nGame Over!")
            return True
        
        self.ally_turn()

        input(f"{Styles.fg.lightblue}Press Enter to continue...{Styles.reset}")

        if not any(enemy.is_alive() for enemy in self.enemies):
            colorprint("Room Clear", "lightgreen")
            return True
        
        self._player_turn_setup()
        return False

    def do_attack(self, arg):
        skill = self._get_skill()
        try:
            targets = self._get_targets(skill)
            results = skill.use(self.player, targets)
            if results[1]:  # If hit
                colorprint(results[0] + "\n", "lightgreen")
            else:
                print_error(results[0] + "\n")
        except AttributeError:
            pass
        return False


    def do_rest(self, arg):
        colorprint(f"{self.player.name} takes a nap.", "lightgreen")
        self.player.rest()

    def do_items(self, arg):
        items = list(self.player.inventory.keys())
        self._display_items()

        print_game_msg(f"Pick an item...\n")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}").strip()

        try:
            chosen_index = int(chosen) - 1
            if 0 <= chosen_index < len(items):
                return items[chosen_index]
        except ValueError:
            pass

        print_error("Invalid selection \nPlease try again")
        return self.do_items(arg)  # If invalid input then we ask again

    def do_retreat(self, arg):
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

    def start_combat(self):
        self._player_turn_setup()
        self.cmdloop()

    def _player_turn_setup(self):
        clear_stdout()
        colorprint(Styles.bold + PLAYER_TURN_BANNER, "green")
        time.sleep(0.3)
        clear_stdout()
        colorprint(f"{Styles.bold}Health: {self.player.health}/{self.player.max_health}", "magenta")
        colorprint(f"{Styles.bold}Mana: {self.player.mana}/{self.player.max_mana}\n", "cyan")

        [effect.apply(self.player) for effect in self.player.effects if self.player.effects]
        self.player.draw_skills()

        print(f"{Styles.bold}Enemies:{Styles.reset}")
        colorprint(self._display_enemies() + "\n", "red")

        if self.allies:
            print(f"{Styles.bold}Allies:{Styles.reset}")
            colorprint(self._display_allies() + "\n", "green")

        colorprint("Choose an action...", "lightblue")
        print("{red}Attack{reset} | {green}Rest{reset} | {yellow}Items{reset} | {blue}Retreat{reset}".format(
            red=Styles.fg.red,
            reset=Styles.reset,
            yellow=Styles.fg.yellow,
            green=Styles.fg.green,
            blue=Styles.fg.blue,
            pink=Styles.fg.lightblue))

    def _display_enemies(self):
        return "\n".join(
            [f"{i + 1}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})" for i, enemy in enumerate(self.enemies) if
             enemy.is_alive()])

    def _display_skills(self):
        for i, skill in enumerate(self.player.skill_hand):
            time.sleep(0.2)
            if skill.mana_cost > self.player.mana:
                print(
                    f"""{i + 1}. {Styles.fg.red} {skill.name} 
(Cost: {skill.mana_cost} MP)
{skill.description}
Target: {skill.target.value}{Styles.reset}
"""
                )
            else:
                print(
                    f"""{i + 1}. {Styles.fg.lightgreen} {skill.name} 
(Cost: {skill.mana_cost} MP)
{skill.description}
Target: {skill.target.value}{Styles.reset}
"""
                )

    def _get_skill(self) -> Optional[Skill]:
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

    def _display_items(self):
        items = list(self.player.inventory.keys())
        for i, item in enumerate(items, 1):
            quantity = self.player.inventory[item]
            print(f"{Styles.fg.green}{i}. {item.name} x{quantity} - {item.description} {Styles.reset}")

    def _get_item(self) -> Optional[Item]:
        items = list(self.player.inventory.keys())
        self._display_items()

        print_game_msg(f"Pick an item...\n")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}").strip()

        try:
            chosen_index = int(chosen) - 1
            if 0 <= chosen_index < len(items):
                return items[chosen_index]
        except ValueError:
            pass

    def _get_targets(self, skill: Skill) -> list[Entity]:
        clear_stdout()
        match skill.target:
            case SkillTarget.SINGLE_ENEMY:
                print(f"{Styles.fg.lightblue}{Styles.bold}{skill.name} selected.{Styles.reset}")
                colorprint(self._display_enemies(), "red")
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
                print(f"{Styles.fg.lightblue}{skill.name} selected.{Styles.reset}")
                colorprint(self._display_allies(), "lightgreen")
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

    def _run_away(self):
        penalty = int(0.1 * self.player.health)

        if rand.choice((0, 0, 1)):
            print_game_msg(f"You manage to flee.")  # 33/66 chance of success when trying to run away
            for enemy in self.enemies:
                enemy.health = 0
            return

        self.player.health -= penalty
        print_error(f"{rand.choice(RETREAT_FAILURE_MESSAGES)}\nYou lose: \u2014{penalty}HP")  # \u2014: em dash

    def enemy_turn(self):
        [self._enemy_action(enemy) for enemy in self.enemies if enemy.is_alive]

    def _enemy_action(self, enemy: Enemy):
        # Check for any skills that will kill the player, if none found just choose a random skill
        fatal_skills = [skill for skill in enemy.skills if (enemy.attack + skill.power) >= self.player.health]
        if any(fatal_skills):
            print_error(rand.choice(fatal_skills).use(enemy, [self.player])[0])
        else:
            print_error(rand.choice(enemy.skills).use(enemy, [self.player])[0])

    def ally_turn(self):
        [self._ally_action(ally) for ally in self.allies if ally.is_alive]

    def _ally_action(self, ally: Ally):
        results = self._use_ally_skill(ally)

        if results[1]:  # If hit
            colorprint(results[0], "lightgreen")
        else:
            print_error(results[0])

    def _use_ally_skill(self, ally: Ally):
        chosen_skill = rand.choice(ally.skills)
        match ally.profession:
            case Professions.PRIEST:
                if chosen_skill.target == SkillTarget.SINGLE_ALLY:
                    return chosen_skill.use(ally, [self.player])
                elif chosen_skill.target == SkillTarget.ALL_ALLIES:
                    allies = self.allies.copy()
                    allies.append(self.player)
                    return chosen_skill.use(ally, allies)
                else:
                    return chosen_skill.use(ally, [ally])
            case Professions.WARRIOR | Professions.ROGUE | Professions.MAGE:
                if chosen_skill.target == SkillTarget.SINGLE_ENEMY:
                    return chosen_skill.use(ally, [rand.choice(self.enemies)])
                elif chosen_skill.target == SkillTarget.ALL_ENEMIES:
                    return chosen_skill.use(ally, self.enemies)
            case _:
                raise ValueError(
                    f"Unknown profession: {ally.profession}\n This should never happen. Please report this.")

    def _display_allies(self):
        return "\n".join(
            [f"{i + 1}. {ally.name} (HP: {ally.health}/{ally.max_health})" for i, ally in enumerate(self.allies) if
             ally.is_alive()])

    def _allocate_experience(self):
        for enemy in self.enemies:
            if enemy.is_alive():
                continue
            self.player.experience += enemy.exp_amt
            self.enemies.remove(enemy)

    def default(self, line):
        self.triggered_help = True
        return super().default(line)