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


from game.game import Game
from game.core import *
from game.utils.styles import Styles, colorprint


banana = Item("Banana", "A cool banana")
apple = Item("Apple", "Big red apple")
pear = Item("Pear", "A sour pear!")
game = Game(input(f"{Styles.fg.lightgreen}Enter Player Name: {Styles.reset}"))
goblin = Enemy("Goblin", "Green thing", 10, 1000, 0)
goblin.skills = [GENERAL_SKILLS["Basic Attack"], GENERAL_SKILLS["Power Strike"]]
bobette = Ally("Bobette", 10, Professions.PRIEST)
bobette.skills = [GENERAL_SKILLS["Basic Heal"], PRIEST_SKILLS["Divine Shield"], PRIEST_SKILLS["Holy Light"]]
game.player.skill_hand = [GENERAL_SKILLS["Basic Attack"], GENERAL_SKILLS["Power Strike"]]
game.player.inventory = {banana: 2, apple:7, pear: 1}
game.initiate_combat([bobette], [goblin])
