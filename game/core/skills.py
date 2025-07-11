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

from .status_effects import StatusEffect, status_effects
from ..utils import SkillTarget

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .entities import Entity, Player, Ally, Enemy

class Skill:
    def __init__(self, name: str, description: str, power: int, 
                 mana_cost: int, target: SkillTarget, accuracy: float = 1.0,
                 effect: Optional[StatusEffect] = None):
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
                    damage = max(1, user.attack + self.power)
                    damage = target.take_damage(damage)
                    results.append(f"{user.name} uses {self.name} on {target.name} for {damage} damage!")
                elif self.target in [SkillTarget.SELF, SkillTarget.SINGLE_ALLY, SkillTarget.ALL_ALLIES]:
                    heal_amount = self.power + (user.defense // 2)
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





# The list of skills that any entity can use
GENERAL_SKILLS = [
    Skill("Tester", "", 10000000, 0, SkillTarget.ALL_ENEMIES),
    Skill("Basic Attack", "A simple attack", 5, 0, SkillTarget.SINGLE_ENEMY, 0.1),
    Skill("Power Strike", "A powerful strike", 15, 10, SkillTarget.SINGLE_ENEMY),
    Skill("God of gambling", "Good Luck!", rand.randint(-1000, 1000), rand.randint(0, 100), rand.choice(list(SkillTarget)), rand.random(), rand.choice(list(status_effects.values())))
]
WARRIOR_SKILLS = [
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),

]

MAGE_SKILLS = [
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),

]

ROGUE_SKILLS = [
    #TODO
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY),
]

PRIEST_SKILLS = [
    Skill("Holy Light", "A light that heals", 20, 15, SkillTarget.SINGLE_ALLY),
    Skill("Divine Shield", "Protects an ally from damage", 0, 20, SkillTarget.SINGLE_ALLY, effect=status_effects["shield"]),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY)
]

ENEMY_SKILLS = [
    #TODO
    Skill("Enemy Basic Attack", "A basic attack from an enemy", 1000000, 0, SkillTarget.SINGLE_ENEMY),
]
