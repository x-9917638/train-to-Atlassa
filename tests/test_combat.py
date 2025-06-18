import unittest
from game.core.combat import CombatSystem
from game.core.entities import Player, Enemy
from game.core.skills import Skills

class TestCombatSystem(unittest.TestCase):
    def setUp(self):
        self.combat_system = CombatSystem(Player("Bob"), [Enemy('Goblin', 10, 10, 10, 10), Enemy('Skelteton', 5, 7, 3, 5)])
        

    def test_display_enemies(self):
        pass

    def test_display_skills(self):
        self.combat_system.player.skill_hand = [Skills["Basic Attack"], Skills["Power Strike"]] # Hardcode some skills in the Player's hand for testing
        self.assertEqual(self.combat_system._get_skills(), ["1. Basic Attack (Cost: 0 MP) - A simple attack", "2. Power Strike (Cost: 10 MP) - A powerful strike", ])
        self.combat_system.player.skill_hand = [] # Reset the player hand

    def test_handle_player_action(self):
        self.combat_system._get_player_action()
    
