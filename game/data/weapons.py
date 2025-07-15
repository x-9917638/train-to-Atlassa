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

from ..core.items import Weapon

SECTION_ONE_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon(
        name="Training Sword | <Tier 1>", 
        description="It's a sword, but not a very good one.", 
        boost_range=(3, 7)
        ): 0.44,
    Weapon(
        name="Rusty Sword | <Tier 1>", 
        description="A subpar sword.", 
        boost_range=(5, 10)
        ): 0.3,
    Weapon(
        name="Iron Sword | <Tier 1>", 
        description="A sturdy iron sword.", 
        boost_range=(8, 15)
        ): 0.2,
    Weapon(
        name="Steel Sword | <Tier 1>", 
        description="A sharp steel sword, fit for a knight.", 
        boost_range=(12, 20)
        ): 0.05,
    Weapon(
        name="Enchanted Sword | <Tier 1>", 
        description="A sword, imbued with magic.", 
        boost_range=(15, 25)
        ): 0.01
}

SECTION_TWO_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon(
        name="Frostbite | <Tier 2>",
        description="A cursed sword that freezes wounds, leaving victims brittle.",
        boost_range=(15, 17)
    ): 0.3,
    Weapon(
        name="Duskfang | <Tier 2>",
        description="A dagger, perfect for an assassination.",
        boost_range=(15, 20)
    ): 0.3,
    Weapon(
        name="Dawnbringer | <Tier 2>",
        description="A greatsword with the radiance of the sun.",
        boost_range=(10, 25)
    ): 0.3,
    Weapon(
        name="Shadow Blade | <Tier 2>",
        description="It seems to have been forged with pure darkness.",
        boost_range=(30, 32)
    ): 0.05,
    Weapon(
        name="Holy Avenger | <Tier 2>",
        description="A pure holy light emanates from the sword.",
        boost_range=(25, 40)
    ): 0.05
}

SECTION_THREE_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon(
        name="The Abyssal Maw | <Tier 3>",
        description="A flail with a living, toothy head that hungers for flesh.",
        boost_range=(20, 30)
    ): 0.3,
    Weapon(
        name="Stormcaller | <Tier 3>",
        description="A mace that crackles with the power of thunder.",
        boost_range=(25, 35)
    ): 0.3,
    Weapon(
        name="The Hollow Glaive | <Tier 3>",
        description="A powerful glaive that is said to absorb souls.",
        boost_range=(30, 40)
    ): 0.25,
    Weapon(
        name="Bloodflute | <Tier 3>",
        description="A flute that plays a haunting melody, said to drain the life force of its victims.",
        boost_range=(35, 45)
    ): 0.1,
    Weapon(
        name="Mirrorblade | <Tier 3>",
        description="A sword that reflects the future.",
        boost_range=(50, 55)
    ): 0.05

}

SECTION_FOUR_WEAPONS = { # <Weapon>: <Weighted Chance>
    Weapon(
        name="Worldrender | <Tier 4>",
        description="A colossal sword that can cleave mountains.",
        boost_range=(60, 65)
    ): 0.25,
    Weapon(
        name="Voidreaver | <Tier 4>",
        description="A scythe that can cut through the fabric of reality.",
        boost_range=(45, 75)
    ): 0.25,
    Weapon(
        name="Celestial Spear | <Tier 4>",
        description="A spear that channels the power of the stars.",
        boost_range=(55, 70)
    ): 0.25,
    Weapon(
        name="Oathkeeper | <Tier 4>",
        description="A collosal warhammer capable of shaking the earth.",
        boost_range=(65, 80)
    ): 0.25
}
