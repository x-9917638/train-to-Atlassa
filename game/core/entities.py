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
from .skills import Skill, GENERAL_SKILLS, ENEMY_SKILLS, WARRIOR_SKILLS, MAGE_SKILLS, ROGUE_SKILLS, PRIEST_SKILLS
from .status_effects import StatusEffect
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
        self.effects: list[StatusEffect] = [] # Status effects
    
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
        self.skills = GENERAL_SKILLS.copy()
        self.skill_hand: list[Skill] = []
        self.profession = None
        self.allies = []
    

    def add_ally(self, ally):
        if isinstance(ally, Ally):
            self.allies.append(ally)
            ally.generate_skills()
        else:
            raise TypeError("Ally must be an instance of the Ally class.\nThis should never happen, please report this.")


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
    

    def check_level_up(self):
        if self.experience >= self.level * 50:
            self._level_up()


    def _level_up(self):
        self.experience = 0
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
            case Professions.PRIEST:
                # High health, high mana
                self.max_health += random.randrange(70, 100)
                self.max_mana += random.randrange(30, 50)
                self.attack += random.randrange(1, 5)
                self.defense += random.randrange(3, 8)
            case _:
                raise ValueError(f"Unknown profession: {self.profession}")
        self.health = self.max_health
        self.mana = self.max_mana
        self.effects = [] 


    def discard_skill(self, skill: Skill):
        if skill in self.skill_hand:
            self.skill_hand.remove(skill)
    
    
    def rest(self):
        # When a player rests, they do not attack. 
        # Instead, they refresh skill cooldowns, heal, and generate mana
        self.mana += min(math.ceil(0.2 * self.max_mana), (self.max_mana - self.mana)) 
        self.health += min(math.floor(0.1 * self.max_health), (self.max_health - self.health))


class Enemy(Entity):
    def __init__(self, name: str, description: str, level:int, exp_amt:int, num_skills:int):
        health, attack, defense = (level * 100, level * 5, level * 5)
        super().__init__(name, health, attack, defense)
        self.mana = float("inf")
        self.description = description
        self.skills = self.create_enemy_skills(num_skills)
        self.exp_amt = exp_amt
    

    def create_enemy_skills(self, amount: int) -> list[Skill]:
        skills = random.choices(ENEMY_SKILLS, k=amount)
        return skills


class Ally(Entity):
    def __init__(self, name: str, description:str, level:int, profession: Professions):
        health, attack, defense = (level * 100, level * 5, level * 5)
        super().__init__(name, health, attack, defense)
        self.description = description
        self.mana = float("inf")
        self.profession = profession


    def generate_skills(self):
        num_skills = random.randint(1, 3)
        match self.profession:
            case Professions.WARRIOR:
                self.skills = random.choices(WARRIOR_SKILLS, k=num_skills)
            case Professions.MAGE:
                self.skills = random.choices(MAGE_SKILLS, k=num_skills)
            case Professions.ROGUE:
                self.skills = random.choices(ROGUE_SKILLS, k=num_skills)
            case Professions.PRIEST:
                self.skills = random.choices(PRIEST_SKILLS, k=num_skills)
            case _:
                raise ValueError(f"Unknown ally class: {self.ally_class}")



# Entities for use within the game
SECTION_ONE_ENEMIES = [
    # Level 1-2: Early game
    Enemy("Goblin", "A small green creature with a mischievous grin.", 1, 10, 2),
    Enemy("Skeleton", "An animated skeleton, rattling its bones as it moves.", 1, 12, 2),
    Enemy("Bandit", "A common thief or outlaw who preys on travelers.", 1, 13, 2),
    Enemy("Imp", "A small, mischievous demon known for its trickery and chaos.", 1, 14, 2),
    Enemy("Zombie", "A slow-moving undead creature with a hunger for flesh.", 2, 16, 2),
    Enemy("Harpy", "A winged creature with a haunting song that lures victims to their doom.", 2, 18, 3),
    Enemy("Ghoul", "A flesh-eating undead creature that lurks in graveyards.", 2, 20, 3),
    Enemy("Cultist", "A member of a dark cult, devoted to a sinister deity or cause.", 2, 22, 3),
    Enemy("Giant Spider", "A massive spider that spins webs to ensnare its prey.", 2, 24, 3),
]
SECTION_TWO_ENEMIES = [
    # Level 3-4: Mid game
    Enemy("Troll", "A large, hulking creature with regenerative abilities.", 3, 28, 4),
    Enemy("Dark Elf", "A sinister elf with dark skin and a penchant for magic.", 3, 30, 4),
    Enemy("Specter", "A spectral being that haunts the living.", 3, 32, 4),
    Enemy("Banshee", "A wailing spirit that foretells death and brings despair to those who hear its cry.", 3, 34, 4),
    Enemy("Swamp Hag", "A twisted, malevolent creature that dwells in marshes and swamps.", 3, 36, 4),
    Enemy("Witch", "A practitioner of dark magic, often associated with curses and hexes.", 3, 38, 4),
    Enemy("Dragonling", "A young dragon, smaller but still fierce and dangerous.", 3, 40, 4),
    Enemy("Shadow Beast", "A creature made of pure darkness, lurking in the shadows.", 4, 44, 5),
    Enemy("Wraith", "A ghostly figure that drains the life force of its victims.", 4, 46, 5),
    Enemy("Basilisk", "A serpent-like creature with a deadly gaze that can petrify its prey.", 4, 48, 5),
    Enemy("Kraken Cultist", "A follower of the legendary kraken, seeking to summon the beast from the depths of the ocean.", 4, 50, 5),
    Enemy("Corrupted Druid", "A nature priest who has been tainted by dark magic, twisting the natural world to their will.", 4, 52, 5),
    Enemy("Ice Elemental", "A being of pure ice, capable of freezing its enemies with a touch.", 4, 54, 5),
    Enemy("Warlock", "A malevolent spellcaster who makes pacts with dark forces for power.", 4, 56, 5),
]
SECTION_THREE_ENEMIES = [
    # Level 5-6: Late game
    Enemy("Werewolf", "A human cursed to transform into a wolf-like beast under the full moon.", 5, 60, 6),
    Enemy("Griffin", "A majestic creature with the body of a lion and the wings and head of an eagle.", 5, 62, 6),
    Enemy("Living Armor", "A suit of armor animated by dark magic, moving with a life of its own.", 5, 64, 6),
    Enemy("Earth Elemental", "A being of solid rock and earth, strong and unyielding.", 5, 66, 6),
    Enemy("Fire Elemental", "A creature of living flame, burning everything in its path.", 5, 68, 6),
    Enemy("Cursed Pirate", "A once-noble sailor now cursed to roam the seas as a ghostly figure, seeking revenge on those who wronged them.", 5, 70, 6),
    Enemy("Doppelganger", "A shape-shifting creature that can mimic the appearance of any being, sowing confusion and chaos.", 5, 72, 6),
    Enemy("Minotaur", "A half bull, half human creature that roams labyrinths.", 6, 76, 7),
    Enemy("Chimera", "A monstrous creature with the body of a lion, the head of a goat, and a serpent for a tail.", 6, 78, 7),
    Enemy("Manticore", "A beast with the body of a lion, the wings of a bat, and a scorpion's tail.", 6, 80, 7),
    Enemy("Possessed Knight", "A knight whose body has been taken over by a malevolent spirit, turning them into a relentless foe.", 6, 82, 7),
    Enemy("Stone Golem", "A massive creature made of stone, animated by ancient magic to protect its creator.", 6, 84, 7),
    Enemy("Black Knight", "A fearsome warrior clad in dark armor, wielding a cursed sword that drains the life from its victims.", 6, 86, 7),
]
SECTION_FOUR_ENEMIES = [
    # Level 7-8: End game
    Enemy("Lich", "A powerful undead sorcerer who has achieved immortality through dark magic.", 7, 90, 8),
    Enemy("Necromancer", "A dark mage who commands the undead and practices forbidden magic.", 7, 92, 8),
    Enemy("Frost Giant", "A colossal giant from the frozen north, wielding ice and snow as weapons.", 7, 94, 8),
    Enemy("Abyssal Horror", "A creature from the darkest depths of the ocean, twisted and monstrous.", 7, 96, 8),
    Enemy("Storm Elemental", "A tempestuous being of wind and lightning, capable of unleashing devastating storms.", 7, 98, 8),
    Enemy("Demon", "A malevolent being from the underworld, often summoned by dark magic.", 7, 100, 8),
    Enemy("Undead Giant", "A massive, reanimated giant that towers over its foes, driven by an insatiable hunger for destruction.", 8, 110, 9)
]


SECTION_ONE_BOSSES = [
    # Early Game Bosses (Level 2-3)
    Enemy("Goblin King", "The cunning and ruthless ruler of the goblins, wielding a jagged crown and a massive club.", 2, 30, 4),
    Enemy("Bone Lord", "A towering skeleton adorned with ancient armor, commanding legions of the undead.", 3, 40, 5)
]

SECTION_TWO_BOSSES = [
    # Mid Game Bosses (Level 4-5)
    Enemy("Witch Queen", "A master of curses and dark magic, surrounded by a cloud of sinister energy.", 4, 60, 6),
    Enemy("Ancient Treant", "A colossal, ancient tree spirit, its roots and branches crushing all who oppose it.", 5, 80, 6)
]

SECTION_THREE_BOSSES = [
    # Late Game Bosses (Level 6-7)
    Enemy("Drake Matriarch", "The matriarch of a dragon brood, her scales shimmer with elemental power.", 6, 120, 7),
    Enemy("Lord of Shadows", "A mysterious figure cloaked in darkness, able to manipulate the very shadows themselves.", 7, 140, 8)
]

SECTION_FOUR_BOSSES = [
    # End Game Bosses (Level 8+)
    Enemy("Archdemon Malakar", "A demon lord from the deepest abyss, radiating overwhelming power and malice.", 8, 200, 10),
    Enemy("The Eternal Lich", "An immortal sorcerer whose phylactery is hidden, wielding devastating necromancy.", 8, 220, 10)
]

