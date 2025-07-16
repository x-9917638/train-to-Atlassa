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

from ..utils import print_error, typing_print
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from .entities import Entity

class StatusEffect:
    def __init__(self, name:str, duration: int, effects: Callable, on_remove: Callable) -> None:
        """
        :param duration: How many turns the StatusEffect will last for
        :param effects: Function that implements what the StatusEffect will do
        :param reverse: Function that implements what the StatusEffect will do when it expires
        """
        self.name = name
        self._apply = effects
        self._remove = on_remove
        self.duration = duration
        return None
    
    def apply(self, entity: 'Entity') -> None:
        """
        Apply the status effect to the entity. Should be called every turn while in combat
            :param entity: The entity to apply the status effect to.
        """
        if self.duration <= 0:
            self.remove(entity)
            return None
        self._apply(entity)
        typing_print(f"{entity.name} is {self.name.lower()} for {self.duration} turns.")
        self.duration -= 1
        return None
    
    def remove(self, entity: 'Entity') -> None:
        """
        This is called when the status effect expires or is removed.
            :param entity: The entity to remove the status effect on.
        """
        self._remove(entity)
        typing_print(f"{entity.name} is no longer {self.name.lower()}!")
        entity.effects.remove(self)
        return None
        
