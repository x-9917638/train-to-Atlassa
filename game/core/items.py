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

from functools import partial
import random as rand
from abc import ABC

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .entities import Player, Entity
    from .skills import Skill


class Item(ABC): # ABC: Abstract Base Class
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
        self.boost_range: tuple[int, int] = boost_range
        self.current_boost: int = 0 # Track the random boost so can remove
    

    def equip(self, player:"Player") -> None:
        if self.current_boost:
            raise SystemExit("Weapon was already equipped.\nThis should never happen, please report this.")
        boost: int = rand.randint(*self.boost_range)
        player.attack += boost
        player.max_mana += boost * 10
        player.mana += boost * 10
        self.current_boost = boost
        return None


    def unequip(self, player:"Player") -> None:
        player.attack -= self.current_boost
        player.max_mana -= self.current_boost * 10 # type: ignore
        # Mana should not be negative so check for min value
        player.mana -= min(player.mana, self.current_boost * 10) #type: ignore 
        self.current_boost = 0
        return None


class Armor(Item):
    def __init__(self, name:str, description:str, boost_range: tuple[int, int]):
        """
        :param name: Name of item
        :param description: Description of item
        :param boost_range: The range that the random boost to player stats given by the item can be in.
        """
        super().__init__(name, description)
        self.boost_range: tuple[int, int] = boost_range
        self.current_boost: int = 0 # Track the random boost so can remove
    

    def equip(self, player: "Player") -> None:
        if self.current_boost:
            raise SystemExit("Armor was already equipped.\nThis should never happen, please report this.")
        boost: int = rand.randint(*self.boost_range)
        player.defense += boost
        player.max_health += boost * 10
        player.health += boost * 10
        self.current_boost = boost
        return None


    def unequip(self, player: "Player") -> None:
        player.defense -= self.current_boost
        player.max_health -= self.current_boost * 10 # type: ignore
        player.health -= min(player.health, self.current_boost * 10) # type: ignore
        self.current_boost = 0
        return None


class Consumable(Item):
    def __init__(self, name: str, description: str, effect: Callable[["Entity"], None]):
        """ 
        :param name: Name of item
        :param description: Description of item
        :param effect: Function that applies the effect of the item. Takes one argument, the entity.
        """
        super().__init__(name, description)
        self.effect: Callable[["Entity"], None] = effect
        self.consumed: bool = False # Track if the item has been consumed


    def consume(self, entity: "Entity") -> None:
        # TODO
        assert not self.consumed,"Item was already consumed.\nThis should never happen, please report this."
        self.consumed = True
        self.effect(entity)
        return None


# Use partial before ppassing to Consumable
def heal(entity: "Entity", amount: int) -> None:
    """
    Heal the entity by a certain amount.
        :param player: The player to heal.
        :param amount: The amount to heal the player by. 
    """
    entity.heal(amount) # Already handles health overflow logic
    return None


def mana_restore(player: "Player", amount: int) -> None:
    # Should not be used on enemies or allies.
    """
    Restore the entity's mana by a certain amount. 
        :param player: The entity to restore mana for.
        :param amount: The amount to restore the entity's mana by.
    """
    player.mana = min(player.max_mana, player.mana + amount)
    return None


def add_skill(entity: "Entity", skill: "Skill") -> bool:
    """
    Add a skill to the player's skill list.
        :param entity: The entity to add the skill to.
        :param skill: The skill to add to the entity's skill list.
        :return: True if the skill was added, False if it was already in their deck.
    """
    if skill not in entity.skill_deck:
        entity.skill_deck.append(skill)
        return True
    return False

banana = Consumable("Banana", "A delicious banana that heals you.", partial(heal, amount=50))

SECTION_ONE_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon("Training Sword", "It's a sword, but not a very good one.", (3, 7)): 0.44,
    Weapon("Rusty Sword", "A subpar sword.", (5, 10)): 0.3,
    Weapon("Iron Sword", "A sturdy iron sword.", (8, 15)): 0.2,
    Weapon("Steel Sword", "A sharp steel sword, fit for a knight.", (12, 20)): 0.05,
    Weapon("Enchanted Sword", "A sword, imbued with magic.", (15, 25)): 0.01
}

SECTION_ONE_ARMOR = { # <Armor>: <Weighted Chance>
    Armor("Leather Armor", "Basic leather armor.", (3, 7)): 0.39,
    Armor("Chainmail Armor", "Capable of stopping arrows, but not much more.", (5, 10)): 0.3,
    Armor("Plate Armor", "Of course large metal plates can protect your body.", (8, 15)): 0.2,
    Armor("Dragon Scale Armor", "A set of armor said to be made from dragon scales.", (12, 20)): 0.1,
    Armor("Mystic Armor", "Although designed for mages, it suprisingly presents a high resistance to physical damage.", (15, 25)): 0.01
}

SECTION_ONE_SCROLLS = { # <Consumable>: <Weighted Chance>
    Consumable("Scroll of Healing", "A scroll that heals you for 50 health.", partial(heal, amount=50)): 0.4,
    Consumable("Scroll of Mana", "A scroll that restores 50 mana.", partial(mana_restore, amount=50)): 0.3,
}

SECTION_ONE_ITEMS = { # <Weighted Chance>: <Category>
    0.1: SECTION_ONE_WEAPONS,
    0.1: SECTION_ONE_ARMOR,
    0.8: SECTION_ONE_SCROLLS
}

SECTION_TWO_ITEMS = [

]

SECTION_THREE_ITEMS = [

]

SECTION_FOUR_ITEMS = [

]