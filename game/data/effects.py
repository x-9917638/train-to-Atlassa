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
    setattr(entity, "defense", entity.defense + 10) 
    setattr(entity, "health", entity.health + 50)
    colorprint(f"{entity.name} is shielded and gains 50 health and 10 defense!", "green")
    return None


def poison_effect(entity: "Entity") -> None:
    entity.health -= 5
    print_error(f"{entity.name} is poisoned and loses 5 health! Current health: {entity.health}")
    return None


def burn_effect(entity: "Entity") -> None:
    entity.health -= 10
    print_error(f"{entity.name} is burned and loses 10 health! Current health: {entity.health}")
    return None


STATUS_EFFECTS = {
    "poison": StatusEffect(
        name="Poisoned",
        duration=3,
        effects=poison_effect
    ),
    "burn": StatusEffect(
        name="Burned",
        duration=2,
        effects=burn_effect
    ),
    "shield": StatusEffect(
        name="Shielded",
        duration=1,
        effects=shield_effect
    )
}