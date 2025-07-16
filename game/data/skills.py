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

from ..core.skills import Skill
from ..utils import SkillTarget
from .effects import STATUS_EFFECTS
import random

# The list of skills that any entity can use
GENERAL_SKILLS = [
    Skill("Tester", "", 10000000, 0, SkillTarget.ALL_ENEMIES),
    Skill("Basic Attack", "A simple attack", 5, 0, SkillTarget.SINGLE_ENEMY, 0.1),
    Skill("Power Strike", "A powerful strike", 15, 10, SkillTarget.SINGLE_ENEMY),
    Skill(
        name="God of gambling", 
        description="Good Luck!", 
        power=random.randint(-1000, 1000), 
        mana_cost=random.randint(0, 100), 
        target=random.choice(list(SkillTarget)), 
        accuracy=random.random(), 
        effect=random.choice(list(STATUS_EFFECTS.values()))
    )
]
WARRIOR_SKILLS = [
    Skill(
        name="Placeholder", 
        description="Placeholder", 
        power=0, 
        mana_cost=0, 
        target=SkillTarget.SINGLE_ENEMY
    ),
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
    Skill("Divine Shield", "Protects an ally from damage", 0, 20, SkillTarget.SINGLE_ALLY, effect=STATUS_EFFECTS["shield"]),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY)
]

ENEMY_SKILLS = [
    #TODO
    Skill("Enemy Basic Attack", "A basic attack from an enemy", 1000000, 0, SkillTarget.SINGLE_ENEMY, 0),
]
