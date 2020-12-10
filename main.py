import pygame, sys, random

def draw_floor():
	screen.blit(floor_surface,(floor_x_position, 850))
	screen.blit(floor_surface,(floor_x_position + 500, 850))

def create_pipe():
	random_pipe_position = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_position))
	top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_position - 300))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1000:
			screen.blit(pipe_surface, pipe) 
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (250, 100))
		screen.blit(score_surface, score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (250, 100))
		screen.blit(score_surface, score_rect)

		high_score_surface = game_font.render(f'High Score:{int(high_score)}', True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect(center = (250, 550))
		screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 256)
screen = pygame.display.set_mode((500, 1000))
clock = pygame.time.Clock()

title = pygame.display.set_caption('Flappy Birds')
icon = pygame.image.load('flappy.png')
pygame.display.set_icon(icon)

game_font = pygame.font.Font('04B_19.ttf',40)

#Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

bkg_surface = pygame.image.load('C:/Users/SANGRAM/Desktop/Python/FPasset/background-day.png').convert()
bkg_surface = pygame.transform.scale2x(bkg_surface)

floor_surface = pygame.image.load('C:/Users/SANGRAM/Desktop/Python/FPasset/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

bird_surface = pygame.image.load('C:/Users/SANGRAM/Desktop/Python/FPasset/bluebird-midflap.png').convert_alpha()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, 512))

pipe_surface = pygame.image.load('C:/Users/SANGRAM/Desktop/Python/FPasset/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 800)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('C:/Users/SANGRAM/Desktop/Python/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (250, 500))

flap_sound = pygame.mixer.Sound('C:/Users/SANGRAM/Desktop/Python/audio/wing.wav')
death_sound = pygame.mixer.Sound('C:/Users/SANGRAM/Desktop/Python/audio/hit.wav')
score_sound = pygame.mixer.Sound('C:/Users/SANGRAM/Desktop/Python/audio/point.wav')
score_sound_count = 100

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 12
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100, 512)
				bird_movement = 0
				score = 0
				
		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.blit(bkg_surface,(0, 0))

	if game_active:
	# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)
		game_active = check_collision(pipe_list)

		#Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		score += 0.01
		score_display('main_game')
		score_sound_count -= 1
		if score_sound_count <= 0:
			score_sound.play()
			score_sound_count = 100
	else:
		screen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game_over')

	#Floor
	floor_x_position -= 1
	draw_floor()
	if floor_x_position <= -500:
		floor_x_position = 0
	screen.blit(floor_surface,(floor_x_position, 850))

	pygame.display.update()
	clock.tick(120)
