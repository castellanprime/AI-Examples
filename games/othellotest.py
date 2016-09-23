#!/usr/bin/env python

"""
File: othellotest.py
Date: Sept 17, 2016
Author: Okusanya David
"""
import unittest
from othello import Othello

class OthelloTest(unittest.TestCase):

	def test_assignPlayer(self):
		o = Othello()
		self.assertEqual(o.PLAYER_WHITE, 2)
		self.assertEqual(o.PLAYER_BLACK, 1)

if __name__ == '__main__':
	unittest.main()