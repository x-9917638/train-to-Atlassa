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

from ..core.entities import Enemy

SECTION_ONE_ENEMIES = [
    # Level 1-2: Early game
    Enemy(
		name="Goblin", 
		description="A small green creature with a mischievous grin.", 
		level=1, 
		exp_amt=10, 
		num_skills=2
	),
    Enemy(
		name="Skeleton", 
		description="An animated skeleton, rattling its bones as it moves.", 
		level=1, 
		exp_amt=12, 
		num_skills=2
	),
    Enemy(
		name="Bandit", 
		description="A common thief or outlaw who preys on travelers.", 
		level=1, 
		exp_amt=13, 
		num_skills=2
	),
    Enemy(
		name="Imp", 
		description="A small, mischievous demon known for its trickery and chaos.", 
		level=1, 
		exp_amt=14, 
		num_skills=2
	),
    Enemy(
		name="Zombie", 
		description="A slow-moving undead creature with a hunger for flesh.", 
		level=2, 
		exp_amt=16, 
		num_skills=2
	),
    Enemy(
		name="Harpy", 
		description="A winged creature with a haunting song that lures victims to their doom.", 
		level=2, 
		exp_amt=18, 
		num_skills=3
	),
    Enemy(
		name="Ghoul", 
		description="A flesh-eating undead creature that lurks in graveyards.", 
		level=2, 
		exp_amt=20, 
		num_skills=3
	),
    Enemy(
		name="Cultist", 
		description="A member of a dark cult, devoted to a sinister deity or cause.", 
		level=2, 
		exp_amt=22, 
		num_skills=3
	),
    Enemy(
		name="Giant Spider", 
		description="A massive spider that spins webs to ensnare its prey.", 
		level=2, 
		exp_amt=24, 
		num_skills=3
	)
]
SECTION_TWO_ENEMIES = [
    # Level 3-4: Mid game
    Enemy(
		name="Troll", 
		description="A large, hulking creature with regenerative abilities.", 
		level=3, 
		exp_amt=28, 
		num_skills=4
	),
    Enemy(
		name="Dark Elf", 
		description="A sinister elf with dark skin and a penchant for magic.", 
		level=3, 
		exp_amt=30, 
		num_skills=4
	),
    Enemy(
		name="Specter", 
		description="A spectral being that haunts the living.", 
		level=3, 
		exp_amt=32, 
		num_skills=4
	),
    Enemy(
		name="Banshee", 
		description="A wailing spirit that foretells death and brings despair to those who hear its cry.", 
		level=3, 
		exp_amt=34, 
		num_skills=4
	),
    Enemy(
		name="Swamp Hag", 
		description="A twisted, malevolent creature that dwells in marshes and swamps.", 
		level=3, 
		exp_amt=36, 
		num_skills=4
	),
    Enemy(
		name="Witch", 
		description="A practitioner of dark magic, often associated with curses and hexes.", 
		level=3, 
		exp_amt=38, 
		num_skills=4
	),
    Enemy(
		name="Dragonling", 
		description="A young dragon, smaller but still fierce and dangerous.", 
		level=3, 
		exp_amt=40, 
		num_skills=4
	),
    Enemy(
		name="Shadow Beast", 
		description="A creature made of pure darkness, lurking in the shadows.", 
		level=4, 
		exp_amt=44, 
		num_skills=5
	),
    Enemy(
		name="Wraith", 
		description="A ghostly figure that drains the life force of its victims.", 
		level=4, 
		exp_amt=46, 
		num_skills=5
	),
    Enemy(
		name="Basilisk", 
		description="A serpent-like creature with a deadly gaze that can petrify its prey.", 
		level=4, 
		exp_amt=48, 
		num_skills=5
	),
    Enemy(
		name="Kraken Cultist", 
		description="A follower of the legendary kraken, seeking to summon the beast from the depths of the ocean.", 
		level=4, 
		exp_amt=50, 
		num_skills=5
	),
    Enemy(
		name="Corrupted Druid", 
		description="A nature priest who has been tainted by dark magic, twisting the natural world to their will.", 
		level=4, 
		exp_amt=52, 
		num_skills=5
	),
    Enemy(
		name="Ice Elemental", 
		description="A being of pure ice, capable of freezing its enemies with a touch.", 
		level=4, 
		exp_amt=54, 
		num_skills=5
	),
    Enemy(
		name="Warlock", 
		description="A malevolent spellcaster who makes pacts with dark forces for power.", 
		level=4, 
		exp_amt=56, 
		num_skills=5
	)
]
SECTION_THREE_ENEMIES = [
    # Level 5-6: Late game
    Enemy(
		name="Werewolf", 
		description="A human cursed to transform into a wolf-like beast under the full moon.", 
		level=5, 
		exp_amt=60, 
		num_skills=6
	),
    Enemy(
		name="Griffin", 
		description="A majestic creature with the body of a lion and the wings and head of an eagle.", 
		level=5, 
		exp_amt=62, 
		num_skills=6
	),
    Enemy(
		name="Living Armor", 
		description="A suit of armor animated by dark magic, moving with a life of its own.", 
		level=5, 
		exp_amt=64, 
		num_skills=6
	),
    Enemy(
		name="Earth Elemental", 
		description="A being of solid rock and earth, strong and unyielding.", 
		level=5, 
		exp_amt=66, 
		num_skills=6
	),
    Enemy(
		name="Fire Elemental", 
		description="A creature of living flame, burning everything in its path.", 
		level=5, 
		exp_amt=68, 
		num_skills=6
	),
    Enemy(
		name="Cursed Pirate", 
		description="A once-noble sailor now cursed to roam the seas as a ghostly figure, seeking revenge on those who wronged them.", 
		level=5, 
		exp_amt=70, 
		num_skills=6
	),
    Enemy(
		name="Doppelganger", 
		description="A shape-shifting creature that can mimic the appearance of any being, sowing confusion and chaos.", 
		level=5, 
		exp_amt=72, 
		num_skills=6
	),
    Enemy(
		name="Minotaur", 
		description="A half bull, half human creature that roams labyrinths.", 
		level=6, 
		exp_amt=76, 
		num_skills=7
	),
    Enemy(
		name="Chimera", 
		description="A monstrous creature with the body of a lion, the head of a goat, and a serpent for a tail.", 
		level=6, 
		exp_amt=78, 
		num_skills=7
	),
    Enemy(
		name="Manticore", 
		description="A beast with the body of a lion, the wings of a bat, and a scorpion's tail.", 
		level=6, 
		exp_amt=80, 
		num_skills=7
	),
    Enemy(
		name="Possessed Knight", 
		description="A knight whose body has been taken over by a malevolent spirit, turning them into a relentless foe.", 
		level=6, 
		exp_amt=82, 
		num_skills=7
	),
    Enemy(
		name="Stone Golem", 
		description="A massive creature made of stone, animated by ancient magic to protect its creator.", 
		level=6, 
		exp_amt=84, 
		num_skills=7
	),
    Enemy(
		name="Black Knight", 
		description="A fearsome warrior clad in dark armor, wielding a cursed sword that drains the life from its victims.", 
		level=6, 
		exp_amt=86, 
		num_skills=7
	)
]
SECTION_FOUR_ENEMIES = [
    # Level 7-8: End game
    Enemy(
		name="Lich", 
		description="A powerful undead sorcerer who has achieved immortality through dark magic.", 
		level=7, 
		exp_amt=90, 
		num_skills=8
	),
    Enemy(
		name="Necromancer", 
		description="A dark mage who commands the undead and practices forbidden magic.", 
		level=7, 
		exp_amt=92, 
		num_skills=8
	),
    Enemy(
		name="Frost Giant", 
		description="A colossal giant from the frozen north, wielding ice and snow as weapons.", 
		level=7, 
		exp_amt=94, 
		num_skills=8
	),
    Enemy(
		name="Abyssal Horror", 
		description="A creature from the darkest depths of the ocean, twisted and monstrous.", 
		level=7, 
		exp_amt=96, 
		num_skills=8
	),
    Enemy(
		name="Storm Elemental", 
		description="A tempestuous being of wind and lightning, capable of unleashing devastating storms.", 
		level=7, 
		exp_amt=98, 
		num_skills=8
	),
    Enemy(
		name="Demon", 
		description="A malevolent being from the underworld, often summoned by dark magic.", 
		level=7, 
		exp_amt=100, 
		num_skills=8
	),
    Enemy(
		name="Undead Giant", 
		description="A massive, reanimated giant that towers over its foes, driven by an insatiable hunger for destruction.", 
		level=8, 
		exp_amt=110, 
		num_skills=9
    )
]


SECTION_ONE_BOSSES = [
    # Early Game Bosses (Level 2-3)
    Enemy(
		name="Goblin King", 
		description="The cunning and ruthless ruler of the goblins, wielding a jagged crown and a massive club.", 
		level=2, 
		exp_amt=30, 
		num_skills=4
	),
    Enemy(
		name="Bone Lord", 
		description="A towering skeleton adorned with ancient armor, commanding legions of the undead.", 
		level=3, 
		exp_amt=40, 
		num_skills=5
    )
]

SECTION_TWO_BOSSES = [
    # Mid Game Bosses (Level 4-5)
    Enemy(
		name="Witch Queen", 
		description="A master of curses and dark magic, surrounded by a cloud of sinister energy.", 
		level=4, 
		exp_amt=60, 
		num_skills=6
	),
    Enemy(
		name="Ancient Treant", 
		description="A colossal, ancient tree spirit, its roots and branches crushing all who oppose it.", 
		level=5, 
		exp_amt=80, 
		num_skills=6
    )
]

SECTION_THREE_BOSSES = [
    # Late Game Bosses (Level 6-7)
    Enemy(
		name="Drake Matriarch", 
		description="The matriarch of a dragon brood, her scales shimmer with elemental power.", 
		level=6, 
		exp_amt=120, 
		num_skills=7
	),
    Enemy(
		name="Lord of Shadows", 
		description="A mysterious figure cloaked in darkness, able to manipulate the very shadows themselves.", 
		level=7, 
		exp_amt=140, 
		num_skills=8
    )
]

SECTION_FOUR_BOSSES = [
    # End Game Bosses (Level 8+)
    Enemy(
		name="Archdemon Malakar", 
		description="A demon lord from the deepest abyss, radiating overwhelming power and malice.", 
		level=8, 
		exp_amt=200, 
		num_skills=10
	),
    Enemy(
		name="The Eternal Lich", 
		description="An immortal sorcerer whose phylactery is hidden, wielding devastating necromancy.", 
		level=8, 
		exp_amt=220,
        num_skills=10
    )
]