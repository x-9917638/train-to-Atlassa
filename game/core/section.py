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
import logging

logger = logging.getLogger(__name__)

class Section:
    def __init__(self, section_number: int):
        self.number: int = section_number
        self.carriages: list[Carriage] = []
        self.generate_section()
    

    def generate_section(self) -> None:
        logging.info(f"Starting generation of section {self.number}.")
        # Create the guaranteed home carriage
        home = Carriage(CarriageType.SAFE, f"Section {self.number} HOME Carriage", self.number)
        self.carriages.append(home)

        logging.debug(f"Home carriage created for section {self.number}.")
        # Generate other carriage
        self._generate_other_carriages()

        
        # Create the guaranteed boss
        boss = Carriage(CarriageType.BOSS, f"Section {self.number} BOSS Carriage", self.number)
        self.carriages.append(boss)

        logging.debug(f"Boss carriage created for section {self.number}.")

        # Connect carriages
        self._connect_carriages()
        
        logging.info(f"Section {self.number} generated with {len(self.carriages)} carriages.")
        return None
    
    
    def _generate_other_carriages(self) -> None:
        num_carriages = random.randint(4, 6)
        place_types = [CarriageType.ALLY, CarriageType.FIGHT, CarriageType.CHALLENGE]
        weights = [0.3, 0.5, 0.2]
        
        for i in range(num_carriages):
            carriage_type = random.choices(place_types, k=1, weights=weights)[0]
            carriage = Carriage(carriage_type, f"Section {self.number} Carriage {i+2}", self.number)
            self.carriages.append(carriage)

            logging.debug(f"Carriage {i+2} of type {carriage_type} created for section {self.number}.")
        
        
        return None


    def _connect_carriages(self) -> None:
        for i in range(len(self.carriages) - 1):
            self.carriages[i]._add_connection(self.carriages[i+1])
        self.carriages[-2]._add_connection(self.carriages[-1])
        return None
