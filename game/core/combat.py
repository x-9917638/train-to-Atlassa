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

from .entities import Player, Enemy
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
        self._get_enemies()
        self._get_skills()
        
        # Handle player input
        self._handle_player_action()

    def _get_enemies(self):
        return [f"{i+1}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})" for i, enemy in enumerate(self.enemies) if enemy.is_alive()]
    
    def _get_skills(self):
        return [f"{i+1}. {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description}" for i, skill in enumerate(self.player.skill_hand)]
    
    def _get_player_action(self):
        # Ask for input (with style :P)
        commands = ["attack", "retreat", "items", "rest"]
        colorprint("Choose an action...", "lightblue")
        chosen = input("{red}Attack{reset} | {green}Rest{reset} | {yellow}Items{reset} | {blue}Retreat{reset}\n{pink}> ".format(
            red=Styles.fg.red, 
            reset=Styles.reset, 
            yellow=Styles.fg.yellow, 
            green=Styles.fg.green, 
            blue=Styles.fg.blue, 
            pink=Styles.fg.lightblue))
        while chosen.lower() not in commands:
            chosen = input("{red}Attack{reset} | {green}Rest{reset} | {yellow}Items{reset} | {blue}Retreat{reset}\n{pink}> ".format(
                red=Styles.fg.red, 
                reset=Styles.reset, 
                yellow=Styles.fg.yellow, 
                green=Styles.fg.green, 
                blue=Styles.fg.blue, 
                pink=Styles.fg.lightblue))
        return chosen
    
    def _handle_player_action(self):
        command = self._get_player_action()
        match command:
            case _: pass
    
    def enemy_turn(self):
        [self._execute_enemy_action(enemy) for enemy in self.enemies if enemy.is_alive]


    def _execute_enemy_action(self, enemy):
        # Implementation of enemy AI
        pass
