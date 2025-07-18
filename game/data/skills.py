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
    # Skill(
    #     name="Testing Skill",
    #     description="",
    #     power=99999999,
    #     mana_cost=0,
    #     target=SkillTarget.ALL_ENEMIES,
    # ),
    Skill(
        name="Basic Attack | <Tier 0>", 
        description="A basic attack that deals damage to a single enemy.", 
        power=40, 
        mana_cost=0, 
        target=SkillTarget.SINGLE_ENEMY
    ),
    Skill(
        name="Gambling Fever | <Tier ???>", 
        description="Good Luck!", 
        power=random.randint(-8000, 8000), 
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
        power=160,
        mana_cost=15,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.8,
    ),
    Skill(
        name="Power Strike | <Tier 1>",
        description="A powerful strike",
        power=120,
        mana_cost=10,
        target=SkillTarget.SINGLE_ENEMY,
    ),
    Skill(
        name="Slash | <Tier 1>",
        description="A quick sword attack.",
        power=64,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY
    ),
]

SECTION_TWO_WARRIOR: list[Skill] = [
    Skill(
        name="Heavy Blow | <Tier 2>",
        description="A powerful attack, utilising the weight of the weapon.",
        power=320,
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
        power=480,
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
        power=960,
        mana_cost=50,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="World Breaker | <Tier 4>",
        description="An all-out attack that deals heavy damage to one enemy, but leaves you with little defense.",
        power=1200,
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
        power=144,
        mana_cost=30,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["burn"]
    ),
    Skill(
        name="Magic Missile | <Tier 1>",
        description="A basic magical attack.",
        power=80,
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
        power=240,
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
        power=360,
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
        power=2400,
        mana_cost=200,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.75,
        effect=STATUS_EFFECTS["vulnerable"]
    ),
    Skill(
        name="Tsunami | <Tier 4>",
        description="Conjure enormous waves to wash away all enemies.",
        power=800,
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
        power=112,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY
    ),
    Skill(
        name="Throwing Knife | <Tier 1>",
        description="Throw a knife at an enemy.",
        power=160,
        mana_cost=5,
        target=SkillTarget.SINGLE_ENEMY
    ),
]

SECTION_TWO_ROGUE: list[Skill] = [
    Skill(
        name="Poison Strike | <Tier 2>",
        description="Attack with a poisoned blade.",
        power=176,
        mana_cost=15,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["poison"]
    ),
    Skill(
        name="Shadow Sneak | <Tier 2>",
        description="Melt into the shadows and appear behind an enemy, dealing massive damage if not spotted.",
        power=520,
        mana_cost=30,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.5
    ),
]

SECTION_THREE_ROGUE: list[Skill] = [
    Skill(
        name="Fan of Knives | <Tier 3>",
        description="Attack all enemies with thrown knives.",
        power=320,
        mana_cost=40,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="Ambush | <Tier 3>",
        description="Deal extra damage when attacking from stealth.",
        power=320,
        mana_cost=20,
        target=SkillTarget.SINGLE_ENEMY
    ),
]

SECTION_FOUR_ROGUE: list[Skill] = [
    Skill(
        name="Death Blooom | <Tier 4>",
        description="A deadly spinning attack that hits all enemies.",
        power=800,
        mana_cost=120,
        target=SkillTarget.ALL_ENEMIES
    ),
    Skill(
        name="Shadow Bomb | <Tier 4>",
        description="Engulf the battlefield in shadow, poisoning enemies.",
        power=640,
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

SECTION_ONE_PRIEST: list[Skill] = [
    Skill(
        name="Holy Light | <Tier 1>",
        description="A light that heals a single ally.",
        power=80,
        mana_cost=10,
        target=SkillTarget.SINGLE_ALLY
    ),
    Skill(
        name="Smite | <Tier 1>",
        description="A holy attack that deals damage to a single enemy.",
        power=100,
        mana_cost=8,
        target=SkillTarget.SINGLE_ENEMY
    ),
    Skill(
        name="Blessing | <Tier 1>",
        description="A blessing that increases an ally's defense.",
        power=0,
        mana_cost=5,
        target=SkillTarget.SINGLE_ALLY,
        effect=STATUS_EFFECTS["blessing"]
    ),
]

SECTION_TWO_PRIEST: list[Skill] = [
    Skill(
        name="Mass Heal | <Tier 2>",
        description="Heals all allies.",
        power=160,
        mana_cost=20,
        target=SkillTarget.ALL_ALLIES
    ),
    Skill(
        name="Divine Shield | <Tier 2>",
        description="Protects an ally from damage.",
        power=0,
        mana_cost=20,
        target=SkillTarget.SINGLE_ALLY,
        effect=STATUS_EFFECTS["shield"]
    ),
]

SECTION_THREE_PRIEST: list[Skill] = [
    Skill(
        name="Sanctuary | <Tier 3>",
        description="Heals and greatly reduces damage taken by all allies.",
        power=250,
        mana_cost=40,
        target=SkillTarget.ALL_ALLIES,
        effect=STATUS_EFFECTS["shield"]
    ),
    Skill(
        name="Purify | <Tier 3>",
        description="Removes all negative effects from an ally.",
        power=0,
        mana_cost=10,
        target=SkillTarget.SINGLE_ALLY,
        effect=STATUS_EFFECTS["purify"]
    ),
]

SECTION_FOUR_PRIEST: list[Skill] = [
    Skill(
        name="Full Heal | <Tier 4>",
        description="Heals a single ally to full health.",
        power=0,
        mana_cost=50,
        target=SkillTarget.SINGLE_ALLY,
        effect=STATUS_EFFECTS["full_heal"]
    ),
    Skill(
        name="Divine Retribution | <Tier 4>",
        description="Calls upon the wrath of the gods to punish those that are evil.",
        power=600,
        mana_cost=100,
        target=SkillTarget.ALL_ENEMIES,
        effect=STATUS_EFFECTS["burn"]
    ),
]

PRIEST_SKILLS: dict[int, list[Skill]] = {
    1: SECTION_ONE_PRIEST,
    2: SECTION_TWO_PRIEST,
    3: SECTION_THREE_PRIEST,
    4: SECTION_FOUR_PRIEST,
}

SECTION_ONE_ENEMY: list[Skill] = [
    Skill(
        name="Enemy Basic Attack",
        description="A basic attack from an enemy",
        power=30,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.9
    ),
    Skill(
        name="Ambush | <Tier 1>",
        description="A surprise attack that deals extra damage.",
        power=60,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.6
    )
]

SECTION_TWO_ENEMY: list[Skill] = [
    Skill(
        name="Savage Bite",
        description="A vicious bite that deals heavy damage.",
        power=100,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.85
    ),
    Skill(
        name="Poison Spit",
        description="Spits poison at a single enemy, causing damage over time.",
        power=80,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY,
        effect=STATUS_EFFECTS["poison"],
        accuracy=0.8
    ),
]

SECTION_THREE_ENEMY: list[Skill] = [
    Skill(
        name="Howl",
        description="A terrifying howl that lowers all enemies' defenses.",
        power=0,
        mana_cost=0,
        target=SkillTarget.ALL_ENEMIES,
        effect=STATUS_EFFECTS["long_vulnerable"],
    ),
    Skill(
        name="Frenzy",
        description="Attack with a flurry of blows, dealing heavy damage to one enemy.",
        power=150,
        mana_cost=0,
        target=SkillTarget.SINGLE_ENEMY,
        accuracy=0.7
    ),
]

SECTION_FOUR_ENEMY: list[Skill] = [
    Skill(
        name="Dark Pulse",
        description="A wave of dark energy hits all enemies.",
        power=300,
        mana_cost=0,
        target=SkillTarget.ALL_ENEMIES,
        accuracy=0.75
    ),
]

ENEMY_SKILLS: dict[int, list[Skill]] = {
    1: SECTION_ONE_ENEMY,
    2: SECTION_TWO_ENEMY,
    3: SECTION_THREE_ENEMY,
    4: SECTION_FOUR_ENEMY,
}
