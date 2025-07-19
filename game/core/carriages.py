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

from ..utils import CarriageType, Professions

from ..data import SECTION_ONE_ITEMS, SECTION_TWO_ITEMS, SECTION_THREE_ITEMS, SECTION_FOUR_ITEMS
from ..data.enemies import SECTION_ONE_ENEMIES, SECTION_TWO_ENEMIES, SECTION_THREE_ENEMIES, SECTION_FOUR_ENEMIES
from ..data.enemies import SECTION_ONE_BOSSES, SECTION_TWO_BOSSES, SECTION_THREE_BOSSES, SECTION_FOUR_BOSSES

from .entities import Ally


import random as rand
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .entities import Enemy
    from .items import Item

logger = logging.getLogger(__name__)

# Descriptions and names for allies
ALLY_NAMES = [
    "Aelara", "Brialla", "Cyndra", "Drusila", "Elyndra",
    "Feyra", "Gwyneth", "Haelia", "Ilythia", "Jasmina",
    "Kythira", "Lunara", "Morgwen", "Nyssa", "Orianna",
    "Phaedra", "Quinnara", "Ravena", "Sylria", "Thalindra",
    "Aldric", "Baelthor", "Cedric", "Dain", "Eldrin",
    "Fenris", "Gorion", "Haldor", "Ithil", "Jorund",
    "Kael", "Lorath", "Maldrek", "Nyr", "Orin",
    "Parthas", "Quillon", "Ragnar", "Soren", "Thrain"
]

DESCRIPTIONS_WARRIOR = [
    "A stalwart defender of the realm, wielding a mighty sword and shield.",
    "A battle-hardened warrior, known for their bravery and strength in combat.",
    "A fierce protector, clad in heavy armor and ready to face any foe.",
    "A seasoned fighter, skilled in the art of war and tactics.",
    "A relentless warrior, charging into battle with unwavering resolve.",
    "A disciplined soldier, trained in the ways of combat and strategy.",
    "A noble knight, sworn to uphold justice and protect the innocent.",
    "A skilled gladiator, known for their prowess in the arena and unmatched combat skills.",
    "A legendary hero, whose deeds in battle have become the stuff of legends.",
    "A fearless champion, standing as a bulwark against the forces of darkness.",
]    

DESCRIPTIONS_MAGE = [
    "A master of the arcane arts, wielding powerful spells to vanquish foes.",
    "A wise and learned mage, skilled in the manipulation of magical energies.",
    "A sorcerer of great renown, capable of bending reality to their will.",
    "A mystical spellcaster, drawing upon ancient knowledge to cast devastating spells.",
    "An elemental mage, commanding the forces of fire, ice, and lightning.",
    "A cunning illusionist, using trickery and deception to outwit enemies.",
    "A healer of great skill, mending wounds and restoring vitality with magic.",
    "A warlock who has made pacts with dark forces for forbidden power.",
    "A necromancer who commands the undead and wields dark magic.",
    "A sage of the arcane, whose wisdom and knowledge are unmatched."
]

DESCRIPTIONS_ROGUE = [
    "A stealthy assassin, skilled in the art of silent killing and subterfuge.",
    "A cunning thief, adept at picking locks and stealing valuable treasures.",
    "A shadowy rogue, moving unseen through the darkness to strike at enemies.",
    "A master of deception, using charm and wit to manipulate others.",
    "A skilled archer, deadly with a bow and arrow from a distance.",
    "A quick-footed duelist, excelling in one-on-one combat with agility and finesse.",
    "A trapper who sets deadly traps to ensnare unsuspecting foes.",
    "A poisoner who uses deadly toxins to weaken and incapacitate enemies.",
    "A swashbuckler, known for their flamboyant style and daring exploits.",
    "A rogue with a heart of gold, using their skills for noble causes."
]    

DESCRIPTIONS_PRIEST = [
    "A devoted healer, channeling divine energy to mend wounds and cure ailments.",
    "A pious cleric, spreading the light of their faith to protect and guide others.",
    "A spiritual leader, offering wisdom and counsel to those in need.",
    "A holy warrior, wielding both sword and prayer to vanquish evil.",
    "A mystic who communes with the divine for guidance and strength.",
    "A protector of the weak, using their faith to shield allies from harm.",
    "A benevolent priestess, known for their compassion and kindness.",
    "A champion of justice, standing against darkness with unwavering faith.",
    "A divine oracle, foreseeing the future and offering prophetic insights.",
    "A guardian of sacred knowledge, preserving ancient texts and teachings."
]

class Carriage:
    num2word_map: dict[int, str] = {
        1: "ONE",
        2: "TWO",
        3: "THREE",
        4: "FOUR"
    }


    def __init__(self, carriage_type: CarriageType, name: str, section:int):
        self.type: CarriageType = carriage_type
        self.name: str = name
        self.entities = []
        self.allies: list[Ally] = []
        self.enemies: list["Enemy"] = []
        self.connected_places: list[Carriage] = []
        self.items: list["Item"] = []
        self.section: int = section
        self.section_str: str = self.num2word_map[self.section] 
        self.generate_entities()
        self.generate_items()
        

    def generate_entities(self) -> None:
        match self.type:
            case CarriageType.FIGHT:
                enemies: list["Enemy"] = self._choose_enemies(rand.randint(1, 2))
                self._add_enemy(enemies)

            case CarriageType.ALLY:
                if rand.choice((True, False)): # 50% chance to add an ally
                    ally = self._make_ally()
                    self._add_ally(ally) # Possibility of duplicate, but it's so low so whatever

            case CarriageType.CHALLENGE:
                enemies: list["Enemy"] = self._choose_enemies(rand.randint(3, 4))
                self._add_enemy(enemies)
                    
            case CarriageType.BOSS:
                num_bosses: int = rand.choice([1, 1, 1, 1, 2])
                boss_pool: list["Enemy"] = globals()[f"SECTION_{self.section_str}_BOSSES"].copy()
                bosses = rand.sample(boss_pool, k=num_bosses)
                self._add_enemy(bosses)

        return None


    def _make_ally(self) -> Ally:
        ally_name: str = rand.choice(ALLY_NAMES)
        ally_profession: Professions = rand.choice([profession for profession in Professions if profession != Professions.ENEMY]) # Exclude ENEMY profession
        match ally_profession:
            case Professions.WARRIOR:
                ally_description: str = rand.choice(DESCRIPTIONS_WARRIOR)
            case Professions.MAGE:
                ally_description: str = rand.choice(DESCRIPTIONS_MAGE)
            case Professions.ROGUE:
                ally_description: str = rand.choice(DESCRIPTIONS_ROGUE)
            case Professions.PRIEST:
                ally_description: str = rand.choice(DESCRIPTIONS_PRIEST)
            case _:
                raise ValueError(f"Unknown profession: {ally_profession}")
        match self.section:
            case 1:
                ally_level: int = rand.randint(1, 2)
            case 2:
                ally_level: int = rand.randint(2, 4)
            case 3:
                ally_level: int = rand.randint(4, 6)
            case 4:
                ally_level: int = rand.randint(6, 8)
            case _:
                raise ValueError(f"Unknown section: {self.section}")
        return Ally(name=ally_name, description=ally_description, level=ally_level, section=self.section, profession=ally_profession)


    def _choose_enemies(self, num_enemies: int) -> list["Enemy"]:
        enemy_pool: list["Enemy"] = globals()[f"SECTION_{self.section_str}_ENEMIES"].copy()
        chosen_enemies = rand.sample(enemy_pool, k=num_enemies)
        return chosen_enemies


    def generate_items(self) -> None:
        # Choose num items
        num_items: int = rand.choice((0, 0, 0, 1, 2))
        items = self._choose_items(num_items)
        logger.debug(f"Generated {num_items} items for carriage {self.name} in section {self.section}.")
        self.items.extend(items)


    def _choose_items(self, num_items: int) -> list["Item"]:
        item_pool: list[dict["Item", float]] = globals()[f"SECTION_{self.section_str}_ITEMS"]
        chosen_items = []
        WEAPONS, ARMORS, SCROLLS = 0, 1, 2 # No magic numbers!
        for _ in range(num_items):
            category = rand.choice((WEAPONS, ARMORS, SCROLLS)) 
            chosen_items.extend(rand.choices(list(item_pool[category].keys()), k=1, weights=list(item_pool[category].values())))
        return chosen_items
    

    def _add_enemy(self, enemies: list["Enemy"]) -> None:
        self.enemies.extend(enemies)
        return None


    def _add_ally(self, ally: Ally) -> None:
        self.allies.append(ally)
        return None


    def _add_connection(self, carriage: "Carriage") -> None:
        self.connected_places.append(carriage)
        return None

