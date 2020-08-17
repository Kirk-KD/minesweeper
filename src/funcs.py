import pygame
from .loaded_sounds import sounds

pygame.init()

def deep_copy(list_2d) -> list:
	res = []
	for l in list_2d:
		res.append(l.copy())
	return res

def in_between(num, min_, max_, include_start_end=True) -> bool:
	if include_start_end:
		return num >= min_ and num <= max_
	else:
		return num > min_ and num < max_

def sec_to_time_str(sec):
	m, s = divmod(sec, 60)
	h, m = divmod(m, 60)

	if s < 10:
		s = f'0{s}'
	if m < 10:
		m = f'0{m}'
	if h < 10:
		h = f'0{h}'

	return f'{h}:{m}:{s}'

def play_sound(sound_name):
	pygame.mixer.Sound.play(sounds[sound_name])
