import pygame
from sys import exit

width, height = 800,400

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bãrdou")
clock = pygame.time.Clock()
game_active = True 
start_time = 0
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/Ground.png").convert()

score_surface = test_font.render("Bardou", False, (125,125,0))
score_rect = score_surface.get_rect(midtop=(400,25))

snail_surface = pygame.image.load("graphics/chico_novo_jogo.png").convert_alpha()
snail_surface = pygame.transform.scale(snail_surface, (150,100))
snail_rect = snail_surface.get_rect(midbottom=(800,300))
snail_speed = 3

player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (100,300))
player_speed = 2
player_facing_right = True

gravity = 0

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf= test_font.render(f'{current_time/1000:.1f}s', False, (120,120,120))
    score_rect = score_surf.get_rect(center = (400,75))
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
    move_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:            
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_rect.bottom -= 50
                    gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:            
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_rect.bottom -= 50
                    gravity = -20
        else:
            if event.type == pygame.KEYDOWN:            
                if event.key == pygame.K_SPACE:
                    game_active = True
                    player_rect.left = 100
                    snail_rect.right = 800
                    gravity = 0
                    snail_speed = 3
                    start_time = pygame.time.get_ticks()
                    
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score_rect_color = pygame.draw.rect(screen, (0,225,225),score_rect,1,10)
        screen.blit(score_surface,score_rect)
        display_score()

        if snail_rect.right <= 0:
            snail_rect.left = 800
            snail_speed += 1

        snail_rect.left -= snail_speed
        screen.blit(snail_surface, snail_rect)

        line = pygame.draw.line(screen, color=(100,100,100), start_pos=player_rect.center, end_pos= pygame.mouse.get_pos())
        circle = pygame.draw.ellipse(screen,color=(220,220,0),rect= pygame.Rect(700, 0, 100, 100))
        
        if player_rect.bottom < 300:
            gravity += .75
            player_rect.top += gravity

        if player_rect.bottom > 300:
            player_rect.bottom = 300
        
        if player_rect.left >= 800:
            player_rect.right = 0

        screen.blit(player_surf, player_rect)

        if player_rect.colliderect(snail_rect):
            game_active = False
    else:
        screen.fill((255,0,0))
         

    pygame.display.update()
    clock.tick(60) 