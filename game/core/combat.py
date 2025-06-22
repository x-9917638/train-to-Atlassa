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
from .entities import Player, Enemy
from ..utils.enums import CombatCommand
from ..utils.styles import Styles, colorprint

class CombatSystem:
    def __init__(self, player: Player, enemies: list[Enemy]):
        self.player = player
        self.enemies = enemies
    
    def start_combat(self):
        while self.player.is_alive() and any(enemy.is_alive() for enemy in self.enemies):
            # Maybe implement turn order randomly selected... Idk
            self.player_turn()
            
            # Must check again because player might have killed them all on their turn
            if not any(enemy.is_alive() for enemy in self.enemies):
                break
                
            self.enemy_turn()
        
        return self.player.is_alive()
    
    def player_turn(self):
        print(f"\n=== Your Turn ===")
        print(f"Health: {self.player.health}/{self.player.max_health}")
        print(f"Mana: {self.player.mana}/{self.player.max_mana}")
        
        # Display enemies and skills
        print(self._get_enemies())

        
        # Handle player input
        self._handle_player_action()

    def _get_enemies(self):
        return [f"{i+1}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})" for i, enemy in enumerate(self.enemies) if enemy.is_alive()]
    

    def _get_chosen_skill(self):
        """Get skills in player's hands returned in a list of strings formatted for display"""
        if self.player.skill_hand == []:
            colorprint("You have no skills in your hand...", "red")
            return 0
        for i, skill in enumerate(self.player.skill_hand):
            if skill.mana_cost > self.player.mana:
                print(f"{i+1}. {Styles.fg.red} {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description} {Styles.reset}")
            else:
                print(f"{i+1}. {Styles.fg.lightgreen} {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description} {Styles.reset}")
        colorprint(f"Pick a skill...\n(1 - {len(self.player.skill_hand)}, 0 to cancel.)", "lightblue")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}")
        options = [str(i) for i in range(len(self.player.skill_hand) + 1)]
        while chosen not in options:
            colorprint("Invalid selection. (0 to cancel).\nPlease try again", "red")
            chosen = input(f"{Styles.fg.pink}> {Styles.reset}")
        self.player.discard_skill(self.player.skill_hand[chosen-1])



    def _get_player_action(self):
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
    
    def _get_chosen_item(self):
        for item, quantity in self.player.inventory.items(): # Convert it into a set to remove duplicate listings
            print(f"{Styles.fg.green}{item.name} x{quantity} - {item.description} {Styles.reset}")
        colorprint(f"Pick an item...\n(1 - {len(self.player.inventory)}, 0 to cancel.)", "lightblue")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}")
        options = [str(i) for i in range(len(self.player.inventory) + 1)]
        while chosen not in options:
            colorprint("Invalid selection. (0 to cancel).\nPlease try again", "red")
            chosen = input(f"{Styles.fg.pink}> {Styles.reset}")

        return chosen

    def _handle_player_action(self):
        command = self._get_player_action()
        match command:
            case CombatCommand.FIGHT.value: 
                self._get_chosen_skill()
            case CombatCommand.REST.value: 
                self.player.rest()
            case CombatCommand.ITEM.value: 
                self._get_chosen_item()
            case CombatCommand.RUN.value: 
                pass

    
    def enemy_turn(self):
        [self._execute_enemy_action(enemy) for enemy in self.enemies if enemy.is_alive]


    def _execute_enemy_action(self, enemy: Enemy):
        # Check for any fatal skills, if none found just choose a random skill
        fatal_skills = [skill for skill in enemy.skills if (enemy.attack + skill.power) >= self.player.health]
        if any(fatal_skills):
            rand.choice(fatal_skills).use(enemy, [self.player])
        else:
            rand.choice(enemy.skills).use(enemy, [self.player])
        

