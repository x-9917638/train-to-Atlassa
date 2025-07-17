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

from ..core.status_effects import StatusEffect
from ..utils import print_error, colorprint
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..core.entities import Entity


def shield_effect(entity: "Entity") -> None:
    entity.defense += 10
    entity.max_health += 50
    entity.health += 50 
    colorprint(f"{entity.name} is shielded and gains 50 health and 10 defense!", "green")
    return None

def shield_remove(entity: "Entity") -> None:
    entity.defense -= 10
    entity.max_health -= min(entity.max_health - 1, 50)  # Prevents going below 1 health
    entity.health -= min(entity.health - 1, 50)
    colorprint(f"{entity.name}'s shield has worn off and they lose 50 health and 10 defense.", "red")
    return None


def poison_effect(entity: "Entity") -> None:
    entity.health -= 15
    print_error(f"{entity.name} is poisoned and loses 5 health! Current health: {entity.health}")
    return None

def poison_remove(entity: "Entity") -> None:
    print_error(f"{entity.name} is no longer poisoned. Current health: {entity.health}")
    return None


def burn_effect(entity: "Entity") -> None:
    entity.health -= 25
    print_error(f"{entity.name} is burned and loses 10 health! Current health: {entity.health}")
    return None

def burn_reverse(entity: "Entity") -> None:
    colorprint(f"{entity.name} is no longer burned.", "green")
    return None


def war_cry_effect(entity: "Entity") -> None:
    entity.attack += 5
    entity.defense += 5
    colorprint(f"{entity.name} is motivated and gains 5 attack!", "yellow")
    return None

def war_cry_remove(entity: "Entity") -> None:
    entity.attack -= 10
    entity.defense -= 10
    colorprint(f"The war cry has worn off of {entity.name}...", "red")
    return None


def vulnerable_effect(entity: "Entity") -> None:
    entity.defense -= 30
    colorprint(f"{entity.name} has their defense lowered by 30...", "red")
    return None

def vulnerable_remove(entity: "Entity") -> None:
    entity.defense += 30
    colorprint(f"{entity.name} is no longer vulnerable.", "green")
    return None


def mana_restore_effect(entity: "Entity") -> None:
    entity.mana += 100
    if entity.mana > entity.max_mana:
        entity.mana = entity.max_mana
    colorprint(f"{entity.name} gained 100 mana! Current mana: {entity.mana}", "green")
    return None


def frostbite_effect(entity: "Entity") -> None:
    entity.health -= 12
    colorprint(f"{entity.name} is frostbitten and takes 8 damage!", "red")
    return None

def frostbite_remove(entity: "Entity") -> None:
    colorprint(f"{entity.name} thawed out.", "green")
    return None


def purify_effect(entity: "Entity") -> None:
    entity.effects = []
    colorprint(f"{entity.name} has been purified and all status effects have been removed!", "green")
    return None

def purify_remove(entity: "Entity") -> None: # Param here is just for type hints to not scream at me
    # No need to do anything
    return None


def full_heal_effect(entity: "Entity") -> None:
    entity.health = entity.max_health
    colorprint(f"{entity.name} has been fully healed!", "green")
    return None

def full_heal_remove(entity: "Entity") -> None: # Param here is just for type hints to not scream at me
    # No need to do anything
    return None


def blessing_effect(entity: "Entity") -> None:
    entity.defense += 10
    colorprint(f"{entity.name} is blessed by the gods and gains 10 defense!", "green")
    return None

def blessing_remove(entity: "Entity") -> None:
    entity.defense -= 30
    colorprint(f"{entity.name}'s blessing has worn off and they lose 30 defense.", "red")
    return None


STATUS_EFFECTS = {
    "poison": StatusEffect(
        name="Poisoned",
        duration=3,
        effects=poison_effect,
        on_remove=poison_remove
    ),
    "burn": StatusEffect(
        name="Burned",
        duration=2,
        effects=burn_effect,
        on_remove=burn_reverse
    ),
    "shield": StatusEffect(
        name="Shielded",
        duration=1,
        effects=shield_effect,
        on_remove=shield_remove
    ),
    "war_cry": StatusEffect(
        name="Motivated",
        duration=2,
        effects=war_cry_effect,
        on_remove=war_cry_remove
    ),
    "vulnerable": StatusEffect(
        name="Vulnerable",
        duration=1,
        effects=vulnerable_effect,
        on_remove=vulnerable_remove
    ),
    "mana_restore": StatusEffect(
        name="Mana Restore",
        duration=1,
        effects=mana_restore_effect,
        on_remove=lambda _: None # Do nothing
    ),
    "frostbite": StatusEffect(
        name="Frostbite",
        duration=4,
        effects=frostbite_effect,
        on_remove=frostbite_remove
    ),
    "purify": StatusEffect(
        name="Purified",
        duration=1,
        effects=purify_effect,
        on_remove=purify_remove
    ),
    "full_heal": StatusEffect(
        name="Full Heal",
        duration=1,
        effects=full_heal_effect,
        on_remove=full_heal_remove
    ),
    "blessing": StatusEffect(
        name="Blessed",
        duration=3,
        effects=blessing_effect,
        on_remove=blessing_remove
    ),
    "long_vulnerable": StatusEffect(
        name="Vulnerable",
        duration=3,
        effects=vulnerable_effect,
        on_remove=vulnerable_remove
    ),
}