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

from typing import List, Tuple, Optional
from ..utils.enums import SkillTarget
from enum import Enum

class Skill:
    def __init__(self, name: str, description: str, power: int, 
                 mana_cost: int, target: SkillTarget, 
                 effect: Optional[str] = None):
        self.name = name
        self.description = description
        self.power = power
        self.mana_cost = mana_cost
        self.target = target
        self.current_cooldown = 0
        self.effect = effect
    
    def use(self, user, targets: List) -> Tuple[str, bool]:
        """Returns (result_message, was_successful)"""
        if user.mana < self.mana_cost:
            return f"Not enough mana to use {self.name}!", False
        
        user.mana -= self.mana_cost
        
        results = []
        for target in targets:
            if self.target in [SkillTarget.SINGLE_ENEMY, SkillTarget.ALL_ENEMIES]:
                damage = max(1, (user.attack + self.power) - (target.defense // 2))
                actual_damage = target.take_damage(damage)
                results.append(f"{user.name} uses {self.name} on {target.name} for {actual_damage} damage!")
            elif self.target in [SkillTarget.SELF, SkillTarget.SINGLE_ALLY, SkillTarget.ALL_ALLIES]:
                heal_amount = self.power + (user.defense // 2)
                actual_heal = target.heal(heal_amount)
                results.append(f"{user.name} uses {self.name} on {target.name} healing {actual_heal} health!")
        
        if self.effect:
            for target in targets:
                results.append(f"{target.name} is now {self.effect}!")
        
        return "\n".join(results), True
    
    def __str__(self):
        # I didn't like seeing a random memory address.
        return self.name
    

# The list of hardcoded skills that players / enemy can use
Skills = {
    "Basic Attack": Skill("Basic Attack", "A simple attack", 5, 0, SkillTarget.SINGLE_ENEMY),
    "Power Strike": Skill("Power Strike", "A powerful strike", 15, 10, SkillTarget.SINGLE_ENEMY)
}
