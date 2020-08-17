import pygame
import random

from .tile import Tile
from .loaded_sprites import mine_dict

class TileMap(object):
	def __init__(self, width, height, grid_size, mines):
		self.width = width
		self.height = height
		self.grid_size = grid_size
		self.map = [[Tile(row_i, col_i, grid_size) for col_i in range(width)] for row_i in range(height)]

		while mines != 0:
			if not self.map[(temp_row := random.randint(0, height - 1))][(temp_col := random.randint(0, width - 1))].is_mine:
				self.map[temp_row][temp_col].is_mine = True
				mines -= 1

		for y in self.map:
			for x in y:
				x.mines_count = x.get_near_mine_count(self)
				if x.is_mine:
					x.mine_sprite = mine_dict['mine']
				else:
					x.mine_sprite = mine_dict['mine_n{n}'.format(n=x.mines_count)]

