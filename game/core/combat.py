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
from ..utils.styles import Styles, colorprint, print_error, print_game_msg

FAILURE_MESSAGES = [ # Courtesy of Deepseek
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
            
            # Must check again because player might have killed them all on their turn
            if not any(enemy.is_alive() for enemy in self.enemies):
                colorprint("Room Clear", "lightgreen")
                break
                
            self.enemy_turn()
        if not self.player.is_alive():
            print_error("You died...")
            
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
            print_error("You have no skills in your hand...")
            return 0
        
        for i, skill in enumerate(self.player.skill_hand):
            if skill.mana_cost > self.player.mana:
                print(f"{i+1}. {Styles.fg.red} {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description} {Styles.reset}")
            else:
                print(f"{i+1}. {Styles.fg.lightgreen} {skill.name} (Cost: {skill.mana_cost} MP) - {skill.description} {Styles.reset}")

        print_game_msg(f"Pick a skill...\n(1 - {len(self.player.skill_hand)}, 0 to cancel.)")
        chosen = int(input(f"{Styles.fg.pink}> {Styles.reset}"))
        options = [i for i in range(len(self.player.skill_hand) + 1)]

        while chosen not in options:
            print_error("Invalid selection (0 to cancel).\nPlease try again")
            chosen = int(input(f"{Styles.fg.pink}> {Styles.reset}"))
        
        chosen_skill = self.player.skill_hand[chosen-1]
        self.player.discard_skill(chosen_skill)
        return chosen_skill



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
        for item, quantity in self.player.inventory.items():
            print(f"{Styles.fg.green}{item.name} x{quantity} - {item.description} {Styles.reset}")

        print_game_msg(f"Pick an item...\n(1 - {len(self.player.inventory)}, 0 to cancel.)")
        chosen = input(f"{Styles.fg.pink}> {Styles.reset}")
        options = [str(i) for i in range(len(self.player.inventory) + 1)]

        while chosen not in options:
            print_error("Invalid selection (0 to cancel).\nPlease try again")
            chosen = input(f"{Styles.fg.pink}> {Styles.reset}")

        return chosen

    def _run_from_combat(self):
        penalty = int(0.1 * self.player.health)
        
        if rand.randint(0,1):
            print_game_msg(f"You manage to flee.") # 50/50 chance of success when trying to run away
            for enemy in self.enemies:
                enemy.health = 0 
        else:
            self.player.health -= penalty # As a penalty for trying retreat, they lose 10% hp
            print_error(f"{rand.choice(FAILURE_MESSAGES)}\nYou lose: \u2014{penalty}HP") # \u2014: em dash


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
                self._run_from_combat()

    
    def enemy_turn(self):
        [self._execute_enemy_action(enemy) for enemy in self.enemies if enemy.is_alive]


    def _execute_enemy_action(self, enemy: Enemy):
        # Check for any fatal skills, if none found just choose a random skill
        fatal_skills = [skill for skill in enemy.skills if (enemy.attack + skill.power) >= self.player.health]
        if any(fatal_skills):
            rand.choice(fatal_skills).use(enemy, [self.player])
        else:
            rand.choice(enemy.skills).use(enemy, [self.player])
        

