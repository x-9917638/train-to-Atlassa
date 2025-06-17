"""Game Logic"""

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

from .core.entities import Player
from .core.floor import Floor
from .core.combat import CombatSystem

NAMES = [
    "Aelara", "Brialla", "Cyndra", "Drusila", "Elyndra",
    "Feyra", "Gwyneth", "Haelia", "Ilythia", "Jasmina",
    "Kythira", "Lunara", "Morgwen", "Nyssa", "Orianna",
    "Phaedra", "Quinnara", "Ravena", "Sylria", "Thalindra",
    "Aldric", "Baelthor", "Cedric", "Dain", "Eldrin",
    "Fenris", "Gorion", "Haldor", "Ithil", "Jorund",
    "Kael", "Lorath", "Maldrek", "Nyr", "Orin",
    "Parthas", "Quillon", "Ragnar", "Soren", "Thrain"
]

class Game:
    def __init__(self, player_name: str):
        self.player = Player(player_name)
        # Create 4 floors, maybe if i add an infinite mode this may need to be changed
        self.floors = [Floor(i+1) for i in range(4)]
        self.current_floor = self.floors[0]
        self.current_place = self.current_floor.places[0]
        self.game_over = False
        self.victory = False


    def move_player(self, place_index: int):
        try: # Account for player trying to move past the final room.
            self.current_place = self.current_floor.places[place_index]
            return (True, self.current_place)
        except IndexError:
            return (False, self.current_place)
    
    def handle_place_events(self):
        # Implementation of place events
        pass
    
    def initiate_combat(self):
        CombatSystem.start_combat()
    
    def handle_boss_defeat(self):
        # Implementation of boss defeat logic
        pass
