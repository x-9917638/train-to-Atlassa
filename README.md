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
## Skills
## Status Effects
## Combat
## Enemies
## Allies
## Items
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