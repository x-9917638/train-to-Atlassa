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

from .skills import ROGUE_SKILLS, WARRIOR_SKILLS, MAGE_SKILLS
from ..utils import Styles

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
        self.consume_msg: str = consume_msg if consume_msg else f"{Styles.fg.lightgreen}You use the {self.name}.{Styles.reset}"
        self.consumed: bool = False # Track if the item has been consumed


    def consume(self, player: "Player") -> None:
        # TODO
        assert not self.consumed,"Item was already consumed.\nThis should never happen, please report this."
        logger.debug(f"Consuming item {self.name} for player {player.name}.")
        self.consumed = True
        self.effect(player)
        print(self.consume_msg)
        return None

# Consumable effects
# Use partial before ppassing to instantiator
def heal(player: "Player", amount: int) -> None:
    """
    Heal the entity by a certain amount.
        :param player: The player to heal.
        :param amount: The amount to heal the player by. 
    """
    player.heal(amount) # Already handles health overflow logic
    return None


def mana_restore(player: "Player", amount: int) -> None:
    """
    Restore the player's mana by a certain amount. 
        :param player: The player to restore mana for.
        :param amount: The amount to restore the player's mana by.
    """
    player.mana = min(player.max_mana, player.mana + amount)
    return None

def stat_boost(player: "Player", amount: int, stat: Literal["attack", "defense", "max_health", "max_mana"]) -> None:
    """
    Boost a player's stat by a certain amount.
        :param player: The player to boost.
        :param amount: The amount to boost the player's stat by.
        :param stat: The stat to boost. Should be one of 'attack', 'defense', 'max_health', 'max_mana'.
    """
    setattr(player, stat, getattr(player, stat) + amount)
    return None


SECTION_ONE_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon(
        name="Training Sword", 
        description="It's a sword, but not a very good one.", 
        boost_range=(3, 7)
        ): 0.44,
    Weapon(
        name="Rusty Sword", 
        description="A subpar sword.", 
        boost_range=(5, 10)
        ): 0.3,
    Weapon(
        name="Iron Sword", 
        description="A sturdy iron sword.", 
        boost_range=(8, 15)
        ): 0.2,
    Weapon(
        name="Steel Sword", 
        description="A sharp steel sword, fit for a knight.", 
        boost_range=(12, 20)
        ): 0.05,
    Weapon(
        name="Enchanted Sword", 
        description="A sword, imbued with magic.", 
        boost_range=(15, 25)
        ): 0.01
}

SECTION_ONE_ARMOR = { # <Armor>: <Weighted Chance>
    Armor(
        name="Leather Armor", 
        description="Basic leather armor.",
        boost_range=(3, 7)
        ): 0.39,
    Armor(
        name="Chainmail Armor", 
        description="Capable of stopping arrows, but not much more.",
        boost_range=(5, 10)
        ): 0.3,
    Armor(
        name="Plate Armor", 
        description="Of course massive metal plates will protect you.",
        boost_range=(8, 15)
        ): 0.2,
    Armor(
        name="Dragon Scale Armor", 
        description="A set of armor said to be made from dragon scales.",
        boost_range=(12, 20)
        ): 0.1,
    Armor(
        name="Mystic Armor", 
        description="Although designed for mages, it presents a suprisingly high resistance to physical damage.",
        boost_range=(15, 25)
        ): 0.01
}

SECTION_ONE_CONSUMABLES = { # <Consumable>: <Weighted Chance>
    Consumable(
        name="Scroll of Healing <Tier 1>", 
        description="A scroll that heals you for 50 health.", 
        effect=partial(heal, amount=50)
    ): 0.25,
    Consumable(
        name="Scroll of Mana <Tier 1>", 
        description="A scroll that restores 50 mana.", 
        effect=partial(mana_restore, amount=50)
    ): 0.25,
    Consumable(
        name="Scroll of Strength <Tier 1>", 
        description="A scroll that permanently boosts attack by 2.",
        effect=partial(stat_boost, amount=2, stat="attack")
    ): 0.2,
    Consumable(
        name="Scroll of Defense <Tier 1>", 
        description="A scroll that permanently boosts defense by 2.",
        effect=partial(stat_boost, amount=2, stat="defense")
    ): 0.2,
    Consumable(
        name="Juggernaut's Blood <Tier 1>", 
        description="It seems to have the potential to increase one's health.",
        consume_msg=f"{Styles.fg.lightgreen}You drink the blood. A rush of vitality flows through you. (+20 Max HP){Styles.reset}",
        effect=partial(stat_boost, amount=20, stat="max_health")
    ): 0.05,
    Consumable(
        name="Ancient Writings <Tier 1>", 
        description="A musty page filled with scribbles. Perhaps it can increase one's mana?",
        consume_msg=f"{Styles.fg.lightgreen}You attempt to read the page. You understand nothing, yet you feel a surge of magic within. (+20 Max MP){Styles.reset}",
        effect=partial(stat_boost, amount=20, stat="max_mana")
    ): 0.05
}

SECTION_TWO_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon(
        name="Frostbite | <Tier 2>",
        description="A cursed sword that freezes wounds, leaving victims brittle.",
        boost_range=(15, 17)
    ): 0.3,
    Weapon(
        name="Duskfang | <Tier 2>",
        description="A dagger, perfect for an assassination.",
        boost_range=(15, 20)
    ): 0.3,
    Weapon(
        name="Dawnbringer | <Tier 2>",
        description="A greatsword with the radiance of the sun.",
        boost_range=(10, 25)
    ): 0.3,
    Weapon(
        name="Shadow Blade | <Tier 2>",
        description="It seems to have been forged with pure darkness.",
        boost_range=(30, 32)
    ): 0.05,
    Weapon(
        name="Holy Avenger | <Tier 2>",
        description="A pure holy light emanates from the sword.",
        boost_range=(25, 40)
    ): 0.05
}

SECTION_TWO_ARMOR = { # <Armor>: <Weighted Chance>
    Armor(
        name="Whisperweave Cloak | <Tier 2>",
        description="A cloak that muffles sound, making the wearer nearly silent when moving.",
        boost_range=(10, 12)
    ): 0.3,
    Armor(
        name="Feywild Mantle | <Tier 2>",
        description="A shimmering cape imbued with nature's grace.",
        boost_range=(8, 18)
    ): 0.3,
    Armor(
        name="Serpentscale Hauberk | <Tier 2>",
        description="A coat of overlapping metallic scales that slithers to deflect blows.",
        boost_range=(19, 40)
    ): 0.25,
    Armor(
        name="Dawnforged Plate | <Tier 2>",
        description="Armor that glows with the light of the rising sun, deterring undead and demons.",
        boost_range=(20, 28)
    ): 0.1,
    Armor(
        name="The Aegis of the Phoenix | <Tier 2>",
        description="Forged from the feathers of a phoenix, this cloak provides a startlingly high defense for bird feathers.",
        boost_range=(30, 40)
    ): 0.05
}

SECTION_TWO_SCROLLS = { # <Consumable>: <Weighted Chance>
    Consumable(
        name="Scroll of Healing | <Tier 2>", 
        description="A scroll that heals you for 100 health.", 
        effect=partial(heal, amount=100)
    ): 0.25,
    Consumable(
        name="Scroll of Mana | <Tier 2>", 
        description="A scroll that restores 100 mana.", 
        effect=partial(mana_restore, amount=100)
    ): 0.25,
    Consumable(
        name="Scroll of Strength | <Tier 2>", 
        description="A scroll that permanently boosts attack by 5.",
        effect=partial(stat_boost, amount=5, stat="attack")
    ): 0.2,
    Consumable(
        name="Scroll of Defense | <Tier 2>", 
        description="A scroll that permanently boosts defense by 5.",
        effect=partial(stat_boost, amount=5, stat="defense")
    ): 0.2,
    Consumable(
        name="Liquid Lightning | <Tier 2>", 
        description="A vial of liquid lightning. It's rumored to increase strength, but maybe it'd be a good idea to not drink lightning?",
        consume_msg=f"{Styles.fg.lightgreen}You drink the blood. A rush of vitality flows through you. (+10 Attack){Styles.reset}",
        effect=partial(stat_boost, amount=10, stat="attack")
    ): 0.05,
    Consumable(
        name="The Archmage's Book | <Tier 2> ", 
        description="A book owned by a powerful archmage.",
        consume_msg=f"{Styles.fg.lightgreen}You flip open the book and see a child's picure book. Yet, knowledge of the arcane floods into you. (+50 Max MP){Styles.reset}",
        effect=partial(stat_boost, amount=50, stat="max_mana")
    ): 0.05
}

#_______________________________________________PLACEHOLDER____________________________________________________
SECTION_THREE_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon("Training Sword", "It's a sword, but not a very good one.", (3, 7)): 0.44,
    Weapon("Rusty Sword", "A subpar sword.", (5, 10)): 0.3,
    Weapon("Iron Sword", "A sturdy iron sword.", (8, 15)): 0.2,
    Weapon("Steel Sword", "A sharp steel sword, fit for a knight.", (12, 20)): 0.05,
    Weapon("Enchanted Sword", "A sword, imbued with magic.", (15, 25)): 0.01
}

SECTION_THREE_ARMOR = { # <Armor>: <Weighted Chance>
    Armor("Leather Armor", "Basic leather armor.", (3, 7)): 0.39,
    Armor("Chainmail Armor", "Capable of stopping arrows, but not much more.", (5, 10)): 0.3,
    Armor("Plate Armor", "Of course large metal plates can protect your body.", (8, 15)): 0.2,
    Armor("Dragon Scale Armor", "A set of armor said to be made from dragon scales.", (12, 20)): 0.1,
    Armor("Mystic Armor", "Although designed for mages, it suprisingly presents a high resistance to physical damage.", (15, 25)): 0.01
}

SECTION_THREE_SCROLLS = { # <Consumable>: <Weighted Chance>
    Consumable("Scroll of Healing", "A scroll that heals you for 50 health.", partial(heal, amount=50)): 0.4,
    Consumable("Scroll of Mana", "A scroll that restores 50 mana.", partial(mana_restore, amount=50)): 0.3,
    # No skill scrolls in section one
}
#_____________________________________________PLACEHOLDER____________________________________________________
SECTION_FOUR_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon("Training Sword", "It's a sword, but not a very good one.", (3, 7)): 0.44,
    Weapon("Rusty Sword", "A subpar sword.", (5, 10)): 0.3,
    Weapon("Iron Sword", "A sturdy iron sword.", (8, 15)): 0.2,
    Weapon("Steel Sword", "A sharp steel sword, fit for a knight.", (12, 20)): 0.05,
    Weapon("Enchanted Sword", "A sword, imbued with magic.", (15, 25)): 0.01
}

SECTION_FOUR_ARMOR = { # <Armor>: <Weighted Chance>
    Armor("Leather Armor", "Basic leather armor.", (3, 7)): 0.39,
    Armor("Chainmail Armor", "Capable of stopping arrows, but not much more.", (5, 10)): 0.3,
    Armor("Plate Armor", "Of course large metal plates can protect your body.", (8, 15)): 0.2,
    Armor("Dragon Scale Armor", "A set of armor said to be made from dragon scales.", (12, 20)): 0.1,
    Armor("Mystic Armor", "Although designed for mages, it suprisingly presents a high resistance to physical damage.", (15, 25)): 0.01
}

SECTION_FOUR_SCROLLS = { # <Consumable>: <Weighted Chance>
    Consumable("Scroll of Healing", "A scroll that heals you for 50 health.", partial(heal, amount=50)): 0.4,
    Consumable("Scroll of Mana", "A scroll that restores 50 mana.", partial(mana_restore, amount=50)): 0.3,
    # No skill scrolls in section one
}


SECTION_ONE_ITEMS = [ # <Weighted Chance>: <Category>
    SECTION_ONE_WEAPONS,
    SECTION_ONE_ARMOR,
    SECTION_ONE_CONSUMABLES,
]

SECTION_TWO_ITEMS = [
    SECTION_TWO_WEAPONS,
    SECTION_TWO_ARMOR,
    SECTION_TWO_SCROLLS,
]

SECTION_THREE_ITEMS = [
    SECTION_THREE_WEAPONS,
    SECTION_THREE_ARMOR,
    SECTION_THREE_SCROLLS,
]

SECTION_FOUR_ITEMS = [
    SECTION_FOUR_WEAPONS,
    SECTION_FOUR_ARMOR,
    SECTION_FOUR_SCROLLS,
]