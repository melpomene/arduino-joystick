#!/usr/bin/env python
# encoding: utf-8
"""
Test.py

Created by christopher on 2011-05-21.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import unittest
import Read

class Test(unittest.TestCase):
	def setUp(self):
		self.r = Read.JoystickReader()
		pass
		
	def test_Read(self):
		self.r.start()
		

    
if __name__ == '__main__':
	unittest.main()