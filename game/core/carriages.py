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
from .entities import Ally
from .entities import SECTION_ONE_ENEMIES, SECTION_TWO_ENEMIES, SECTION_THREE_ENEMIES, SECTION_FOUR_ENEMIES
from .entities import SECTION_ONE_BOSSES, SECTION_TWO_BOSSES, SECTION_THREE_BOSSES, SECTION_FOUR_BOSSES
import random as rand

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
    def __init__(self, carriage_type: CarriageType, name: str, section:int):
        self.type = carriage_type
        self.name = name
        self.entities = []
        self.allies = []
        self.enemies = []
        self.connected_places = []
        self.items = []
        self.section = section
        self.generate_entities()

    def generate_entities(self):

        match self.type:
            case CarriageType.FIGHT:
                for i in range(rand.randint(1, 3)):
                    match self.section:
                        case 1:
                            enemy = rand.choice(SECTION_ONE_ENEMIES)
                        case 2:
                            enemy = rand.choice(SECTION_TWO_ENEMIES)
                        case 3:
                            enemy = rand.choice(SECTION_THREE_ENEMIES)
                        case 4:
                            enemy = rand.choice(SECTION_FOUR_ENEMIES)
                        case _:
                            raise ValueError(f"Invalid section: {self.section}.\n This should never happen, please report this.")
                    self._add_enemy(enemy)

            case CarriageType.REST:
                for i in range(rand.randint(0, 1)):
                    ally_name = rand.choice(ALLY_NAMES)
                    ally_profession = rand.choice(list(Professions))
                    match ally_profession:
                        case Professions.WARRIOR:
                            ally_description = rand.choice(DESCRIPTIONS_WARRIOR)
                        case Professions.MAGE:
                            ally_description = rand.choice(DESCRIPTIONS_MAGE)
                        case Professions.ROGUE:
                            ally_description = rand.choice(DESCRIPTIONS_ROGUE)
                        case Professions.PRIEST:
                            ally_description = rand.choice(DESCRIPTIONS_PRIEST)
                    self._add_ally(Ally(ally_name, ally_description, rand.randint(1, 8), ally_profession))

            case CarriageType.CHALLENGE:
                for i in range(rand.randint(3, 4)):
                    match self.section:
                        case 1:
                            enemy = rand.choice(SECTION_ONE_ENEMIES)
                        case 2:
                            enemy = rand.choice(SECTION_TWO_ENEMIES)
                        case 3:
                            enemy = rand.choice(SECTION_THREE_ENEMIES)
                        case 4:
                            enemy = rand.choice(SECTION_FOUR_ENEMIES)
                        case _:
                            raise ValueError(f"Invalid section: {self.section}.\n This should never happen, please report this.")
                    self._add_enemy(enemy)
                    
            case CarriageType.BOSS:
                for i in range(rand.choice([1, 1, 1, 1, 2])):
                    match self.section:
                        case 1:
                            enemy = rand.choice(SECTION_ONE_BOSSES)
                        case 2:
                            enemy = rand.choice(SECTION_TWO_BOSSES)
                        case 3:
                            enemy = rand.choice(SECTION_THREE_BOSSES)
                        case 4:
                            enemy = rand.choice(SECTION_FOUR_BOSSES)
                        case _:
                            raise ValueError(f"Invalid section: {self.section}.\n This should never happen, please report this.")
                    self._add_enemy(enemy)

    def _add_enemy(self, entity):
        self.enemies.append(entity)

    def _add_ally(self, ally):
        self.allies.append(ally)
    
    def _add_connection(self, place):
        self.connected_places.append(place)


