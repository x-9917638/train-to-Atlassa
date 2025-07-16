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
from .core.save_handler import handle_save

from .utils import Styles, colorprint, print_game_msg, print_error, typing_print
from .utils import clear_stdout
from .utils import BaseCommandHandler

from .data.skills import WARRIOR_SKILLS, ROGUE_SKILLS, MAGE_SKILLS

import time, os, pathlib, random, logging, copy

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .core.carriages import Carriage
    from .core.skills import Skill

logger = logging.getLogger(__name__)

WARNING_MESSAGE = f"""{" " * 25}{Styles.fg.red}__        ___    ____  _   _ ___ _   _  ____ 
{" " * 25}\ \      / / \  |  _ \| \ | |_ _| \ | |/ ___|
 {" " * 25}\ \ /\ / / _ \ | |_) |  \| || ||  \| | |  _ 
  {" " * 25}\ V  V / ___ \|  _ <| |\  || || |\  | |_| |
   {" " * 25}\_/\_/_/   \_\_| \_\_| \_|___|_| \_|\____|{Styles.reset}"""


class GameData:
    """Data class to hold game state for pickle / unpickle"""
    def __init__(self, player:Player, sections: list[Section], current_section: Section, current_carriage: 'Carriage'):
        self.player: Player = player
        self.sections: list[Section] = sections
        self.current_section: Section = current_section
        self.current_carriage: "Carriage" = current_carriage


class Game:    
    """Note: None of the methods in this class should be called directly. Use GameCommandHandler."""
    def __init__(self, player_name: str, data: Optional[GameData] = None):
        if data:
            # If we have saved data, load it
            self.player: Player = data.player
            self.sections: list[Section] = data.sections
            self.current_section: Section = data.current_section
            self.current_carriage: "Carriage" = data.current_carriage

        else:
            self.player: Player = Player(player_name)
            self.sections: list[Section] = [Section(i+1) for i in range(4)]
            self.current_section: Section = self.sections[0]
            self.current_carriage: "Carriage" = self.current_section.carriages[0]

        self.game_over: bool = False
        self.victory: bool = False
        

    def _to_data(self) -> GameData:
        """Convert the game state to a GameData object for saving."""
        return GameData(
            player=self.player,
            sections=self.sections,
            current_section=self.current_section,
            current_carriage=self.current_carriage
        )

    
    def _fight(self) -> None:
        if not self.current_carriage.enemies:
            print_error("There are no enemies to fight here.")
            return None
        self._initiate_combat(self.player.allies, self.current_carriage.enemies)
        return None

    def _move_player(self, direction: int) -> None:
        # Only 2 ways to move: forward (1) or back (-1)
        current_index: int = self.current_section.carriages.index(self.current_carriage)
        new_index: int = current_index + direction
        
        if 0 <= new_index < len(self.current_section.carriages):
            self.current_carriage = self.current_section.carriages[new_index]
            colorprint(f"Moved to {self.current_carriage.name}.", "lightgreen")
            self._show_info()
        else:
            print_error(f"You can't move {'forward' if direction > 0 else 'back'} - you're at the {'end' if direction > 0 else 'start'} of this section.")


    def _initiate_combat(self, allies: list, enemies: list) -> None:
        combat_system: CombatSystem = CombatSystem(self.player, allies, enemies)
        
        combat_system.start_combat() # Exits once combat is over

        self.current_carriage.enemies = [] # Remove the dead enemies from the carriage
        
        # Check if player died
        if not combat_system.player.is_alive():
            self.game_over = True
            return None

        # Check if combat resulted in boss defeat
        if self.current_carriage.type.value == "Boss Room" and not any(enemy.is_alive() for enemy in enemies):
            self._handle_boss_defeat()
            return None

        num_skills: int = combat_system.num_skills_owed 
        if num_skills > 0:
            self._give_new_skills(num_skills)
            
        self._show_info()
        
        return None


    def _give_new_skills(self, num_skills: int) -> None:
        colorprint(f"You have earned {num_skills} new skill{'s' if num_skills > 1 else ''}!", "lightgreen")
        
        profession: str = f"{self.player.profession.value.upper()}_SKILLS"
        profession_skills: dict[int, list["Skill"]] = copy.deepcopy(globals()[profession])
        
        skill_pool: list["Skill"] = []
        for i in range(1, self.current_section.number + 1):
            skill_pool.extend(profession_skills[i])
        
        num_skills = min(num_skills, len(skill_pool))  # Ensure we don't try to get more skills than available

        new_skills: list["Skill"] = random.sample(skill_pool, k=num_skills)
        self.player.add_skills_to_deck(new_skills)
        
        return None


    def _handle_boss_defeat(self) -> None:
        colorprint("You have defeated the boss!", "lightgreen")

        if self.current_section.number < len(self.sections):
            colorprint(f"Proceeding to floor {self.current_section.number + 1}...", "lightgreen")
            self.current_section = self.sections[self.current_section.number]
            self.current_carriage = self.current_section.carriages[0]

        else:
            colorprint("You have completed all floors! Congratulations!", "lightgreen")
            self.victory = True

        return None


    def _show_player_status(self) -> None:

        colorprint(f"{Styles.bold}Player: {self.player.name}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Health: {self.player.health}/{self.player.max_health}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Mana: {self.player.mana}/{self.player.max_mana}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Attack: {self.player.attack}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Defense: {self.player.defense}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Level: {self.player.level}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Experience: {self.player.experience}/{self.player.level * 30}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Profession: {self.player.profession.value}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Weapon: {self.player.weapon.name if self.player.weapon else 'None'}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Armor: {self.player.armor.name if self.player.armor else 'None'}", "lightgreen", delay=0.005)
        colorprint(f"{Styles.bold}Allies: {', '.join(ally.name for ally in self.player.allies) if self.player.allies else 'None'}", "lightgreen", delay=0.005)

        return None
    

    def _show_info(self) -> None:
        print_game_msg(f"You are at {self.current_carriage.name}.")

        if self.current_carriage.enemies:
            if self.current_carriage.type.value == "Boss Room":
                # WArnning banner
                print(WARNING_MESSAGE)
                typing_print(f"{Styles.fg.red}{"=" * 30}A boss is present in this carriage!{"=" * 30}{Styles.reset}")
                time.sleep(0.2)
                clear_stdout()

            print_error("Enemies present:")
            for enemy in self.current_carriage.enemies:
                print_error(f"- {enemy.name}: {enemy.description}")

        else: 
            print_error("There are no enemies in this carriage.")           
            # Intentionally in the else block, there should never be both an ally and enemy in one carriage
            if self.current_carriage.allies:
                colorprint("Allies present:", "lightgreen")
                for ally in self.current_carriage.allies:
                    colorprint(f"- {ally.name}: {ally.description}", "lightgreen")

            else:
                print_error("There are no allies in this carriage.")

        return None


    def _show_skills(self) -> None:
        if self.player.skill_deck:
            typing_print("Your skills:")
            for skill in self.player.skill_deck:
                print(f"""{Styles.fg.lightgreen}{skill.name} 
Cost: {skill.mana_cost} MP
Descripion: {skill.description}
Power: {skill.power}
Target: {skill.target.value}
Accuracy: {skill.accuracy * 100}%{Styles.reset}
""" + f"{Styles.fg.lightgreen}{"Effect: " + skill.effect.name if skill.effect else ""}{Styles.reset}")
                time.sleep(0.01)
        
        else:
            typing_print("You have no skills.")
        
        return None


    def _show_inventory(self) -> bool:
        """
        :return: True if inventory is not empty, False otherwise
        """
        if self.player.inventory:
            typing_print("Your inventory:")
            for item in self.player.inventory:
                quantity: int = self.player.inventory[item]
                print(f"{Styles.fg.green}- {item.name}, x{quantity}: {item.description}{Styles.reset}")
                time.sleep(0.01)
            return True
        else:
            typing_print("Your inventory is empty.")
        return False

    def _interact_inventory(self) -> None:
        choice = input(f"{Styles.fg.lightblue}Do you want to [e]quip, [u]se, or [d]rop an item? (Enter to cancel) {Styles.reset} ").strip().lower()
        match choice:
            case "e" | "equip":
                self._equip_item()
            case "u" | "use":
                self._use_item()
            case "d" | "drop":
                self._drop_item()
            case "":
                print_game_msg("Cancelled.")
            case _:
                print_error("Invalid choice.")
                return self._interact_inventory()
        return None


    def _equip_item(self) -> None:
        equipment = [item for item in self.player.inventory if hasattr(item, "boost")]
        
        typing_print("Available items:")
        for i, item in enumerate(equipment, 1):
            print(f"{Styles.fg.green}{i}. {item.name} - {item.description}{Styles.reset}")
            time.sleep(0.01)
        
        typing_print(f"{Styles.fg.lightblue}Enter the number of the item to equip: {Styles.reset}")
        choice = input(f"{Styles.fg.pink}> {Styles.reset}").strip()
        
        try:
            index = int(choice) - 1
            item = equipment[index]
            item.equip(self.player)
            typing_print(f"{Styles.fg.green}Equipped {item.name}!{Styles.reset}")
        
        except (ValueError, IndexError):
            print_error("Invalid input.")
            return self._equip_item()
        
        return None
    
    
    def _use_item(self) -> None:
        consumables = [item for item in self.player.inventory if hasattr(item, "effect")]
        if not consumables:
            print_error("You have no consumables to use.")
            return None
        
        print_game_msg(f"Pick an item...\n")
        choice = input(f"{Styles.fg.pink}> {Styles.reset}").strip()

        try:
            chosen_index = int(choice) - 1
            item = consumables[chosen_index]
            item.consume(self.player)
            
            inv = self.player.inventory.keys()

            logger.debug(f"Player {self.player.name} inventory before item use: {inv}.")

            self.player.remove_item_from_inventory(item)

            logger.debug(f"Player {self.player.name} inventory after item use: {inv}.")
            
        except (ValueError, IndexError):
            logger.info(f"Player {self.player.name} made an invalid selection.")
            print_error("Invalid selection \nPlease try again")
            return self._use_item() # If invalid input then we ask again
        return None


    def _drop_item(self) -> None:
        if not self.player.inventory:
            print_error("You have no items to drop.")
            return None
        
        typing_print("Your inventory:")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{Styles.fg.green}{i}. {item.name} - {item.description}{Styles.reset}")
            time.sleep(0.01)

        print_game_msg(f"Pick an item...\n")
        choice = input(f"{Styles.fg.pink}> {Styles.reset}").strip()

        
        try:
            index = int(choice) - 1
            item = list(self.player.inventory.keys())[index]
            quantity = self.player.inventory[item]

            # Check how many items player want to drop
            if quantity > 1:
                typing_print(f"{Styles.fg.lightblue}You have {quantity} of {item.name}. How many do you want to drop?{Styles.reset}")
                num_items = int(input(f"{Styles.fg.pink}> {Styles.reset}").strip())
            else: num_items = 1
            
            for i in range(num_items):
                self.player.remove_item_from_inventory(item)
            typing_print(f"{Styles.fg.green}Dropped {num_items} of {item.name}!{Styles.reset}")
        
        except (ValueError, IndexError):
            print_error("Invalid input.")
            return self._drop_item()
        
        return None


    def _interact_with_allies(self) -> None:
        if not self.current_carriage.allies:
            typing_print("No allies to interact with in this carriage.")
            return None
        
        typing_print("You can interact with the following allies:")
        for ally in self.current_carriage.allies:
            print(f"- {ally.name}: {ally.description}")
            time.sleep(0.01)

        chosen_name = input("Enter a name: ")
        for ally in self.current_carriage.allies:
            if ally.name.lower() == chosen_name.lower():
                self._hire_ally(ally)

            else:
                typing_print(f"No ally with the name {chosen_name} found in this carriage.")

        return None
            
            
    def _hire_ally(self, ally) -> None:
        choice = input(f"Do you wish to hire {ally.name} to join you on this conquest? ([Y]es/[n]o)")
        match choice.lower():
            case "y" | "yes" | "":
                if len(self.player.allies) > 2:
                    print_error("You already have the maximum number of allies (2). You cannot hire more.")
                
                else:
                    self.player.add_ally(ally)
                    self.current_carriage.allies.remove(ally)
                    colorprint(f"{ally.name} has joined your party!", "green")
            
            case "n" | "no":
                return None
            
            case _:
                print_error("Invalid choice.")
        return None


    def _explore_for_items(self) -> None:
        logging.info("Player is exploring for items.")

        if not self.current_carriage.items:
            logging.debug("No items in carriage, search cancelled.")
            print_error("There are no items in this carriage.")
            return None
        
        success = random.choice((True, True)) # 50% to fail search
        if not success: 
            print_error("You found no items in this carriage.")
            self.current_carriage.items = [] 
            logger.debug("Player failed initial chance to find items in the carriage.")
            return None
        
        logger.debug("Player passed initial chance for items in the carriage.")
        colorprint("You found the following items in this carriage:", "green")
        for item in self.current_carriage.items.copy():
            colorprint(f"- {item.name}: {item.description}", "green")
            self.player.add_item_to_inventory(item)
            self.current_carriage.items.remove(item)
        
        return None


    def _save_game(self) -> None:
        handle_save(self._to_data())


class GameCommandHandler(BaseCommandHandler):
    """Handle all commands related to the game."""
    prompt = f"{Styles.fg.pink}> {Styles.reset}"

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game: Game = game
        self.intro: str = f"{Styles.fg.lightblue}Welcome to the game, {self.game.player.name}! [h]elp for commands.\n{Styles.reset}"


    def precmd(self, line: str) -> str:
        clear_stdout()
        return line
    

    def postcmd(self, stop: bool, line: str) -> bool:
        if self.game.game_over or self.game.victory:
           return True
        return super().postcmd(stop, line)


    def postloop(self) -> None:
        # Will be called when the command loop ends
        print_game_msg("Thank you for playing!")
        return super().postloop()


    # Movement
    def do_next(self, arg) -> None:
        self.game._move_player(1)
        return None
    
    def do_n(self, arg) -> None:
        return self.do_next(arg)


    def do_back(self, arg) -> None:
        self.game._move_player(-1)
        return None
    
    def do_b(self, arg) -> None:
        return self.do_back(arg)


    # Combat
    def do_fight(self, arg) -> None:
        self.game._fight()
        return None


    # Information 
    def do_inventory(self, arg) -> None:
        self.game._show_inventory()
        self.game._interact_inventory()
        return None

    def do_inv(self, arg):
        return self.do_inventory(arg)


    def do_skills(self, arg) -> None:
        self.game._show_skills()
        return None


    def do_status(self, arg) -> None:
        self.game._show_player_status()
        return None


    def do_info(self, arg) -> None:
        self.game._show_info()
        return None


    def do_explore(self, arg) -> None:
        # TODO: Check for items!
        self.game._explore_for_items()
        return None

    # Misc
    def show_help(self) -> None:
        help_text = f"""{Styles.bold}Available commands:{Styles.reset}

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
  hire [ally]       - Hire an ally
  explore           - Check the current carriage for any items.{Styles.reset}
{Styles.bold}System:{Styles.reset}{Styles.fg.lightgreen}
  help, h           - Show this help
  exit              - Exit the game
  
{Styles.italics}Autocompletions are supported.{Styles.reset}
"""
        if os.name != "nt": # Autocomplete doesn't work because Windows doesn't have readline
            help_text += f"{Styles.fg.lightblue}  [TAB]            - Autocomplete commands{Styles.reset}"
        print(help_text)
        return None

    def do_help(self, arg) -> None:
        return self.show_help()

    def do_h(self, arg) -> None:
        return self.do_help(arg)
    

    def do_exit(self, arg) -> bool:
        colorprint("Exiting... Byee", "lightgreen")
        return True

    def do_EOF(self, arg) -> bool:
        return self.do_exit(arg)


    def do_hire(self, arg) -> None:
        if not self.game.current_carriage.allies:
            print_error("No allies to hire.")
            return None
        if arg:  # If specific ally was provided
            ally = next((a for a in self.game.current_carriage.allies 
                        if a.name.lower().startswith(arg.lower())), None)
            if ally:
                self.game._hire_ally(ally)
            else:
                print_error(f"No ally named '{arg}' found.")
        else:
            self.game._interact_with_allies()
        return None
    

    def complete_hire(self, text, line, begidx, endidx) -> list[str]:
        # Autocompleton for hire command
        if not self.game.current_carriage.allies:
            return []
        return [ally.name for ally in self.game.current_carriage.allies 
                if ally.name.lower().startswith(text.lower())]


    def do_save(self, arg) -> None:
        self.game._save_game()
        colorprint(f"Game saved to {pathlib.Path("./saves/savegame.pkl").absolute()}!", "lightgreen")
        return None


