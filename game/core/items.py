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

from ..utils import Styles, typing_print

from functools import partial
import random as rand
from abc import ABC

import logging
logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Callable, Literal, Optional
if TYPE_CHECKING:
    from .entities import Player, Entity
    from .skills import Skill


class Item(ABC): # ABC: Abstract Base Class
    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description
    
    def __repr__(self): # For debug logs
        return f"{self.name}"

    
class Weapon(Item):
    def __init__(self, name:str, description:str, boost_range: tuple[int, int]):
        """
        :param name: Name of item
        :param description: Description of item
        :param boost_range: The range that the random boost to player stats given by the item can be in.
        """
        super().__init__(name, description)
        self.boost: int = rand.randint(*boost_range) # Random boost to player stats
    

    def equip(self, player:"Player") -> None:
        player.remove_item_from_inventory(self) 
        if player.weapon:
            player.weapon.unequip(player) # Unequip old armor
        player.weapon = self
        logger.debug(f"Equipping weapon {self.name} for player {player.name}.")
        player.attack += self.boost
        player.max_mana += self.boost * 10
        player.mana += self.boost * 10
        return None


    def unequip(self, player:"Player") -> None:
        player.add_item_to_inventory(self)
        player.weapon = None
        logger.debug(f"Unequipping weapon {self.name} for player {player.name}.")
        player.attack -= self.boost
        player.max_mana -= self.boost * 10 
        # Mana should not be negative so check for min value
        player.mana -= min(player.mana, self.boost * 10)
        return None


class Armor(Item):
    def __init__(self, name:str, description:str, boost_range: tuple[int, int]):
        """
        :param name: Name of item
        :param description: Description of item
        :param boost_range: The range that the random boost to player stats given by the item can be in.
        """
        super().__init__(name, description)
        self.boost: int = rand.randint(*boost_range) # Random boost to player stats
    

    def equip(self, player: "Player") -> None:
        player.remove_item_from_inventory(self) # Remove from inventory when equipped
        if player.armor:
            player.armor.unequip(player) # Unequip old armor
        player.armor = self
        logger.debug(f"Equipping armor {self.name} for player {player.name}.")
        player.defense += self.boost
        player.max_health += self.boost * 10
        player.health += self.boost * 10
        return None


    def unequip(self, player: "Player") -> None:
        player.add_item_to_inventory(self) # Add back to inventory when unequipped
        player.armor = None
        logger.debug(f"Unequipping armor {self.name} for player {player.name}.")
        player.defense -= self.boost
        player.max_health -= self.boost * 10 
        player.health -= min(player.health, self.boost * 10)
        return None


class Consumable(Item):
    def __init__(self, name: str, description: str, effect: Callable[["Player"], None], consume_msg: Optional[str] = None ):
        """ 
        :param name: Name of item
        :param description: Description of item
        :param effect: Function that applies the effect of the item. Takes one argument, the entity.
        """
        super().__init__(name, description)
        self.effect: Callable[["Player"], None] = effect
        # If it doesn't have a custom consume message, then we can assume it's a scroll so tear it
        self.consume_msg: str = consume_msg if consume_msg else f"{Styles.fg.lightgreen}You tear the {self.name}.{Styles.reset}"


    def consume(self, player: "Player") -> None:
        logger.debug(f"Consuming item {self.name} for player {player.name}.")
        self.effect(player)
        typing_print(self.consume_msg)
        return None
