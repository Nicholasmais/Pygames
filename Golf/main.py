import pygame
import ctypes
import pygame.math

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
width, height = screensize
aspect = width / height
height -= 100

pygame.init()
screen = pygame.display.set_mode((int(width/2), height))
pygame.display.set_caption("Golf")

clock = pygame.time.Clock()
running = True

# Centralize a bola na tela
circle_pos = pygame.math.Vector2(
    int(screen.get_width() / 2), int(screen.get_height()-25))
circle_radius = 17.5
circle_color = (255, 255, 255)

# Desenhe um círculo e obtenha um retângulo que circunscreve o círculo
circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2))
circle_rect = circle_surface.get_rect(center=circle_pos)

circle_goal_pos = pygame.math.Vector2(int(screen.get_width() / 2), int(25))
circle_goal_radius = 25
circle_goal_color = (0, 0, 0)

# Desenhe um círculo e obtenha um retângulo que circunscreve o círculo
circle_goal_surface = pygame.Surface(
    (circle_goal_radius * 2, circle_goal_radius * 2))
circle_goal_rect = circle_goal_surface.get_rect(center=circle_goal_pos)

def treat_collision(moving_object, object_to_check):        
    if moving_object.rect.right > object_to_check.rect.left and moving_object.rect.centerx < object_to_check.rect.centerx and direction[0] > 0:        
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[0] = direction[0]
        object_to_check.moving = True

        direction[0] *= -1
        moving_object.pos[0] = object_to_check.rect.left - moving_object.radius
        return True

    elif moving_object.rect.left < object_to_check.rect.right and moving_object.rect.centerx > object_to_check.rect.centerx and direction[0] < 0:
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[0] = direction[0]
        object_to_check.moving = True

        direction[0] *= -1
        moving_object.pos[0] = object_to_check.rect.right + moving_object.radius
        return True

    if direction[1] > 0:
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[1] = direction[1]
        object_to_check.moving = True

        direction[1] *= -1
        moving_object.pos[1] = object_to_check.rect.top - moving_object.radius
        return True
    else:
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[1] = direction[1]
        object_to_check.moving = True

        direction[1] *= -1
        moving_object.pos[1] = object_to_check.rect.bottom + moving_object.radius
        return True

class Obstaculo:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.pos = pygame.math.Vector2(x, y)
        self.moving = False
        self.time = 0
        self.speed = 0
        self.direction = pygame.math.Vector2([0, 0])
        self.radius = width

    def update(self):
        if self.moving:
            self.rect.center += self.direction * self.speed
            if self.speed <= 0:
                self.moving = False
                self.time = 0


obstaculos = [
    Obstaculo(width/4 - 15, height/2 - 5, 30, 30),
    Obstaculo(width/8 - 15, height/2 - 5, 30, 30),
    Obstaculo(1.5*width/4 - 15, height/2 - 5, 30, 30),
    Obstaculo(width/5.5 - 15, height/4 - 5, 30, 30),
    Obstaculo(1.25*width/4 - 15, height/4 - 5, 30, 30),
    Obstaculo(.75*width/4 - 15, height/1.375 - 5, 30, 30),
    Obstaculo(1.25*width/4 - 15, height/1.375 - 5, 30, 30),
]

friction = .05
moving = False
moving_obstaculo = False
time = 0

ball = Obstaculo(height=circle_radius*2, width=circle_radius*2, x=circle_pos[0], y=circle_pos[1])

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            direction = mouse_pos - ball.pos
            ball.speed = (direction[0]**2 + direction[1]**2)**.5/30
            if direction.length() > 0:
                direction.normalize_ip()
                ball.moving = True

    if ball.moving:
        ball.pos += direction * ball.speed
        ball.speed -= friction*ball.time
        ball.time += .05

        if ball.pos[0] > (width/2) - ball.radius:
            direction[0] *= -1
        if ball.pos[0] < ball.radius:
            direction[0] *= -1
        if ball.pos[1] < ball.radius:
            direction[1] *= -1
        if ball.pos[1] > height - ball.radius:
            direction[1] *= -1
        
        for obstaculo in obstaculos:
            if ball.rect.colliderect(obstaculo):
                treat_collision(ball, obstaculo)
            for outro_obstaculo in obstaculos:
                if obstaculo.moving and outro_obstaculo != obstaculo and obstaculo.rect.colliderect(outro_obstaculo.rect):
                    treat_collision(obstaculo, outro_obstaculo)

        if ball.rect.colliderect(circle_goal_rect):
            ball.pos = pygame.math.Vector2(
                int(screen.get_width() / 2), int(screen.get_height()-25))
            ball.moving = False

        if ball.speed <= 0:
            ball.moving = False
            ball.time = 0

    screen.fill((0, 155, 0))
    ball.rect.center = ball.pos

    for obstaculo in obstaculos:
        if obstaculo.moving:
            obstaculo.speed -= friction*obstaculo.time
            obstaculo.time += .05
            obstaculo.update()

        if obstaculo.rect.x > (width/2) - obstaculo.radius:
            obstaculo.direction[0] *= -1
        if obstaculo.rect.x < obstaculo.radius:
            obstaculo.direction[0] *= -1
        if obstaculo.rect.y < obstaculo.radius:
            obstaculo.direction[1] *= -1
        if obstaculo.rect.y > height - obstaculo.radius:
            obstaculo.direction[1] *= -1

        pygame.draw.ellipse(screen, color=circle_goal_color,
                            rect=obstaculo.rect)

    pygame.draw.ellipse(screen, color=circle_color, rect=ball.rect)
    pygame.draw.ellipse(screen, color=circle_goal_color, rect=circle_goal_rect)

    pygame.display.flip()

pygame.quit()
