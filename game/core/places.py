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

from .events import Event
from ..utils.enums import PlaceType
import random as rand

class Place:
    def __init__(self, place_type: PlaceType, name: str, possible_events:list[Event]=None):
        self.type = place_type
        self.name = name
        self.entities = []
        self.connected_places = []
        self.possible_events = possible_events
        self.visited = False

    def generate_entities(self):
        # Run this on place generation
        # To implement.
        # Randomly pick a bunch of stuff to have random enemies.
        # Call this on Fight and maybe Challenge places.
        pass

    def generate_events(self):
        # Run this on place generation
        pass

    def add_entity(self, entity):
        self.entities.append(entity)
    
    def add_connection(self, place):
        self.connected_places.append(place)
