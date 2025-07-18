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

## Default
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

## Levels
Every entity in the game has a level. Levels dictate the amount of stats an entity has.

The player can gain experience by defeating enemies. Upon levelling up, they will receive a random new skills if available. In addition, depending on their profession, they will receive stat points.

## Skills
The player has a skill hand, and a skill deck. The player can check their deck with the **skills** command, but cannot check their hand before entering battle. Upon entering battle, the player can only use skills from their hand.

There are a variety of skills in Train to Atlasssa, and each class has their own dedicated skills.

The player also begins with 2 default skills: Gambling Fever, and Basic Attack

Skills have 4 stats:
- Power: Influences the amount of damage/healing done by the skill
- Mana Cost: The amount of mana required to use the skills
- Target(s): The targets of the skill. (Single Enemy/Ally, All Enemies/Allies, Self)
- Accuracy: How likely the attack is to hit
- Effect: Any additional effects that the skill inflicts.

## Sections
The game is comprised of 4 sections, which group multiple carriages together. Each section unlocks new skills, items, bosses and enemies.

To proceed to the next section, the player must defeat the boss in the current section.

## Carriages
Each "room" that the player progresses through is a carriage. There are four types of carriage:
- Ally: Has a 50% chance to have an ally in the carriage
- Normal: 1-2 Enemies will be in this carriage
- Challenge: 3-4 Enemies will be in this carriage
- Boss: 1-2 Bosses will be in this carriage

Each carriage has a chance to have up to 2 items on generation.

## Winning
The player wins once the last boss, located in Carriage 8 of Section 4, has been defeated.

## Items
Items are scattered amongst carriages in Train to Atlassa, and the player can attempt to find them using the *explore* command. 

The explore command has a 50% chance to fail. If it does, the items are removed from the carriage.

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
Train to Atlassa implements turn based combat.
Each turn, the player chooses their action first, then the enemies attack, then finally, allies.

The player can choose from 4 options:
- Attack: Choose and use a skill
- Rest: Take a nap
- Items: Use consumables
- Retreat
  
### HP
Health points. To regain health, specific consumable items can be used, or the player can rest during battle.

### MP
Mana points.
All skills require mana to cast. To regain mana, specific consumable items can be used, or the player can rest during battle.

### Skills
Each turn, a random skill is drawn and placed into the players skill hand. If the player chooses to attack, they can pick and use a skill from their hand.

### Items
During battle, the player can use consumables to gain an advatange. However, this will end their turn.

### Resting
Heal 10% of max health and 10% of max mana.

### Retreating
If the player thinks that they cannot win a battle, they may attempt to use the **retreat** command with a 33% chance of success. 

If successful, this clears the room, however, if failed, penalises the player for -10% of their current health.

## Enemies
There are a wide range of enemies in Train to Atlassa. Each section has its unique pool of enemies for the player to face. 

As the player progresses, enemies also become stronger in order to keep the player engaged.


## Allies
Train to Atlassa generate allies randomly, hence, it is almost guaranteed that unique allys will be encountered each playthrough. In fact, there are 12,800 allies when accounting for name and description alone! 

Allies, like players, have a profession. This includes all the player professions, as well as Priest. Their skills are generated from the same pool that the player's is.

Allies can buff players, or defeat enemies, helping the player to win.

Players can have a maximum of 2 living allies at any time.

# Story
The game is set in a fictional fantasy world, albeit one technologically advanced enough to have trains.

The Hero has just returned from a grand conquest in the Central Grand City, Citadel, where they have slain the Monster King and save the city.

After saving the Grand City of Citadel, the Hero, boards the Train to Atlassa...

Little do they know, the remnants of the Monster King's army is waiting. The Monsters have hijacked the train and are using it to facilitate an invasion of Atlassa, the Capitol of the Dwarves.

The player takes the role of the Hero, where their goal is to retake the train from the monsters.

A tragic fate awaits those of Atlassa if they fail.


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