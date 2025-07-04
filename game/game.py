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


from .core.entities import Player
from .core.section import Section
from .core.combat import CombatSystem
from .utils import Styles, colorprint, print_game_msg, print_error, typing_print
from .utils import clear_stdout
from .utils import BaseCommandHandler
import time

WARNING_MESSAGE = f"""{" " * 25}{Styles.fg.red}__        ___    ____  _   _ ___ _   _  ____ 
{" " * 25}\ \      / / \  |  _ \| \ | |_ _| \ | |/ ___|
 {" " * 25}\ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _ 
  {" " * 25}\ V  V / ___ \|  _ <| |\  || || |\  | |_| |
   {" " * 25}\_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____|{Styles.reset}"""


class Game(BaseCommandHandler):    
    prompt = f"{Styles.fg.pink}> {Styles.reset}"
    
    def __init__(self, player_name: str):
        super().__init__()
        self.player = Player(player_name)
        self.sections = [Section(i+1) for i in range(4)]
        self.current_section = self.sections[0]
        self.current_carriage = self.current_section.carriages[0]
        self.game_over = False
        self.victory = False
        self.intro = f"{Styles.fg.lightblue}Welcome to the game, {player_name}! [h]elp for commands.\n{Styles.reset}"

    def precmd(self, line):
        clear_stdout()
        return line

    def postcmd(self, stop, line):
        if self.game_over or self.victory:
            return True  # This will stop the cmd loop
        return False

    # Movement commands
    def do_next(self, arg):
        self._move_player(1)
    def do_n(self, arg):
        self.do_next(arg)

    def do_back(self, arg):
        self._move_player(-1)
    def do_b(self, arg):
        self.do_back(arg)

    # Combat commands
    def do_fight(self, arg):
        """Initiate combat with enemies in current carriage: fight [enemy]"""
        if not self.current_carriage.enemies:
            print_error("There are no enemies to fight here.")
            return

        self.initiate_combat(self.player.allies, self.current_carriage.enemies)

    # Information commands
    def do_inventory(self, arg):
        self.show_inventory()
    def do_inv(self, arg):
        self.do_inventory(arg)

    def do_skills(self, arg):
        self.show_skills()

    def do_status(self, arg):
        self.show_player_status()

    def do_info(self, arg):
        self.show_info()

    # Interaction commands
    def do_interact(self, arg):
        if not self.current_carriage.allies:
            print_error("No allies to interact with here.")
            return
            
        if arg:  # If specific ally was provided
            ally = next((a for a in self.current_carriage.allies 
                        if a.name.lower().startswith(arg.lower())), None)
            if ally:
                self.hire_ally(ally)
            else:
                print_error(f"No ally named '{arg}' found.")
        else:
            self.interact_with_allies()

    # System commands
    def do_help(self, arg):
        self.show_help()

    def do_h(self, arg):
        self.do_help(arg)

    def do_exit(self, arg):
        colorprint("Exiting... Byee", "lightgreen")
        self.game_over = True
        return True

    def do_EOF(self, arg):
        return self.do_exit(arg)

    # Tab completion methods
    def complete_interact(self, text, line, begidx, endidx):
        if not self.current_carriage.allies:
            return []
        return [ally.name for ally in self.current_carriage.allies 
                if ally.name.lower().startswith(text.lower())]

    # Game logic methods
    def _move_player(self, direction):
        current_index = self.current_section.carriages.index(self.current_carriage)
        new_index = current_index + direction
        
        if 0 <= new_index < len(self.current_section.carriages):
            self.current_carriage = self.current_section.carriages[new_index]
            colorprint(f"Moved to {self.current_carriage.name}.", "lightgreen")
            self.show_info()
        else:
            print_error(f"You can't move {'forward' if direction > 0 else 'back'} - you're at the {'end' if direction > 0 else 'start'} of the floor.")

    def initiate_combat(self, allies: list, enemies: list):
        combat_system = CombatSystem(self.player, allies, enemies)
        combat_system.start_combat()
        self.current_carriage.enemies = []
        print("\n\n")
        # Check if combat resulted in boss defeat
        if self.current_carriage.type.value == "Boss Room" and not any(enemy.is_alive() for enemy in enemies):
            self.handle_boss_defeat()
        else:
            self.do_info("") # Show info after combat


    def handle_boss_defeat(self):
        colorprint("You have defeated the boss!", "lightgreen")
        if self.current_section.number < len(self.sections):
            colorprint(f"Proceeding to floor {self.current_section.number + 1}...", "lightgreen")
            self.current_section = self.sections[self.current_section.number]
            self.current_carriage = self.current_section.carriages[0]
            self.show_info()
        else:
            colorprint("You have completed all floors! Congratulations!", "lightgreen")
            self.victory = True

    def show_help(self):
        help_text = f"""
{Styles.bold}Available commands:{Styles.reset}

{Styles.bold}Movement:{Styles.reset}{Styles.fg.lightgreen}
  next, n           - Move to next carriage
  back, b           - Move to previous carriage{Styles.reset}
{Styles.bold}Combat:{Styles.reset}{Styles.fg.lightgreen}
  fight             - Initiate combat{Styles.reset}
{Styles.bold}Information:{Styles.reset}{Styles.fg.lightgreen}
  inv, inventory    - Show inventory
  skills            - Show skills
  status            - Show player status
  info              - Show current carriage info{Styles.reset}
{Styles.bold}Interaction:{Styles.reset}{Styles.fg.lightgreen}
  interact [ally]   - Interact with allies (with specific ally if provided){Styles.reset}
{Styles.bold}System:{Styles.reset}{Styles.fg.lightgreen}
  help, h           - Show this help
  exit              - Exit the game
  
{Styles.italics}Autocompletions are supported.{Styles.reset}
"""
        print(help_text)


    def show_player_status(self):
        colorprint(f"{Styles.bold}Player: {self.player.name}", "lightgreen")
        colorprint(f"{Styles.bold}Health: {self.player.health}/{self.player.max_health}", "lightgreen")
        colorprint(f"{Styles.bold}Mana: {self.player.mana}/{self.player.max_mana}", "lightgreen")
        colorprint(f"{Styles.bold}Attack: {self.player.attack}", "lightgreen")
        colorprint(f"{Styles.bold}Defense: {self.player.defense}", "lightgreen")
        colorprint(f"{Styles.bold}Level: {self.player.level}", "lightgreen")
        colorprint(f"{Styles.bold}Experience: {self.player.experience}/{self.player.level * 50}", "lightgreen")
        colorprint(f"{Styles.bold}Profession: {self.player.profession.value}", "lightgreen")
    

    def show_info(self):
        print_game_msg(f"You are at {self.current_carriage.name}.")

        if self.current_carriage.enemies:
            if self.current_carriage.type.value == "Boss Room":
                print(WARNING_MESSAGE)
                typing_print(f"{Styles.fg.red}{"=" * 30}A boss is present in this carriage!{"=" * 30}{Styles.reset}", delay=0.01)
                time.sleep(0.2)
                clear_stdout()
            print_error("Enemies present:")
            for enemy in self.current_carriage.enemies:
                print_error(f"- {enemy.name}: {enemy.description}")
        else:            
            # Intentionally in the else block, there will never be both an ally and enemy in one carriage
            if self.current_carriage.allies:
                colorprint("Allies present:", "lightgreen")
                for ally in self.current_carriage.allies:
                    colorprint(f"- {ally.name}: {ally.description}", "lightgreen")
            else:
                print_error("There are no allies in this carriage.")


    def show_skills(self):
        if self.player.skills:
            print("Your skills:")
            for skill in self.player.skills:
                print(f"- {skill.name}: {skill.description}")
        else:
            print("You have no skills.")

    def show_inventory(self):
        if self.player.inventory:
            print("Your inventory:")
            for item in self.player.inventory:
                quantity = self.player.inventory[item]
                print(f"- {item.name}, x{quantity}: {item.description}")
        else:
            print("Your inventory is empty.")

    def interact_with_allies(self):
        if not self.current_carriage.allies:
            print("No allies to interact with in this carriage.")
            return
        
        print("You can interact with the following allies:")
        for ally in self.current_carriage.allies:
            print(f"- {ally.name}: {ally.description}")

        ally_name = input("Enter a name: ")
        for ally in self.current_carriage.allies:
            if ally.name.lower() == ally_name.lower():
                self.hire_ally(ally)
            else:
                print(f"No ally with the name {ally_name} found in this carriage.")
                return
            
            
    def hire_ally(self, ally):
        choice = input(f"Do you wish to hire {ally.name} to join you on this conquest? ([Y]es/[n]o)")
        match choice.lower():
            case "y" | "yes" | "":
                if len(self.player.allies) > 2:
                    print("You already have the maximum number of allies. You cannot hire more.")
                else:
                    self.player.add_ally(ally)
                    self.current_carriage.allies.remove(ally)
                    print(f"{ally.name} has joined your party!")
            case "n" | "no":
                return
            case _:
                print_error("Invalid choice.")

