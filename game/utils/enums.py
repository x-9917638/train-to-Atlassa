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

from enum import Enum

class CarriageType(Enum):
    SAFE = "Safe Place"
    REST = "Resting Place"
    FIGHT = "Combat Area"
    CHALLENGE = "Challenge Area"
    BOSS = "Boss Room"

class SkillTarget(Enum):
    SELF = "Self"
    SINGLE_ENEMY = "Single Enemy"
    ALL_ENEMIES = "All Enemies"
    SINGLE_ALLY = "Single Ally"
    ALL_ALLIES = "All Allies"

class Professions(Enum):
    WARRIOR = "Warrior"
    MAGE = "Mage"
    ROGUE = "Rogue"
    PRIEST = "Priest"

class CombatCommand(Enum):
    FIGHT = "attack"
    ITEM = "items"
    REST = "rest"
    RUN = "retreat"

class GeneralCommand(Enum):
    NEXT = "next"
    BACK = "back"
    BAG = ["inv", "inventory"] # Player can type shorthand 'inv' or 'inventory'
    SEARCH = "search"

class ItemType(Enum):
    ARMOR = "armor"
    WEAPON = "weapon"
