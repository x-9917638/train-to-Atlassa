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
from .entities import Entity, Player, Enemy
from .skills import Skill
from .items import Item
from ..utils.enums import CombatCommand, SkillTarget
from ..utils.styles import Styles, colorprint, print_error, print_game_msg

RETREAT_FAILURE_MESSAGES = [ # Courtesy of Deepseek
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





class CombatSystem:
    def __init__(self, player: Player, enemies: list[Enemy]):
        self.player = player
        self.enemies = enemies
    
    def start_combat(self):
        while self.player.is_alive() and any(enemy.is_alive() for enemy in self.enemies):
            # Maybe implement turn order randomly selected... Idk
            self.player_turn()
            
            # Must check before enemy attacks because player might have killed them all on their turn
            if not any(enemy.is_alive() for enemy in self.enemies):
                colorprint("Room Clear", "lightgreen")
                break
                
            self.enemy_turn()

        if not self.player.is_alive():
            print_error("You died...\nGame Over!")
            
        return self.player.is_alive()
    
    def player_turn(self):
        print(f"=== Your Turn ===")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Mana: {self.player.mana}/{self.player.max_mana}")
        self.player.draw_skills()
        # Display enemies
        print("\n".join(self._get_enemies()))

        
        # Handle player input
        self._handle_player_action()

    def _get_enemies(self):
        return [f"{i+1}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})" for i, enemy in enumerate(self.enemies) if enemy.is_alive()]
    

    def _get_skill(self) -> Optional[Skill]:
        if not self.player.skill_hand:
            print_error("You have no skills in your hand...")
            return None
        
        for i, skill in enumerate(self.player.skill_hand):
            if skill.mana_cost > self.player.mana:
                print(f"{i+1}. {Styles.fg.red} {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description} {Styles.reset}")
            else:
                print(f"{i+1}. {Styles.fg.lightgreen} {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description} {Styles.reset}")

        print_game_msg(f"Pick a skill...\n(0 to cancel.)")

        options = [i for i in range(len(self.player.skill_hand) + 1)]
        chosen = 0
        # Get input from user, check if it's a valid number
        # If not, ask again until a valid number is entered
        while not chosen:
            try:
                chosen = int(input(f"{Styles.fg.pink}> {Styles.reset}"))
            except ValueError:
                print_error("Invalid input. Please enter a number.")
        
        while chosen not in options:
            print_error("Invalid selection (0 to cancel).\nPlease try again")
            try:
                chosen = int(input(f"{Styles.fg.pink}> {Styles.reset}"))
            except ValueError:
                print_error("Invalid input. Please enter a digit.")
                continue
            
        skill = self.player.skill_hand[chosen-1]
        self.player.discard_skill(skill)
        return skill
    

    def _get_item(self) -> Optional[Item]:
        items = list(self.player.inventory.keys())
        for i, item in enumerate(items, 1):
            quantity = self.player.inventory[item]
            print(f"{Styles.fg.green}{i}. {item.name} x{quantity} - {item.description} {Styles.reset}")

        print_game_msg(f"Pick an item...\n(0 to cancel.)")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}").strip()

        if chosen == "0":
            return None

        try:
            chosen_index = int(chosen) - 1
            if 0 <= chosen_index < len(items):
                return items[chosen_index]
        except ValueError:
            pass
        print_error("Invalid selection (0 to cancel).\nPlease try again")
        return self._get_item() # If invalid input then we ask again


    def _get_targets(self, skill: Skill) -> list[Entity]:
        match skill.target:
            case SkillTarget.SINGLE_ENEMY:
                chosen_enemy = int(input(f"{Styles.fg.lightblue}{skill.name} selected.\n"
                                         f"Pick an enemy.\n{Styles.reset}" + "\n".join(self._get_enemies()) +
                                         f"\n{Styles.fg.pink}> {Styles.reset}"))
                try:
                    target = [self.enemies[chosen_enemy - 1]]
                except IndexError:
                    print_error("Invalid target.")
                    return self._get_targets(skill)

            case SkillTarget.ALL_ENEMIES:
                target = [self.enemies]
            case SkillTarget.SELF:
                target = [self.player]
            case _:
                # The only way to enter this branch is with a Skill object that has a target set incorrectly.
                raise ValueError("Skill initialised incorrectly: error in target.")
        return target # type: ignore


    def _run_from_combat(self):
        penalty = int(0.1 * self.player.health)
        
        if rand.randint(0,1):
            print_game_msg(f"You manage to flee.") # 50/50 chance of success when trying to run away
            for enemy in self.enemies:
                enemy.health = 0 
        else:
            self.player.health -= penalty # As a penalty for trying retreat, they lose 10% hp
            print_error(f"{rand.choice(RETREAT_FAILURE_MESSAGES)}\nYou lose: \u2014{penalty}HP") # \u2014: em dash


    def _get_initial_command(self) -> str:
        # Ask for input (with style :P)
        commands = ["attack", "retreat", "items", "rest"]
        colorprint("Choose an action...", "lightblue")
        chosen = input("{red}Attack{reset} | {green}Rest{reset} | {yellow}Items{reset} | {blue}Retreat{reset}\n{pink}>{reset} ".format(
            red=Styles.fg.red,
            reset=Styles.reset,
            yellow=Styles.fg.yellow,
            green=Styles.fg.green,
            blue=Styles.fg.blue,
            pink=Styles.fg.lightblue)).lower()

        while chosen not in commands:
            chosen = input("{red}Attack{reset} | {green}Rest{reset} | {yellow}Items{reset} | {blue}Retreat{reset}\n{pink}>{reset} ".format(
                red=Styles.fg.red,
                reset=Styles.reset,
                yellow=Styles.fg.yellow,
                green=Styles.fg.green,
                blue=Styles.fg.blue,
                pink=Styles.fg.lightblue)).lower()
        return chosen


    def _handle_player_action(self):
        command = self._get_initial_command()
        match command:
            case CombatCommand.FIGHT.value:
                skill = self._get_skill()
                try:
                    targets = self._get_targets(skill)
                    results = skill.use(self.player, targets)
                    if results[1]:  # If hit
                        colorprint(results[0], "lightgreen")
                    else:
                        print_error(results[0])  # If miss
                except Exception:
                    return
            case CombatCommand.REST.value: 
                self.player._rest()
            case CombatCommand.ITEM.value: 
                item = self._get_item()
            case CombatCommand.RUN.value:
                self._run_from_combat()

    
    def enemy_turn(self):
        [self._enemy_action(enemy) for enemy in self.enemies if enemy.is_alive]


    def _enemy_action(self, enemy: Enemy):
        # Check for any skills that will kill the player, if none found just choose a random skill
        fatal_skills = [skill for skill in enemy.skills if (enemy.attack + skill.power) >= self.player.health]
        if any(fatal_skills):
            print_error(rand.choice(fatal_skills).use(enemy, [self.player])[0])
        else:
            print_error(rand.choice(enemy.skills).use(enemy, [self.player])[0])
        

