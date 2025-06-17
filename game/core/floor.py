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

import random
from ..utils.enums import PlaceType
from .places import Place

class Floor:
    def __init__(self, floor_number: int):
        self.number = floor_number
        self.places = []
        self.generate_floor()
    
    def generate_floor(self):
        # Create the guaranteed home place
        home = Place(PlaceType.HOME, f"Floor {self.number} Home")
        self.places.append(home)
        
        # Generate other places
        self._generate_other_places()
        
        # Create the guaranteed boss room
        boss_room = Place(PlaceType.BOSS, f"Floor {self.number} Boss Room")
        self.places.append(boss_room)

        # Connect places
        self._connect_places()
    
    def _generate_other_places(self):
        num_places = random.randint(4, 6)
        place_types = [PlaceType.REST, PlaceType.FIGHT, PlaceType.CHALLENGE]
        weights = [0.3, 0.5, 0.2] # Might be too hard rn?
        
        for i in range(num_places):
            place_type = random.choices(place_types, k=1, weights=weights)[0]
            place = Place(place_type, f"Floor {self.number} {place_type.value} {i+1}")
            self.places.append(place)
    
    def _connect_places(self):
        for i in range(len(self.places) - 1):
            self.places[i].add_connection(self.places[i+1])
        self.places[-2].add_connection(self.places[-1])
