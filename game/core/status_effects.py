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

from ..utils import print_error
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from .entities import Entity

class StatusEffect:
    def __init__(self, name:str, duration: int, effects: Callable) -> None:
        """
        :param duration: How many turns the StatusEffect will last for
        :param effects: Function that implements what the StatusEffect will do
        """
        self.name = name
        self._effects = effects
        self.duration = duration
        return None
    
    def apply(self, entity: 'Entity') -> None:
        """
        Apply the status effect to the entity. Should be called every turn while in combat
        :param entity: The entity to apply the status effect to.
        """
        if self.duration <= 0:
            print_error(f"{entity.name} is no longer {self.name.lower()}!")
            entity.effects.remove(self)
            return None
        self._effects(entity)
        print(f"{entity.name} is {self.name.lower()} for {self.duration} turns.")
        self.duration -= 1
        return None
        
