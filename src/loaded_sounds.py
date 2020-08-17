import pygame
import os

pygame.init()

sounds = {}
for file in os.listdir('./sounds'):
	if file.endswith('.wav'):
		sounds[file.split('.')[0]] = pygame.mixer.Sound(f'./sounds/{file}')
