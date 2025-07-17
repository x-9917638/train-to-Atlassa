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
from ..data.skills import GENERAL_SKILLS, ENEMY_SKILLS, WARRIOR_SKILLS, MAGE_SKILLS, ROGUE_SKILLS, PRIEST_SKILLS
from  ..utils import Professions

import random, math, logging, copy

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .carriages import Carriage
    from .items import Item, Weapon, Armor
    from .skills import Skill
    from .status_effects import StatusEffect
    from .entities import Ally

logger = logging.getLogger(__name__)

class Entity: # Abstract base class for all entities in the game
    def __init__(self, name: str, health: int, attack: int, defense: int):
        self.name: str = name
        self.max_health: int = health
        self.health: int = health
        self.attack: int = attack
        self.defense: int = defense
        self.mana: int = 0
        self.max_mana: int = 0
        self.skill_deck: list["Skill"] = []
        self.effects: list["StatusEffect"] = [] # Status effects
        self.profession: Optional[Professions] = None # Profession of the entity, if applicable
        self.section: int = 1
    
    def take_damage(self, amount: int) -> int:
        """Calculate the damage the character takes, after defense."""
        actual_damage: int = max(1, amount - self.defense // 3)
        self.health -= actual_damage
        return actual_damage
    
    def heal(self, amount: int) -> int:
        heal_amount: int = min(amount, self.max_health - self.health)
        self.health += heal_amount
        return heal_amount
    
    def is_alive(self) -> bool:
        return self.health > 0
    
    def _give_new_skills(self, num_skills: int) -> None:     
        if not self.profession:
            return None   
        profession_skills: dict[int, list["Skill"]] = copy.deepcopy(globals()[f"{self.profession.value.upper()}_SKILLS"]) 
        skill_pool: list["Skill"] = []
        for i in range(1, self.section + 1):
            skill_pool.extend(profession_skills[i])
        
        num_skills = min(num_skills, len(skill_pool))  # Ensure we don't try to get more skills than available

        self.skill_deck.extend(random.sample(skill_pool, k=num_skills))
        
        return None



class Player(Entity):
    def __init__(self, name: str):
        super().__init__(name, 100, 5, 5) # Base player stats
        self.level: int = 1
        self.experience: int = 0
        self.max_mana: int = 50
        self.mana: int = 50
        self.current_carriage: Optional["Carriage"] = None
        self.armor: Optional["Armor"] = None
        self.weapon: Optional["Weapon"] = None
        self.inventory: dict["Item", int] = {} # Should store {<Item.name>: <NumItems>}
        self.skill_deck: list["Skill"] = GENERAL_SKILLS.copy() # Start with some default skills
        self.skill_hand: list["Skill"] = []
        self.profession: Optional[Professions] = None
        self.allies: list[Ally] = []
    
    
    def add_ally(self, ally: "Ally") -> None:
        assert isinstance(ally, Ally), "Ally must be an instance of the Ally class.\nThis should never happen, please report this."
        self.allies.append(ally)
        ally.generate_skills()
        return None
    
    
    def add_skills_to_deck(self, skills:list["Skill"]) -> None:
        self.skill_deck.extend(skills)
        return None
    
    def add_item_to_inventory(self, item: "Item") -> None:
        logger.debug(f"Adding item {item.name} to inventory for player {self.name}.")
        self.inventory[item] = self.inventory.get(item, 0) + 1
    
    def remove_item_from_inventory(self, item: "Item") -> None:
        if self.inventory[item] > 1:
            self.inventory[item] -= 1
        else:
            del self.inventory[item]
        logger.debug(f"Removing item {item.name} from inventory for player {self.name}.")
        return None
    
    
    def draw_skills(self, num: int = 1) -> list["Skill"]:
        available_skills: list["Skill"] = [skill for skill in self.skill_deck if skill not in self.skill_hand] # Make sure we do not draw dupes
        if len(available_skills):
        # If there aren't any skills to draw, don't draw.
            drawn: list["Skill"] = random.sample(available_skills, num)
            self.skill_hand.extend(drawn)
        else: drawn = []
        return drawn
    
    
    def check_level_up(self) -> bool:
        if self.experience >= self.level * 30:
            self._level_up()
            return True
        return False

    
    def _level_up(self) -> None:
        overflow = self.experience - (self.level * 30)
        self.experience = overflow
        self.level += 1
        match self.profession:
            case Professions.WARRIOR:
                # High degense, high health
                self.max_health += random.randrange(70, 100)
                self.max_mana += random.randrange(10, 20)
                self.attack += random.randrange(1, 5)
                self.defense += random.randrange(5, 10)
            case Professions.MAGE:
                # High mana, High attack
                self.max_health += random.randrange(30, 60)
                self.max_mana += random.randrange(30, 50)
                self.attack += random.randrange(5, 10)
                self.defense += random.randrange(1, 5)
            case Professions.ROGUE:
                # High attack
                self.max_health += random.randrange(50, 80)
                self.max_mana += random.randrange(10, 20)
                self.attack += random.randrange(8, 15)
                self.defense += random.randrange(1, 5)
            case _:
                raise ValueError(f"Unknown profession: {self.profession}")
        self.health = self.max_health
        self.mana = self.max_mana
        self.effects = [] 
        return None

    
    def discard_skill(self, skill: "Skill") -> None:
        if skill in self.skill_hand:
            self.skill_hand.remove(skill)
        return None
    
    
    def rest(self) -> None:
        # When a player rests, they do not attack. 
        # Instead, they heal, and generate mana
        self.mana += min(math.ceil(0.2 * self.max_mana), (self.max_mana - self.mana)) 
        self.heal(math.floor(0.1 * self.max_health))
        return None


class Enemy(Entity):
    def __init__(self, name: str, description: str, level:int, exp_amt:int, num_skills:int, section: int):
        health, attack, defense = (level * 65, level * 3, level * 3)
        super().__init__(name, health, attack, defense)
        self.mana: int = 99999999
        self.description: str = description
        self.section: int = section # The section this enemy belongs to, used for scaling skills
        self.profession = Professions.ENEMY
        self.create_enemy_skills(num_skills)
        self.exp_amt: int = exp_amt # How much experience this enemy gives when defeated
        
    
    
    def create_enemy_skills(self, amount: int) -> None:
        self._give_new_skills(amount)
        return None
    
    



class Ally(Entity):
    def __init__(self, name: str, description:str, level:int, section: int, profession: Professions):
        health, attack, defense = (level * 65, level * 5, level * 5)
        super().__init__(name, health, attack, defense)
        self.description: str = description
        self.mana: int = 999999999
        self.profession: Professions = profession
        self.section: int = section

    
    def generate_skills(self) -> None:
        num_skills = random.randint(1, 3)
        self._give_new_skills(num_skills)
        return None


