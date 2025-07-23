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

from ..core.items import Armor

SECTION_ONE_ARMOR = { # <Armor>: <Weighted Chance>
    Armor(
        name="Leather Armor | <Tier 1>", 
        description="Basic leather armor.",
        boost_range=(3, 7)
        ): 0.54,
    Armor(
        name="Chainmail Armor | <Tier 1>", 
        description="Capable of stopping arrows, but not much more.",
        boost_range=(5, 10)
        ): 0.3,
    Armor(
        name="Plate Armor | <Tier 1>", 
        description="Of course massive metal plates will protect you.",
        boost_range=(8, 13)
        ): 0.1,
    Armor(
        name="Dragon Scale Armor | <Tier 1>", 
        description="A set of armor said to be made from dragon scales.",
        boost_range=(12, 17)
        ): 0.05,
    Armor(
        name="Mystic Armor | <Tier 1>", 
        description="Although designed for mages, it presents a suprisingly high resistance to physical damage.",
        boost_range=(15, 20)
        ): 0.01
}

SECTION_TWO_ARMOR = { # <Armor>: <Weighted Chance>
    Armor(
        name="Whisperweave Cloak | <Tier 2>",
        description="A cloak that muffles sound, making the wearer nearly silent when moving.",
        boost_range=(10, 12)
    ): 0.42,
    Armor(
        name="Feywild Mantle | <Tier 2>",
        description="A shimmering cape imbued with nature's grace.",
        boost_range=(8, 14)
    ): 0.42,
    Armor(
        name="Serpentscale Hauberk | <Tier 2>",
        description="A coat of overlapping metallic scales that slithers to deflect blows.",
        boost_range=(19, 20)
    ): 0.1,
    Armor(
        name="Dawnforged Plate | <Tier 2>",
        description="Armor that glows with the light of the rising sun, deterring undead and demons.",
        boost_range=(20, 28)
    ): 0.05,
    Armor(
        name="The Aegis of the Phoenix | <Tier 2>",
        description="Forged from the feathers of a phoenix, this cloak provides a startlingly high defense for mere bird feathers.",
        boost_range=(30, 40)
    ): 0.01
}

SECTION_THREE_ARMOR = { # <Armor>: <Weighted Chance>
    Armor(
        name="Voidwalker Robes | <Tier 3>",
        description="Robes that seem to absorb light, turning the wearer into nothing more than a shadowy presence.",
        boost_range=(20, 30)
    ): 0.3,
    Armor(
        name="Titan's Embrace | <Tier 3>",
        description="A massive suit of armor that grants the wearer immense resilience.",
        boost_range=(25, 35)
    ): 0.3,
    Armor(
        name="Celestial Chainmail | <Tier 3>",
        description="An ethereal chainmail that glows with divine light.",
        boost_range=(30, 40)
    ): 0.25,
    Armor(
        name="Stormrider's Harness | <Tier 3>",
        description="A harness that crackles with electrical energy.",
        boost_range=(35, 45)
    ): 0.1,
    Armor(
        name="Eclipse Plate | <Tier 3>",
        description="A dark plate armor that seems to absorb all light around it, making the wearer nearly invisible in shadows.",
        boost_range=(50, 55)
    ): 0.05
}

SECTION_FOUR_ARMOR = { # <Armor>: <Weighted Chance>
    Armor(
        name="Rimeborn Exoskeleton | <Tier 4>",
        description="Frozen armor that encases the wearer in an ever-replenishing layer of ice.",
        boost_range=(60, 65)
    ): 0.25,
    Armor(
        name="Astral Guardian's Spangenhelm | <Tier 4>",
        description="Forged from pure starlight, granting resilience through cosmic power.",
        boost_range=(55, 70)
    ): 0.25,
    Armor(
        name="Rune-Forged Carapace | <Tier 4>",
        description="Etched with ancient glyphs of unyielding stone, the carapace provides unmatched protection.",
        boost_range=(45, 75)
    ): 0.25,
    Armor(
        name="Voidforged Armor | <Tier 4>",
        description="An armor made from the fabric of the void, consuming all attacks.",
        boost_range=(65, 80)
    ): 0.25,
    Armor(
        name="Eternal Sentinel's Aegis | <Tier 4>",
        description="An aegis that glows with an eternal light.",
        boost_range=(60, 70)
    ): 0.25
}