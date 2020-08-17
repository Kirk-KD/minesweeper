import pygame

class Button(object):
	def __init__(self, pos_x, pos_y, width, height, func):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.width = width
		self.height = height
		self.func = func
