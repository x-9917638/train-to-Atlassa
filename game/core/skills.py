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

import random as rand

from ..utils import SkillTarget

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .entities import Entity, Player, Ally, Enemy
    from .status_effects import StatusEffect

class Skill:
    def __init__(self, name: str, description: str, power: int, 
                 mana_cost: int, target: SkillTarget, accuracy: float = 1.0,
                 effect: Optional['StatusEffect'] = None):
        self.name = name
        self.description = description
        self.power = power
        self.mana_cost = mana_cost
        self.target = target
        self.accuracy = accuracy
        self.effect = effect
    
    def use(self, user: "Player | Ally | Enemy", targets: list["Entity"]) -> tuple[str, bool]:
        hit, miss = True, False
        if user.mana < self.mana_cost:
            return f"Not enough mana to use {self.name}!", miss
        
        user.mana -= self.mana_cost
        
        if rand.random() < self.accuracy:
            results = []
            for target in targets:
                if self.target in [SkillTarget.SINGLE_ENEMY, SkillTarget.ALL_ENEMIES]:
                    damage = (user.attack // 4) * self.power
                    damage = target.take_damage(damage)
                    results.append(f"{user.name} uses {self.name} on {target.name} for {damage} damage!")
                elif self.target in [SkillTarget.SELF, SkillTarget.SINGLE_ALLY, SkillTarget.ALL_ALLIES]:
                    heal_amount = self.power * (user.defense // 2)
                    actual_heal = target.heal(heal_amount)
                    results.append(f"{user.name} uses {self.name} on {target.name}, healing {actual_heal} health!")

            if self.effect:
                for target in targets:
                    target.effects.append(self.effect)
                    results.append(f"{target.name} is now {self.effect.name}!")

            return "\n".join(results), hit
        return (_attack_miss_message(user.name), miss)
    

def _attack_miss_message(name: str) -> str:
    """Returns a random attack missed message."""
    messages = [
        f"{name} misses, and accidentally hits a nearby seat. The seat is unimpressed.",
        f"{name} swings their weapon, but it gets stuck in the ground. Now they're just standing there awkwardly.",
        f"{name} tries to attack, but their weapon slips from their hands and lands in a nearby pond. Good job.",
        f"{name} charges at the enemy, but they trip over their feet and fall flat. The enemy laughs.",
        f"{name} attempts a strike, but their weapon bounces off the enemy's armor and hits them in the face. Ouch."
    ]
    return rand.choice(messages)

