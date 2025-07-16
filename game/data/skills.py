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

GENERAL_SKILLS = [
    Skill(
        name="Basic Attack | <Tier 0>", 
        description="A basic attack that deals damage to a single enemy.", 
        power=5, 
        mana_cost=0, 
        target=SkillTarget.SINGLE_ENEMY
    ),
    Skill(
        name="God of gambling | <Tier ???>", 
        description="Good Luck!", 
        power=random.randint(-1000, 1000), 
        mana_cost=random.randint(0, 100), 
        target=random.choice(list(SkillTarget)), 
        accuracy=random.random(), 
        effect=random.choice(list(STATUS_EFFECTS.values()))
    )
]

SECTION_ONE_WARRIOR: list[Skill] = [
    Skill(
        name="Bash | <Tier 1>",
        description="A powerful bash",
        power=20,
        mana_cost=15,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.8,
    ),
    Skill(
        name="Power Strike | <Tier 1>",
        description="A powerful strike",
        power=15,
        mana_cost=10,
        target=SkillTarget.SINGLE_ENEMY,
    ),
    Skill(
        name="Slash | <Tier 1>",
        description="A quick sword attack.",
        power=8,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY
    ),
]

SECTION_TWO_WARRIOR: list[Skill] = [
    Skill(
        name="Heavy Blow | <Tier 2>",
        description="A powerful attack, utilising the weight of the weapon.",
        power=40,
        mana_cost=20,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.85
    ),
    Skill(
        name="Guard | <Tier 2>",
        description="Raise your defense and health for a short time.",
        power=0,
        mana_cost=10,
        target=SkillTarget.SELF,
        effect=STATUS_EFFECTS["shield"]
    ),
]

SECTION_THREE_WARRIOR: list[Skill] = [
    Skill(
        name="Whirlwind | <Tier 3>",
        description="Attack all enemies with spinning blades.",
        power=60,
        mana_cost=40,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="War Cry | <Tier 3>",
        description="A rousing battle cry that boosts your allies' spirits.",
        power=0,
        mana_cost=40,
        target=SkillTarget.ALL_ALLIES,
        effect=STATUS_EFFECTS["war_cry"]
    ),
]

SECTION_FOUR_WARRIOR: list[Skill] = [
    Skill(
        name="Earthshaker | <Tier 4>",
        description="Devastating attack that hits all enemies and may lower their defense.",
        power=120,
        mana_cost=50,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="World Breaker | <Tier 4>",
        description="An all-out attack that deals heavy damage to one enemy, but leaves you with little defense.",
        power=150,
        mana_cost=120,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["vulnerable"],
        accuracy=0.75
    )

]

WARRIOR_SKILLS: dict[int, list[Skill]] = {
    1: SECTION_ONE_WARRIOR,
    2: SECTION_TWO_WARRIOR,
    3: SECTION_THREE_WARRIOR,
    4: SECTION_FOUR_WARRIOR,
}

SECTION_ONE_MAGE: list[Skill] = [
    Skill(
        name="Firebolt | <Tier 1>",
        description="A small bolt of fire that hits a single enemy.",
        power=18,
        mana_cost=30,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["burn"]
    ),
    Skill(
        name="Magic Missile | <Tier 1>",
        description="A basic magical attack.",
        power=10,
        mana_cost=16,
        target=SkillTarget.SINGLE_ENEMY
    ),
    Skill(
        name="Arcane Shield | <Tier 1>",
        description="Protect yourself with a magical barrier.",
        power=0,
        mana_cost=20,
        target=SkillTarget.SELF,
        effect=STATUS_EFFECTS["shield"]
    ),
]

SECTION_TWO_MAGE: list[Skill] = [
    Skill(
        name="Ice Shard | <Tier 2>",
        description="Launch a shard of ice at the enemy.",
        power=30,
        mana_cost=40,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["frostbite"]
    ),
    Skill(
        name="Mana Surge | <Tier 2>",
        description="Restore 100 mana.",
        power=0,
        mana_cost=0,
        target=SkillTarget.SELF,
        effect=STATUS_EFFECTS["mana_restore"]
    ),
]

SECTION_THREE_MAGE: list[Skill] = [
    Skill(
        name="Chain Lightning | <Tier 3>",
        description="Lightning arcs between multiple enemies.",
        power=45,
        mana_cost=100,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="Aqua Bullet | <Tier 3>",
        description="A highly compressed ball of water that deals high damage, but at the cost of accuracy.",
        power=0,
        mana_cost=25,
        target=SkillTarget.SELF,
        accuracy=0.7
    ),
]

SECTION_FOUR_MAGE: list[Skill] = [
    Skill(
        name="Meteor | <Tier 4>",
        description="Call down a meteor to devastate an enemy, but leaves one vulnerable.",
        power=300,
        mana_cost=200,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.75,
        effect=STATUS_EFFECTS["vulnerable"]
    ),
    Skill(
        name="Tsunami | <Tier 4>",
        description="Conjure enormous waves to wash away all enemies.",
        power=100,
        mana_cost=300,
        target=SkillTarget.ALL_ENEMIES
    ),
]

MAGE_SKILLS: dict[int, list[Skill]] = {
    1: SECTION_ONE_MAGE,
    2: SECTION_TWO_MAGE,
    3: SECTION_THREE_MAGE,
    4: SECTION_FOUR_MAGE,
}

SECTION_ONE_ROGUE: list[Skill] = [
    Skill(
        name="Quick Stab | <Tier 1>",
        description="A fast, precise attack.",
        power=14,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY
    ),
    Skill(
        name="Throwing Knife | <Tier 1>",
        description="Throw a knife at an enemy.",
        power=20,
        mana_cost=5,
        target=SkillTarget.SINGLE_ENEMY
    ),
]

SECTION_TWO_ROGUE: list[Skill] = [
    Skill(
        name="Poison Strike | <Tier 2>",
        description="Attack with a poisoned blade.",
        power=22,
        mana_cost=15,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["poison"]
    ),
    Skill(
        name="Shadow Sneak | <Tier 2>",
        description="Melt into the shadows and appear behind an enemy, dealing massive damage if not spotted.",
        power=65,
        mana_cost=30,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.5
    ),
]

SECTION_THREE_ROGUE: list[Skill] = [
    Skill(
        name="Fan of Knives | <Tier 3>",
        description="Attack all enemies with thrown knives.",
        power=40,
        mana_cost=40,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="Ambush | <Tier 3>",
        description="Deal extra damage when attacking from stealth.",
        power=40,
        mana_cost=20,
        target=SkillTarget.SINGLE_ENEMY
    ),
]

SECTION_FOUR_ROGUE: list[Skill] = [
    Skill(
        name="Death Blooom | <Tier 4>",
        description="A deadly spinning attack that hits all enemies.",
        power=100,
        mana_cost=120,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="Shadow Bomb | <Tier 4>",
        description="Engulf the battlefield in shadow, poisoning enemies.",
        power=80,
        mana_cost=120,
        target=SkillTarget.ALL_ENEMIES,
        effect=STATUS_EFFECTS["poison"]
    ),
]

ROGUE_SKILLS: dict[int, list[Skill]] = {
    1: SECTION_ONE_ROGUE,
    2: SECTION_TWO_ROGUE,
    3: SECTION_THREE_ROGUE,
    4: SECTION_FOUR_ROGUE,
}

PRIEST_SKILLS = [
    Skill("Holy Light", "A light that heals", 20, 15, SkillTarget.SINGLE_ALLY),
    Skill("Divine Shield", "Protects an ally from damage", 0, 20, SkillTarget.SINGLE_ALLY, effect=STATUS_EFFECTS["shield"]),
    Skill("Placeholder", "Placeholder", 1000, 0, SkillTarget.SINGLE_ENEMY)
]

ENEMY_SKILLS = [
    #TODO
    Skill("Enemy Basic Attack", "A basic attack from an enemy", 1000000, 0, SkillTarget.SINGLE_ENEMY, 0),
]
