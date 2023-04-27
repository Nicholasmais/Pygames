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
    if moving_object.rect.right > object_to_check.rect.left and moving_object.rect.centerx < object_to_check.rect.centerx and moving_object.direction[0] > 0:        
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[0] = moving_object.direction[0]
        object_to_check.moving = True

        moving_object.direction[0] *= -1
        moving_object.pos[0] = object_to_check.rect.left - moving_object.radius
        return True

    elif moving_object.rect.left < object_to_check.rect.right and moving_object.rect.centerx > object_to_check.rect.centerx and moving_object.direction[0] < 0:
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[0] = moving_object.direction[0]
        object_to_check.moving = True

        moving_object.direction[0] *= -1
        moving_object.pos[0] = object_to_check.rect.right + moving_object.radius
        return True

    if moving_object.direction[1] > 0:
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[1] = moving_object.direction[1]
        object_to_check.moving = True

        moving_object.direction[1] *= -1
        moving_object.pos[1] = object_to_check.rect.top - moving_object.radius
        return True
    else:
        object_to_check.speed = moving_object.speed 
        object_to_check.direction[1] = moving_object.direction[1]
        object_to_check.moving = True

        moving_object.direction[1] *= -1
        moving_object.pos[1] = object_to_check.rect.bottom + moving_object.radius
        return True

class Obstaculo:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.pos = pygame.math.Vector2(x, y)
        self.color = color
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
    Obstaculo(0.175*width, 0.2*height, 30, 30, (255, 0, 0)),  # vermelho
    Obstaculo(0.2*width, 0.2*height, 30, 30, (0, 255, 0)),  # verde
    Obstaculo(0.225*width, 0.2*height, 30, 30, (0, 0, 255)),  # azul
    Obstaculo(0.25*width, 0.2*height, 30, 30, (255, 255, 0)),  # amarelo
    Obstaculo(0.275*width, 0.2*height, 30, 30, (255, 0, 255)),  # roxo
    Obstaculo(0.2*width - 15, 0.25*height, 30, 30, (255, 128, 0)),  # laranja
    Obstaculo(0.225*width - 15, 0.25*height, 30, 30, (0, 255, 255)),  # ciano
    Obstaculo(0.25*width - 15, 0.25*height, 30, 30, (128, 0, 255)),  # roxo escuro
    Obstaculo(0.275*width - 15, 0.25*height, 30, 30, (128, 128, 128)),  # cinza
    Obstaculo(0.2*width , .3*height, 30, 30, (255, 255, 255)),  # branco
    Obstaculo(0.225*width , 0.3*height, 30, 30, (0, 0, 0)),  # preto
    Obstaculo(0.25*width , 0.3*height, 30, 30, (128, 128, 0)),  # verde-escuro
    Obstaculo(0.225*width - 15, 0.35*height, 30, 30, (255, 0, 128)),  # rosa
    Obstaculo(0.25*width - 15, 0.35*height, 30, 30, (0, 128, 128)),  # turquesa
    Obstaculo(0.2375*width - 13.5, 0.4*height, 30, 30, (128, 0, 128))  # roxo claro
]

friction = .05
moving = False
moving_obstaculo = False
time = 0

ball = Obstaculo(height=circle_radius*2, width=circle_radius*2, x=circle_pos[0], y=circle_pos[1],color= (255,255,255))

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
            ball.direction = mouse_pos - ball.pos
            ball.speed = (ball.direction[0]**2 + ball.direction[1]**2)**.5/30
            if ball.direction.length() > 0:
                ball.direction.normalize_ip()
                ball.moving = True

    if ball.moving:
        ball.pos += ball.direction * ball.speed
        ball.speed -= friction*ball.time
        ball.time += .05

        if ball.pos[0] > (width/2) - ball.radius:
            ball.direction[0] *= -1
        if ball.pos[0] < ball.radius:
            ball.direction[0] *= -1
        if ball.pos[1] < ball.radius:
            ball.direction[1] *= -1
        if ball.pos[1] > height - ball.radius:
            ball.direction[1] *= -1
        if abs(ball.pos[0]) > 1.5*width/2 or abs(ball.pos[1]) > 1.5*width:
            ball.pos = [circle_pos[0], circle_pos[1]]
            
        for obstaculo in obstaculos:
            if ball.rect.colliderect(obstaculo):
                treat_collision(ball, obstaculo)                
            for outro_obstaculo in obstaculos:
                if obstaculo.moving and outro_obstaculo != obstaculo and obstaculo.rect.colliderect(outro_obstaculo.rect):
                    treat_collision(obstaculo, outro_obstaculo)                    
                    # if outro_obstaculo.moving:
                    #     treat_collision(outro_obstaculo, ball)
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

        pygame.draw.ellipse(screen, color=obstaculo.color,
                            rect=obstaculo.rect)

    pygame.draw.ellipse(screen, color=circle_color, rect=ball.rect)
    pygame.draw.ellipse(screen, color=circle_goal_color, rect=circle_goal_rect)

    pygame.display.flip()

pygame.quit()
