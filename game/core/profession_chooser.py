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

# Moved into its own class for autocompletions
from ..utils import BaseCommandHandler
from ..utils import Styles, clear_stdout, print_error
from ..utils import Professions


class ProfessionChooser(BaseCommandHandler):
    
    # Priest is excluded - only npcs should have preist profession
    prompt = f"""\n{Styles.bold}{Styles.fg.lightblue}Available Professions:{Styles.reset}
{Styles.fg.lightgreen}Rogue{Styles.reset} - {Styles.fg.lightblue}Stealthy and agile.
{Styles.fg.lightgreen}Warrior{Styles.reset} - {Styles.fg.lightblue}Strong and resilient.
{Styles.fg.lightgreen}Mage{Styles.reset} - {Styles.fg.lightblue}Masters of the arcane.
{Styles.reset}
{Styles.fg.lightblue}Choose a profession: {Styles.reset}"""

    def __init__(self, game):
        super().__init__()
        self.game = game

    def postloop(self) -> None:
        clear_stdout()
        return super().postloop()

    def do_rogue(self, arg):
        """Choose the Rogue profession."""
        self.game.player.profession = Professions.ROGUE
        print(f"{Styles.fg.lightgreen}You have chosen the Rogue profession!{Styles.reset}")
        return True

    def do_warrior(self, arg):
        """Choose the Warrior profession."""
        self.game.player.profession = Professions.WARRIOR
        print(f"{Styles.fg.lightgreen}You have chosen the Warrior profession!{Styles.reset}")
        return True
    
    def do_mage(self, arg):
        """Choose the Mage profession."""
        self.game.player.profession = Professions.MAGE
        print(f"{Styles.fg.lightgreen}You have chosen the Mage profession!{Styles.reset}")
        return True
    
    def default(self, line):
        """Handle invalid input."""
        clear_stdout()
        print_error(f"{Styles.fg.lightred}Invalid profession. Please choose Rogue, Warrior, or Mage.{Styles.reset}")
        return

    def emptyline(self):
        self.default("") 
    
