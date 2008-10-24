# ###################################################
# Copyright (C) 2008 The OpenAnno Team
# team@openanno.org
# This file is part of OpenAnno.
#
# OpenAnno is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from building import Building, Selectable
from game.world.production import SecondaryProducer, PrimaryProducer
from buildable import BuildableSingleWithSurrounding, BuildableSingle
from game.gui.tabwidget import TabWidget
from game.util.point import Point
import game.main

class AnimalFarm(Selectable, SecondaryProducer, BuildableSingleWithSurrounding, Building):
	_surroundingBuildingClass = 18
	""" This class builds pasturage in the radius automatically,
	so that farm animals can graze there """

	def create_carriage(self):
		self.animals = []
		animals = game.main.db("SELECT animal, count from data.animals where building = ?", self.id)
		for (animal,number) in animals:
			for i in xrange(0,number):
				self.animals.append(game.main.session.entities.units[animal](self))

		self.local_carriages.append(game.main.session.entities.units[7](self))

class Lumberjack(Selectable, SecondaryProducer, BuildableSingleWithSurrounding, Building):
	_surroundingBuildingClass = 17
	"""Class representing a Lumberjack."""

class Weaver(Selectable, SecondaryProducer, BuildableSingle, Building):
	pass

class Fisher(Selectable, PrimaryProducer, BuildableSingle, Building):

	def show_menu(self):
		game.main.session.ingame_gui.show_menu(TabWidget(4, self))

	@classmethod
	def isGroundBuildRequirementSatisfied(cls, x, y, island, **state):
		#todo: check cost line
		coast_tile_found = False
		for xx,yy in [ (xx,yy) for xx in xrange(x, x + cls.size[0]) for yy in xrange(y, y + cls.size[1]) ]:
			print "x y:", xx, yy
			tile = island.get_tile(Point(xx,yy))
			classes = tile.__class__.classes
			print classes
			if 'coastline' in classes:
				coast_tile_found = True
			elif 'constructible' not in classes:
				return None

		return {} if coast_tile_found else None

class Church(Selectable, PrimaryProducer, BuildableSingle, Building):
	pass
