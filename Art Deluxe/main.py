import pygame
from sys import exit
import ctypes
import math 

user32 = ctypes.windll.user32

screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
width, height = screensize
aspect = width / height

pygame.init()
screen = pygame.display.set_mode((width, height - 50))
pygame.display.set_caption("Flappy Bãrdou")

clock = pygame.time.Clock()
game_active = True 
start_time = 0

test_font = pygame.font.Font(r"Games\Art Deluxe\font\Pixeltype.ttf", 50)

sky_surface = pygame.image.load(r"Games\Art Deluxe\graphics/Sky.png").convert()
sky_surface = pygame.transform.scale(sky_surface, (width,height))
ground_surface = pygame.image.load(r"Games\Art Deluxe\graphics/Ground.png").convert()
ground_surface = pygame.transform.scale(ground_surface, (width,height))

title_surface = test_font.render("Bardou", False, (125,125,0))
title_rect = title_surface.get_rect(midtop=(width / 2,25))

snail_surface = pygame.image.load(r"Games\Art Deluxe\graphics/chico_novo_jogo.png").convert_alpha()
snail_surface = pygame.transform.scale(snail_surface, (200,100))
snail_rect = snail_surface.get_rect(midbottom=(width,300))
snail_speed = 3
snail_x_pos = snail_rect.x

player_surf = pygame.image.load(r"Games\Art Deluxe\graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (100,300))
player_speed = 3
player_facing_right = True
player_score = 0
player_x_pos = player_rect.x
player_moving_rope = False

gravity = 0
def display_timer():
    current_time = pygame.time.get_ticks() - start_time
    timer_surf= test_font.render(f'{current_time/1000:.1f}s', False, (120,120,120))
    timer_rect = timer_surf.get_rect(center = (width/2,75))
    screen.blit(timer_surf, timer_rect)

def display_score():
    score_surf= test_font.render(f'{player_score}', False, (120,120,120))
    score_rect = score_surf.get_rect(center = (width/2,75+50))
    screen.blit(score_surf, score_rect)

def move_player():
    global gravity, player_surf, player_facing_right
    keys = pygame.key.get_pressed()
    if keys[ord('d')]:
        player_rect.x += player_speed
        if not player_facing_right:
            player_surf = pygame.transform.flip(player_surf, 1,0)
            player_facing_right = True

    if keys[ord('a')]:
        player_rect.x -= player_speed
        if  player_facing_right:
            player_surf = pygame.transform.flip(player_surf, 1,0)
            player_facing_right = False

    if keys[ord('w')] and player_rect.bottom == 300:        
        player_rect.bottom -= 25
        gravity = -15

while True:
    if not player_moving_rope:
        move_player()
    else:        
        player_rect.center += direction * player_speed
        if player_rect.collidepoint(mouse_pos):
            player_moving_rope = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:            
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_rect.bottom -= 5
                    gravity = -20
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
                player_pos = pygame.math.Vector2(player_rect.center)
                direction = mouse_pos - player_pos
                #direction.x /= aspect
                direction = direction.normalize_ip()
                player_moving_rope = True
                continue
                mouse_x, mouse_y = event.pos
                
                dy = abs(-mouse_y + player_rect.centery)
                dx = abs(mouse_x - player_rect.centerx)
                distance = math.sqrt(dx ** 2 + dy ** 2)
                theta = math.atan(dy / dx) if dx != 0  else math.pi / 2
                tempo = abs(distance) / player_speed
                vy = dy / tempo
                vx = (player_speed-vy)*dx / tempo
                player_moving_rope = True
                tempo_x = dx / vx
                tempo_y = dy / vy
                print(mouse_x, mouse_y, player_rect.x, player_rect.y)
                print(vx, vy, dx, dy, tempo_x, tempo_y)
                
        else:
            if event.type == pygame.KEYDOWN:            
                if event.key == pygame.K_SPACE:
                    game_active = True
                    player_rect.left = 100
                    snail_rect.right = 800
                    gravity = 0
                    snail_speed = 3
                    player_score = 0
                    player_moving_rope = False
                    start_time = pygame.time.get_ticks()
                    
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        title_rect_color = pygame.draw.rect(screen, (0,225,225),title_rect,1,10)
        screen.blit(title_surface,title_rect)
        
        display_timer()
        display_score()

        if player_x_pos < snail_x_pos and player_rect.x > snail_rect.x:
                player_score += 1
                player_x_pos = player_rect.x
                snail_x_pos = snail_rect.x
                
        player_x_pos = player_rect.x
        snail_x_pos = snail_rect.x

        if snail_rect.right <= 0:
            snail_rect.left = width
            snail_speed += 1

        snail_rect.left -= snail_speed
        screen.blit(snail_surface, snail_rect)

        line = pygame.draw.line(screen, color=(100,100,100), start_pos=player_rect.center, end_pos= pygame.mouse.get_pos())
        circle = pygame.draw.ellipse(screen,color=(255,255,0),rect= pygame.Rect(width-100, 0, 100, 100))
        
        if player_rect.bottom < 300 and not player_moving_rope:
            gravity += .75
            player_rect.top += gravity
            
        if player_rect.bottom > 300 and not player_moving_rope:
            player_rect.bottom = 300
        
        if player_rect.left >= width:
            player_rect.right = 0

        screen.blit(player_surf, player_rect)

        if player_rect.colliderect(snail_rect):
            game_active = False

    else:
        screen.fill((255,0,0))
         
    pygame.display.update()
    clock.tick(60) 