import pygame

class Image(object):
	def __init__(self, x_pos, y_pos, image_path, width=1, height=1):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.image_path = image_path
		self.width = width
		self.height = height

		self.image = pygame.image.load(self.image_path)
		img_w, img_h = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (round(img_w * self.width), round(img_h * self.height)))

		self.raw_width, self.raw_height = self.image.get_size()

	def draw(self, surf):
		surf.blit(self.image, (self.x_pos - self.raw_width / 2, self.y_pos - self.raw_height / 2))
