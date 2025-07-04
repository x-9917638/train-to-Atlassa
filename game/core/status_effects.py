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


class StatusEffect:
    def __init__(self, name:str, duration: int, effects, ) -> None:
        """
        :param duration: How many turns the StatusEffect will last for
        :param effects: Function that implements what the StatusEffect will do
        """
        self.name = name
        self._effects = effects
        self.duration = duration
    
    def apply(self, entity):
        """
        Apply the status effect to the player. Should be called every turn while in combat
        :param player: The player to apply the status effect to.
        """
        self._effects(entity)
        print(f"{entity.name} is {self.name.lower()} for {self.duration} turns.")
        self.duration -= 1
        

class DummyPlayer(object):
    def __init__(self, health: int) -> None:
        self.health = health

def shieled_effect(player):
    setattr(player, "defense", player.defense + 10) 
    setattr(player, "health", player.health + 50)


status_effects = {
    "poison": StatusEffect(
        name="Poisoned",
        duration=3,
        effects=lambda player: setattr(player, 'health', player.health - 5)
    ),
    "burn": StatusEffect(
        name="Burned",
        duration=2,
        effects=lambda player: setattr(player, 'health', player.health - 10)
    ),
    "weaken": StatusEffect(
        name="Weakened",
        duration=1,
        effects=lambda player: setattr(player, "attack", float("-inf"))
    ),
    "shield": StatusEffect(
        name="Shielded",
        duration=1,
        effects=shieled_effect
    )
}