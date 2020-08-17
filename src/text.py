import pygame

pygame.init()

class Text(object):
	def __init__(self, x_pos, y_pos, text, color=(0, 0, 0), bg_color=None, size=36, font_type=pygame.font.get_default_font()):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.text = str(text)
		self.color = color
		self.bg_color = bg_color
		self.size = size
		self.font_type = font_type

		self.font = pygame.font.Font(self.font_type, self.size)
		self.text_surf = self.font.render(self.text, True, self.color, self.bg_color)

	def draw(self, surf):
		# update size, text and color
		self.font = pygame.font.Font(self.font_type, self.size)
		self.text_surf = self.font.render(self.text, True, self.color, self.bg_color)

		# then draw
		t_width = self.text_surf.get_width()
		t_height = self.text_surf.get_height()
		surf.blit(self.text_surf, (self.x_pos - t_width / 2, self.y_pos - t_height / 2))

	def mouse_hovering(self, mouse_x, mouse_y):
		con_1 = mouse_x >= self.x_pos - self.text_surf.get_width() / 2
		con_2 = mouse_x <= self.x_pos + self.text_surf.get_width() / 2
		con_3 = mouse_y >= self.y_pos - self.text_surf.get_height() / 2
		con_4 = mouse_y <= self.y_pos + self.text_surf.get_height() / 2

		return con_1 and con_2 and con_3 and con_4
