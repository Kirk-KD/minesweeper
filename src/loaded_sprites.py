import pygame
import os

pygame.init()

mine_dict = {}
for file in os.listdir('./sprites'):
	if file.endswith('.png'):
		mine_dict[file.split('.')[0]] = pygame.image.load(f'./sprites/{file}')
