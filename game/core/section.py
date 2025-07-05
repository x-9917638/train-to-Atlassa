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
from ..utils import CarriageType
from .carriages import Carriage

class Section:
    def __init__(self, section_number: int):
        self.number = section_number
        self.carriages = []
        self.generate_section()
    
    def generate_section(self):
        # Create the guaranteed home carriage
        home = Carriage(CarriageType.SAFE, f"Section {self.number} Carriage", self.number)
        self.carriages.append(home)
        
        # Generate other carriage
        self._generate_other_carriages()
        
        # Create the guaranteed boss
        boss = Carriage(CarriageType.BOSS, f"Section {self.number} Carriage", self.number)
        self.carriages.append(boss)

        # Connect carriages
        self._connect_carriages()
    
    def _generate_other_carriages(self):
        num_carriages = random.randint(4, 6)
        place_types = [CarriageType.REST, CarriageType.FIGHT, CarriageType.CHALLENGE]
        weights = [0.3, 0.5, 0.2] # Might be too hard rn?
        
        for i in range(num_carriages):
            carriage_type = random.choices(place_types, k=1, weights=weights)[0]
            carriage = Carriage(carriage_type, f"Section {self.number} Carriage {i+1}", self.number)
            self.carriages.append(carriage)
    
    def _connect_carriages(self):
        for i in range(len(self.carriages) - 1):
            self.carriages[i]._add_connection(self.carriages[i+1])
        self.carriages[-2]._add_connection(self.carriages[-1])
