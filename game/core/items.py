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
from .status_effects import StatusEffect
from ..utils.enums import ItemType
from abc import ABC

class Item(ABC):
    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    
class Weapon(Item):
    def __init__(self, name:str, description:str, boost_range: tuple[int, int]):
        """
        :param name: Name of item
        :param description: Description of item
        :param boost_range: The range that the random boost to player stats given by the item can be in.
        """
        super().__init__(name, description)
        self.boost_range = boost_range
        self.current_boost = None # Track the random boost so can remove
    

    def equip(self, player):
        if self.current_boost:
            raise SystemExit("Weapon was already equipped.\nThis should never happen, please report this.")
        boost = rand.randint(*self.boost_range)
        player.attack += boost
        player.max_mana += boost * 10
        player.mana += boost * 10
        self.current_boost = boost


    def unequip(self, player):
        player.attack -= self.current_boost
        player.max_mana -= self.current_boost * 10 # type: ignore
        player.mana -= self.current_boost * 10 # type: ignore
        self.current_boost = None


class Armor(Item):
    def __init__(self, name:str, description:str, boost_range: tuple[int, int]):
        """
        :param name: Name of item
        :param description: Description of item
        :param boost_range: The range that the random boost to player stats given by the item can be in.
        """
        super().__init__(name, description)
        self.boost_range = boost_range
        self.current_boost = None # Track the random boost so can remove
    
    def equip(self, player):
        if self.current_boost:
            raise SystemExit("Armor was already equipped.\nThis should never happen, please report this.")
        boost = rand.randint(*self.boost_range)
        player.defense += boost
        player.max_health += boost * 10
        player.health += boost * 10
        self.current_boost = boost


    def unequip(self, player):
        player.defense -= self.current_boost
        player.max_health -= self.current_boost * 10 # type: ignore
        player.health -= self.current_boost * 10 # type: ignore
        self.current_boost = None


class Consumable(Item): # TODO
    def __init__(self, name: str, description: str, effect: StatusEffect):
        super().__init__(name, description)
        self.effect = effect
        self.consumed = False # Track if the item has been consumed

    def consume(self, player):
        # TODO
        if self.consumed:
            raise Exception("Item was already consumed.\nThis should never happen, please report this.")
        self.consumed = True
        player.effects.append(self.effect)
