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
from typing import Optional # So I don't get annoying type hints
from ..utils.enums import SkillTarget

class Skill:
    def __init__(self, name: str, description: str, power: int, 
                 mana_cost: int, target: SkillTarget, accuracy: float = 1.0,
                 effect: Optional[str] = None):
        self.name = name
        self.description = description
        self.power = power
        self.mana_cost = mana_cost
        self.target = target
        self.accuracy = accuracy
        self.current_cooldown = 0
        self.effect = effect
    
    def use(self, user, targets: list) -> tuple[str, bool]:
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
                    results.append(f"{target.name} is now {self.effect}!")

            return "\n".join(results), hit
        return (attack_miss_message(user.name), miss)
    

def attack_miss_message(name: str) -> str:
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
GENERAL_SKILLS = {
    "Basic Attack": Skill("Basic Attack", "A simple attack", 5, 0, SkillTarget.SINGLE_ENEMY, 0.1),
    "Power Strike": Skill("Power Strike", "A powerful strike", 15, 10, SkillTarget.SINGLE_ENEMY),
    "Basic Heal": Skill("Prayer", "A simple prayer for divine assitance", 30, 30, SkillTarget.ALL_ALLIES)
}

WARRIOR_SKILLS = {
    #TODO
}

MAGE_SKILLS = {
    #TODO
}

ROGUE_SKILLS = {
    #TODO
}

PRIEST_SKILLS = {
    "Holy Light": Skill("Holy Light", "A light that heals", 20, 15, SkillTarget.SINGLE_ALLY),
    "Divine Shield": Skill("Divine Shield", "Protects an ally from damage", 0, 20, SkillTarget.SINGLE_ALLY, effect="shielded")
}

RANGER_SKILLS = {
    #TODO
}

ENEMY_SKILLS = {
    #TODO
}
