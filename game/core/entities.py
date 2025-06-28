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

from .items import Item
from .skills import Skill, GENERAL_SKILLS, ENEMY_SKILLS, WARRIOR_SKILLS, MAGE_SKILLS, ROGUE_SKILLS, PRIEST_SKILLS, RANGER_SKILLS
from..utils.enums import Professions
import random, math

class Entity:
    def __init__(self, name: str, health: int, attack: int, defense: int):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.skills: list[Skill] = []
        self.effects = {} # Status effects
    
    def take_damage(self, amount: int) -> int:
        """Calculate the damage the character takes, after defense."""
        actual_damage = max(1, amount - self.defense)
        assert isinstance(actual_damage, int) # Make sure that it stays an integer after calculations
        self.health -= actual_damage
        return actual_damage
    
    def heal(self, amount: int) -> int:
        heal_amount = min(amount, self.max_health - self.health)
        assert isinstance(heal_amount, int) # Make sure that it stays an integer after calculations
        self.health += heal_amount
        return heal_amount
    
    def is_alive(self) -> bool:
        return self.health > 0



class Player(Entity):
    def __init__(self, name: str):
        super().__init__(name, 100, 5, 5) # Base player stats
        self.level = 1
        self.experience = 0
        self.max_mana = 50
        self.mana = 50
        self.current_floor = 0
        self.current_carriage = None
        self.armour = None
        self.weapon = None
        self.inventory: dict[Item, int] = {} # Should store {<Item.name>: <NumItems>}
        self.skills = [
            # Player default skills
            GENERAL_SKILLS["Basic Attack"], 
            GENERAL_SKILLS["Power Strike"]
        ]
        self.skill_hand: list[Skill] = []
        self.profession = None
    

    def add_skills_to_deck(self, skills:list[Skill]):
        self.skills.extend(skills)
    

    def draw_skills(self, num: int = 1) -> list[Skill]:
        available_skills = [skill for skill in self.skills if skill not in self.skill_hand] # Make sure we do not draw dupes
        if len(available_skills):
        # If there aren't any skills to draw, don't draw.
            drawn = random.sample(available_skills, num)
            self.skill_hand.extend(drawn)
        else: drawn = []
        return drawn
    

    def discard_skill(self, skill: Skill):
        if skill in self.skill_hand:
            self.skill_hand.remove(skill)
    
    
    def rest(self):
        # When a player rests, they do not attack. 
        # Instead, they refresh skill cooldowns, heal, and generate mana
        self.mana += min(math.ceil(0.2 * self.max_mana), (self.max_mana - self.mana)) 
        self.health += min(math.floor(0.1 * self.max_health), (self.max_health - self.health))

class Enemy(Entity):
    def __init__(self, name: str, description: str, health: int, attack: int, defense: int, num_skills):
        super().__init__(name, health, attack, defense)
        self.mana = 999999 # Set to 999999 so that enemies can use Skill class methods
        self.description = description
        self.skills = self.create_enemy_skills(num_skills)
    
    def create_enemy_skills(self, amount: int) -> list[Skill]:
        skills = random.choices(ENEMY_SKILLS, k=amount)
        return skills

class Ally(Entity):
    def __init__(self, name: str, health: int, attack: int, defense: int, profession: Professions):
        super().__init__(name, health, attack, defense)
        self.profession = profession

    def generate_skills(self):
        match self.profession:
            case Professions.WARRIOR:
                self.skills = [skill for skill in WARRIOR_SKILLS.values()]
            case Professions.MAGE:
                self.skills = [skill for skill in MAGE_SKILLS.values()]
            case Professions.ROGUE:
                self.skills = [skill for skill in ROGUE_SKILLS.values()]
            case Professions.PRIEST:
                self.skills = [skill for skill in PRIEST_SKILLS.values()]
            case Professions.RANGER:
                self.skills = [skill for skill in RANGER_SKILLS.values()]
            case _:
                raise ValueError(f"Unknown ally class: {self.ally_class}")
    
    