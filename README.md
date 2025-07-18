# Train to Atlassa
A text based adventure game with turn based combat.

# Prerequisites
- [python>=3.10](https://python.org)
- MacOS/Other *nix Systems: getch<br>
    `python3 -m pip install getch`
- Note: Autocompletion of commands will not work on Windows due to the lack of readline.

# Getting Started
1. Make sure the required dependencies are installed
2. Clone the repository: 
```git clone https://github.com/x-9917638/train-to-Atlassa.git```
3. Change directory: 
```cd train-to-Atlassa```
4. Start the game: 
```python3 main.py```

# Usage
Train to Atlassa accepts input via various commands. 
It acts as an interactive shell prompt with various modes, depending on the commands given.
<br>
There are 2 main modes:
- Default
- Combat

## Default mode
The player is placed into default mode for navigation, and managing their status. 
<br>
Autocompletions are supported.
<br>
Available Commands:
- Movement:
    - Move to next carriage: **next, n**
    - Move to previous carriage | **back, b**
- Combat:
    - Initiate combat | **fight**
- Information:
    - Show inventory | **inv, inventory**
    - Show skills | **skills**
    - Show player status | **status**
    - Show current carriage info **info**            
- Interaction:
    - Hire an ally | **hire [ally]**
    - Check the current carriage for any items. | **explore**
- System:
  - Show help | **help, h** or *empty command*
  - Exit the game | **exit, CTRL + D**  
  - Save the game to local file | **save**

### Inventory
The inventory presents a simple menu to manage items.
<br>
Available Commands:
- Equip a Weapon or Armor | **e, equip**
- Use a Consumable | **u, use**
- Drop (delete) an Item | **d, drop**
- Cancel | **any other input**

## Combat
After initiating combat using the *fight* command, the player is sent into combat mode.
<br>
The interface displays the following:
- Health
- Mana
- Enemies
- Allies (If applicable)


The player can choose one of five commands, and autocompletions are supported.
<br>
Available Commands:
- Use a skill | **attack**
- Rest (Heal 20% max HP, 10% max MP) | **rest**
- Use a consusmable item | **items**        
- Retreat (Clears the room) | **retreat**    
- Show help | **help, h** or *empty command*


# Mechanics
## Professions
Train to Atlassa has 4 professions: Rogue, Warrior, Mage, Priest

The priest profession is limited to NPC allys.

Professions influence the stats and skills of the player.
- Warrior: 
  - High Defense, High Health
  - Specialises in crowd control skills
- Rogue:
  - Very High Attack
  - Specialises in high damage, single target skills
- Mage:
  - High mana, High Attack
  - Skills are all-rounded


## Skills
There are a variety of skills in Train to Atlasssa, and each class has their own dedicated skills

The player also begins with 2 default skills: Gambling Fever, and Basic Attack

Skills have 4 stats:
- Power: Influences the amount of damage/healing done by the skill
- Mana Cost: The amount of mana required to use the skills
- Target(s): The targets of the skill. (Single Enemy/Ally, All Enemies/Allies, Self)
- Accuracy: How likely the attack is to hit
- Effect: Any additional effects that the skill inflicts.

## Items
Items are scattered amongst carriages in Train to Atlassa, and the player can attempt to find them using the *explore* command. 

Items are split into 3 categories: Armor, Weapons, Consumables.

Armor and weapons have a *boost* stat. This stat determines how effective the item is.
- Armor: 
  - Adds *boost* amount of defense
  - Adds 100 x *boost* amount of max health
- Weapons:
  - Adds *boost* amount of attack
  - Adds 100 x *boost* amount of max mana
- Consumables:
  - Each consumable has a unique effect. 
  - In most cases, the description should tell the player what the consumable will do.

## Status Effects
Status effects take effect at the start of the Entity's turn.
Train to Atlassa implements multiple status effects:
- Poison:
  - Lasts 3 turns
  - -5% max HP each turn
- Burn:
  - Lasts 2 turns
  - -10% max HP each turn
- Shield:
  - Lasts 1 turn
  - +10 Defense, +50 HP
- Motivated:
  - Lasts 2 turns
  - Each turn, +5 Attack, +5 Defense
- Vulnerable:
  - Each turn, -30 Defense
- Frostbite
  - Lasts 
  - -8% max HP each turn
- Purified:
  - Lasts 1 turn
  - Removes all prior effects
- Blessing:
  - Lasts 3 turns
  - Each turn, +10 Defense

## Combat
### HP
### MP
### Items
## Enemies
## Allies

### Weapons
### Consumables
### Armor


# Story
TODO

# Licence
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.