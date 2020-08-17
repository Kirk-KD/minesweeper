"""
@TODO:
	- set flags    : done
	- remove flags : done
	- GUI          : paused
	- win          : done
	- lose         : done
	- sounds       : doing
	?- menu
"""

import pygame
import random
import sys

from .tile_map import TileMap
from .text import Text
from .image import Image
from .funcs import in_between, sec_to_time_str, play_sound

pygame.init()

passed = 0
def minesweeper(t_width):
	global passed
	passed = t_width

	## GAME CONSTANTS DATA ---------------------
	win_width = 600
	win_height = 400
	surf = pygame.display.set_mode((win_width, win_height))

	# easy: 50; medium: 40; hard: 20;
	tile_width = t_width if (400 % t_width == 0 and t_width < 100 and t_width > 5) else 40

	tile_map_width = (win_width - 200) // tile_width
	tile_map_height = win_height // tile_width

	num_of_mines = round(tile_map_width * tile_map_height * (1 / 8))
	# num_of_mines = 5

	## MAP -------------------------------------
	game_map = TileMap(tile_map_width, tile_map_height, tile_width, num_of_mines)

	## IN-GAME DATA VARIABLES ------------------
	mouse_over_row_i = 0
	mouse_over_col_i = 0

	flags_left = num_of_mines
	clicks = 0

	game_status = 0

	## ON-SCREEN UIs ---------------------------
	timer_sec = 0
	timer_label = Text(505, 20, text=sec_to_time_str(timer_sec), color=(255, 255, 255), size=25)

	flag_label = Text(525, 50, text=f'{flags_left} Left', color=(200, 200, 200), size=21)
	flag_img = Image(467, 50, './sprites/flag.png', 1.5, 1.5)

	clicks_lable = Text(525, 85, text=f'{clicks}', color=(200, 200, 200), size=21)
	clicks_img = Image(467, 85, './sprites/click.png', 1.5, 1.5)

	restart_lable = Text(500, 140, text='Restart', color=(200, 200, 200), size=27)

	win_lose_label = Text(500, 320, text='', color=(210, 210, 210), size=35)

	UIs = [timer_label, flag_label, flag_img, restart_lable, win_lose_label, clicks_lable, clicks_img]

	## TIMING ----------------------------------
	timer_eid = pygame.USEREVENT + 1
	pygame.time.set_timer(timer_eid, 1000)

	## FUNCTIONS -------------------------------
	def mouse_pos_to_index():
		mx, my = pygame.mouse.get_pos()
		# print(f'mouse X: {mx} mouse Y: {my}')
		row_i = my // tile_width
		col_i = mx // tile_width
		return row_i, col_i

	def reveal_near_clear_tiles(tile, game_map, flags_left):
		# reveal an area of safe tiles
		tiles_to_check = tile.get_near_tiles(game_map)
		for t in tiles_to_check:
			t_near = t.get_near_tiles(game_map)
			for in_t in t_near:
				if in_t not in tiles_to_check and in_t.mines_count == 0:
					tiles_to_check.append(in_t)

		# reveal the neighbour tiles of the safe tiles
		for t in tiles_to_check:
			game_map.map[t.row_i][t.col_i].is_revealed = True
			for r, c in game_map.map[t.row_i][t.col_i].get_near_indexes():
				if in_between(r, 0, game_map.height - 1) and in_between(c, 0, game_map.width - 1):
					if (temp := game_map.map[r][c]).mines_count != -1:
						if temp.is_flag:
							temp.is_flag = False
							flags_left += 1
						temp.is_revealed = True

		return game_map, flags_left

	end_mode = 0
	## MAIN GAME LOOP --------------------------
	playing = True
	while playing:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				end_mode = 0
				playing = False

			elif e.type == pygame.MOUSEBUTTONDOWN:
				if restart_lable.mouse_hovering(*pygame.mouse.get_pos()):
					end_mode = 1
					playing = False

				if game_status != 0 or (mp := pygame.mouse.get_pos())[0] > 400 or mp[1] > 400:
					continue

				clicks += 1
				clicked_tile = game_map.map[mouse_over_col_i][mouse_over_row_i]

				if e.button == 1: # LMB
					if not clicked_tile.is_flag:
						if (c := clicked_tile.mines_count) > 0:
							play_sound(f'click_{c}')

						clicked_tile.is_revealed = True

						if clicked_tile.mines_count == 0:
							play_sound('multi_reveal')
							game_map, flags_left = reveal_near_clear_tiles(clicked_tile, game_map, flags_left)

						# lose if clicked on a mine
						elif clicked_tile.is_mine:
							play_sound('lose')

							game_status = -1
							for y in game_map.map:
								for t in y:
									if not (t.is_mine and t.is_flag):
										t.is_revealed = True
										if t.is_flag:
											flags_left += 1

				elif e.button == 3: # RMB
					play_sound('flag')
					if clicked_tile.is_flag:
						clicked_tile.is_flag = False
						flags_left += 1
					elif not clicked_tile.is_revealed:
						if flags_left > 0:
							clicked_tile.is_flag = True
							flags_left -= 1

			elif e.type == timer_eid:
				if game_status != 0:
					continue

				timer_sec += 1
				timer_label.text = sec_to_time_str(timer_sec)

		# win if all the tiles are revealed or flagged
		if all([(t.is_revealed or t.is_flag) for r in game_map.map for t in r]) and game_status != -1:
			game_status = 1

		# get mouse pos
		m_row_i, m_col_i = mouse_pos_to_index()
		if in_between(m_row_i, 0, tile_map_height - 1) and in_between(m_col_i, 0, tile_map_width - 1):
			mouse_over_row_i, mouse_over_col_i = m_row_i, m_col_i
			game_map.map[mouse_over_col_i][mouse_over_row_i].is_hovering = True

		# draw
		surf.fill((90, 90, 90))

		for y in game_map.map:
			for t in y:
				t.draw(surf)
				t.is_hovering = False

		for UI in UIs:
			UI.draw(surf)

		# game status
		if game_status == 1:
			win_lose_label.text = 'WIN'
		elif game_status == -1:
			win_lose_label.text = 'LOSE'
		else:
			win_lose_label.text = ''

		# update UI
		flag_label.text = f'{flags_left} Left'
		clicks_lable.text = f'{clicks}'

		if restart_lable.mouse_hovering(*pygame.mouse.get_pos()):
			restart_lable.size = 29
			restart_lable.color = (210, 210, 210)
		else:
			restart_lable.size = 27
			restart_lable.color = (200, 200, 200)

		pygame.display.update()
	## END OF MAIN GAME LOOP -------------------
	if end_mode == 1:
		minesweeper(passed)
	# else:
	# sys.exit()
	# 	from .. import minesweeper
## END OF MAIN GAME FUNCTION ========================================

# while True:
# 	minesweeper(40)

