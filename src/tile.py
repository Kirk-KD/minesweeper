import pygame
import random

from .loaded_sprites import mine_dict
from .funcs import deep_copy, in_between

class Tile(object):
	def __init__(self, row_i, col_i, width):
		self.row_i = row_i
		self.col_i = col_i
		self.x_pos = row_i * width
		self.y_pos = col_i * width
		self.width = width

		self.is_mine = False
		self.is_flag = False
		self.mines_count = None
		self.mine_sprite = None

		self.is_revealed = False
		self.is_hovering = False

	def get_near_mine_count(self, tile_map) -> int:
		if not self.is_mine:
			t_map = deep_copy(tile_map.map)
			near_tiles = self.get_near_tiles(tile_map)

			mines_count = 0
			for t in near_tiles:
				if t.is_mine:
					mines_count += 1

			return mines_count

		return -1

	def get_near_indexes(self) -> list:
		near_indexes = [
			(self.row_i - 1, self.col_i - 1),
			(self.row_i - 1, self.col_i    ),
			(self.row_i - 1, self.col_i + 1),
			(self.row_i    , self.col_i - 1),
			(self.row_i    , self.col_i + 1),
			(self.row_i + 1, self.col_i - 1),
			(self.row_i + 1, self.col_i    ),
			(self.row_i + 1, self.col_i + 1)
		]
		return near_indexes

	def get_near_tiles(self, tile_map) -> list:
		t_map = deep_copy(tile_map.map)

		near = []
		near_indexes = self.get_near_indexes()

		for r, c in near_indexes:
			if in_between(r, 0, tile_map.height - 1) and in_between(c, 0, tile_map.width - 1):
				near.append(t_map[r][c])

		return near

	def draw(self, surf):
		bg = pygame.Rect((self.x_pos, self.y_pos), (self.width, self.width))
		fg = pygame.Rect((self.x_pos + 1, self.y_pos + 1), (self.width - 2, self.width - 2))

		pygame.draw.rect(surf, (168, 168, 168), bg)
		if self.is_revealed:
			parsed_mine_sprite = pygame.transform.scale(self.mine_sprite, (self.width - 2, self.width - 2))
			surf.blit(parsed_mine_sprite, (self.x_pos + 1, self.y_pos + 1))
		elif self.is_flag:
			parsed_flag_sprite = pygame.transform.scale(mine_dict['flag'], (self.width - 2, self.width - 2))
			surf.blit(parsed_flag_sprite, (self.x_pos + 1, self.y_pos + 1))
		else:
			if self.is_hovering:
				pygame.draw.rect(surf, (199, 199, 199), fg)
			else:
				pygame.draw.rect(surf, (219, 219, 219), fg)

