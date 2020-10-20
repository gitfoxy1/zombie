""" Test games.py """

import unittest

import pygame

from games import Game


class Test(unittest.TestCase):
    """ Test games.py """

    def test_positive__update_active_character(self):
        """ Game.update_active_character()
            ход переходит к следующему герою
        """
        pygame.init()
        game = Game(2)
        characters = game.characters.sprites()
        hero1 = characters[0]
        hero2 = characters[1]

        # ходы у hero1 ещё не закончились
        # hero1 actions=3/3 active=True
        # hero2 actions=3/3 active=False
        game.update_active_character()
        self.assertTrue(hero1.active, msg="Expected: hero1.active=True")
        self.assertFalse(hero2.active, msg="Expected: hero2.active=False")
        self.assertIs(hero1.actions, 3, msg="Expected: hero1.actions=3/3")
        self.assertIs(hero2.actions, 3, msg="Expected: hero2.actions=3/3")

        # ходы у hero1 закончились и ход переходит hero2
        # hero1: actions=0/3 active=True  -> actions=3/3 active=False
        # hero2: actions=3/3 active=False -> actions=3/3 active=True
        hero1.actions = 0
        game.update_active_character()
        self.assertFalse(hero1.active, msg="Expected: hero2.active=False")
        self.assertTrue(hero2.active, msg="Expected: hero2.active=True")
        self.assertIs(hero1.actions, 3, msg="Expected: hero1.actions=3/3")
        self.assertIs(hero2.actions, 3, msg="Expected: hero2.actions=3/3")

        # ходы у hero2 ещё не закончились
        # hero1: actions=0/3 active=True  -> actions=3/3 active=False
        # hero2: actions=3/3 active=False -> actions=3/3 active=True
        hero2.actions = 2
        game.update_active_character()
        self.assertFalse(hero1.active, msg="Expected: hero2.active=False")
        self.assertTrue(hero2.active, msg="Expected: hero2.active=True")
        self.assertIs(hero1.actions, 3, msg="Expected: hero1.actions=3/3")
        self.assertIs(hero2.actions, 2, msg="Expected: hero2.actions=3/3")

        # ходы у hero2 закончились и ход переходит hero1
        # hero1 actions=3/3 active=True
        # hero2 actions=3/3 active=False
        hero2.actions = 0
        game.update_active_character()
        self.assertTrue(hero1.active, msg="Expected: hero1.active=True")
        self.assertFalse(hero2.active, msg="Expected: hero2.active=False")
        self.assertIs(hero1.actions, 3, msg="Expected: hero1.actions=3/3")
        self.assertIs(hero2.actions, 3, msg="Expected: hero2.actions=3/3")
        print()
        print()


if __name__ == '__main__':
    unittest.main()
