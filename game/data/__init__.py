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

from .weapons import SECTION_ONE_WEAPONS, SECTION_TWO_WEAPONS, SECTION_THREE_WEAPONS, SECTION_FOUR_WEAPONS
from .armor import SECTION_ONE_ARMOR, SECTION_TWO_ARMOR, SECTION_THREE_ARMOR, SECTION_FOUR_ARMOR
from .consumables import SECTION_ONE_CONSUMABLES, SECTION_TWO_CONSUMABLES, SECTION_THREE_CONSUMABLES, SECTION_FOUR_CONSUMABLES

SECTION_ONE_ITEMS = [ # <Weighted Chance>: <Category>
    SECTION_ONE_WEAPONS,
    SECTION_ONE_ARMOR,
    SECTION_ONE_CONSUMABLES,
]

SECTION_TWO_ITEMS = [
    SECTION_TWO_WEAPONS,
    SECTION_TWO_ARMOR,
    SECTION_TWO_CONSUMABLES,
]

SECTION_THREE_ITEMS = [
    SECTION_THREE_WEAPONS,
    SECTION_THREE_ARMOR,
    SECTION_THREE_CONSUMABLES,
]

SECTION_FOUR_ITEMS = [
    SECTION_FOUR_WEAPONS,
    SECTION_FOUR_ARMOR,
    SECTION_FOUR_CONSUMABLES,
]


