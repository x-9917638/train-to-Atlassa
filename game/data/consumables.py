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

from ..core.items import Consumable
from ..utils import Styles

from functools import partial
from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from ..core.entities import Player

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


SECTION_ONE_CONSUMABLES = { # <Consumable>: <Weighted Chance>
    Consumable(
        name="Scroll of Healing | <Tier 1>", 
        description="A scroll that heals you for 50 health.", 
        effect=partial(heal, amount=50)
    ): 0.25,
    Consumable(
        name="Scroll of Mana | <Tier 1>", 
        description="A scroll that restores 50 mana.", 
        effect=partial(mana_restore, amount=50)
    ): 0.25,
    Consumable(
        name="Scroll of Strength | <Tier 1>", 
        description="A scroll that permanently boosts attack by 2.",
        effect=partial(stat_boost, amount=2, stat="attack")
    ): 0.2,
    Consumable(
        name="Scroll of Defense | <Tier 1>", 
        description="A scroll that permanently boosts defense by 2.",
        effect=partial(stat_boost, amount=2, stat="defense")
    ): 0.2,
    Consumable(
        name="Juggernaut's Blood | <Tier 1>", 
        description="It seems to have the potential to increase one's health.",
        consume_msg=f"{Styles.fg.lightgreen}You drink the blood. A rush of vitality flows through you. (+20 Max HP){Styles.reset}",
        effect=partial(stat_boost, amount=20, stat="max_health")
    ): 0.05,
    Consumable(
        name="Ancient Writings | <Tier 1>", 
        description="A musty page filled with scribbles. Perhaps it can increase one's mana?",
        consume_msg=f"{Styles.fg.lightgreen}You attempt to read the page. You understand nothing, yet you feel a surge of magic within. (+20 Max MP){Styles.reset}",
        effect=partial(stat_boost, amount=20, stat="max_mana")
    ): 0.05
}

SECTION_TWO_CONSUMABLES = { # <Consumable>: <Weighted Chance>
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
        consume_msg=f"{Styles.fg.lightgreen}The lightning scalds your throat, evoking a rush of strength within you. (+10 Attack){Styles.reset}",
        effect=partial(stat_boost, amount=10, stat="attack")
    ): 0.05,
    Consumable(
        name="The Archmage's Book | <Tier 2> ", 
        description="A book owned by a powerful archmage.",
        consume_msg=f"{Styles.fg.lightgreen}You flip open the book. It's a typical children's picure book. Yet, knowledge of the arcane floods into you. (+50 Max MP){Styles.reset}",
        effect=partial(stat_boost, amount=50, stat="max_mana")
    ): 0.05
}

SECTION_THREE_CONSUMABLES = { # <Consumable>: <Weighted Chance>
    Consumable(
        name="Scroll of Healing | <Tier 3>", 
        description="A scroll that heals you for 200 health.", 
        effect=partial(heal, amount=200)
    ): 0.25,
    Consumable(
        name="Scroll of Mana | <Tier 3>", 
        description="A scroll that restores 200 mana.", 
        effect=partial(mana_restore, amount=200)
    ): 0.25,
    Consumable(
        name="Scroll of Strength | <Tier 3>", 
        description="A scroll that permanently boosts attack by 12.",
        effect=partial(stat_boost, amount=12, stat="attack")
    ): 0.2,
    Consumable(
        name="Scroll of Defense | <Tier 3>", 
        description="A scroll that permanently boosts defense by 12.",
        effect=partial(stat_boost, amount=12, stat="defense")
    ): 0.2,
    Consumable(
        name="Liquid Lightning | <Tier 3>", 
        description="A vial of liquid lightning. It's rumored to increase strength, but maybe it'd be a good idea to not drink lightning?",
        consume_msg=f"{Styles.fg.lightgreen}The lightning scalds your throat, evoking a rush of strength within you. (+10 Attack){Styles.reset}",
        effect=partial(stat_boost, amount=10, stat="attack")
    ): 0.05,
    Consumable(
        name="The Archmage's Book | <Tier 3> ", 
        description="A book owned by a powerful archmage.",
        consume_msg=f"{Styles.fg.lightgreen}You flip open the book. It's a typical children's picure book. Yet, knowledge of the arcane floods into you. (+50 Max MP){Styles.reset}",
        effect=partial(stat_boost, amount=50, stat="max_mana")
    ): 0.05
}