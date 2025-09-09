import pygame
import random
import os
import sys

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tom y Jerry: Juego de Evasión")
clock = pygame.time.Clock()

# Cargar imágenes (si no existen, se usarán formas geométricas)
try:
    tom_img = pygame.image.load("tom.png")
    tom_img = pygame.transform.scale(tom_img, (50, 50))
    jerry_img = pygame.image.load("jerry.png")
    jerry_img = pygame.transform.scale(jerry_img, (30, 30))
    background = pygame.image.load("fondo_casa.jpg")
    background = pygame.transform.scale(background, (800, 600))
    has_images = True
except:
    has_images = False
    print("No se encontraron imágenes. Usando formas geométricas.")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Jugador (Tom)
player_size = 50
player_x = 400
player_y = 500
player_speed = 5

# Enemigos (Jerry y amigos)
enemies = []
enemy_size = 30
enemy_speed = 3

# Variables del juego
score = 0
level = 1
game_over = False
font = pygame.font.SysFont(None, 36)

# Función para dibujar jugador (Tom)
def draw_player(x, y):
    if has_images:
        screen.blit(tom_img, (x, y))
    else:
        pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))
        # Dibujar detalles de Tom
        pygame.draw.circle(screen, WHITE, (x + 15, y + 15), 5)  # Ojo
        pygame.draw.circle(screen, WHITE, (x + 35, y + 15), 5)  # Ojo
        pygame.draw.ellipse(screen, YELLOW, (x + 10, y + 35, 30, 10))  # Boca

# Función para dibujar enemigos (Jerry)
def draw_enemy(x, y):
    if has_images:
        screen.blit(jerry_img, (x, y))
    else:
        pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))
        # Dibujar detalles de Jerry
        pygame.draw.circle(screen, BLACK, (x + 10, y + 10), 3)  # Ojo
        pygame.draw.circle(screen, BLACK, (x + 20, y + 10), 3)  # Ojo
        pygame.draw.ellipse(screen, YELLOW, (x + 10, y + 20, 10, 5))  # Boca

# Función para mostrar texto en pantalla
def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Función para mostrar pantalla de inicio
def show_start_screen():
    screen.fill(WHITE)
    if has_images:
        screen.blit(background, (0, 0))
    
    draw_text("TOM Y JERRY: EVASIÓN", BLACK, 250, 100)
    draw_text("Ayuda a Tom a esquivar a Jerry y sus amigos", BLACK, 180, 150)
    draw_text("Usa las flechas izquierda y derecha para moverte", BLACK, 170, 200)
    draw_text("Presiona ESPACIO para comenzar", BLACK, 230, 300)
    draw_text("Niveles: 1-Fácil, 2-Medio, 3-Difícil", BLACK, 200, 350)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Función para mostrar game over
def show_game_over():
    screen.fill(WHITE)
    if has_images:
        screen.blit(background, (0, 0))
    
    draw_text("¡GAME OVER!", RED, 320, 100)
    draw_text(f"Puntuación final: {score}", BLACK, 300, 200)
    draw_text("Presiona ESPACIO para jugar de nuevo", BLACK, 200, 300)
    draw_text("Presiona ESC para salir", BLACK, 250, 350)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    reset_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Función para reiniciar el juego
def reset_game():
    global player_x, player_y, enemies, score, level, game_over
    player_x = 400
    player_y = 500
    enemies = []
    score = 0
    level = 1
    game_over = False

# Mostrar pantalla de inicio
show_start_screen()

# Bucle principal
running = True
while running:
    if has_images:
        screen.blit(background, (0, 0))
    else:
        screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if game_over:
        show_game_over()
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed
        
    # Ajustar dificultad según nivel
    if score >= 30 and level < 3:
        level = 3
        enemy_speed = 7
    elif score >= 15 and level < 2:
        level = 2
        enemy_speed = 5
        
    # Generar enemigos según nivel
    spawn_rate = 20 - (level * 5)  # Disminuye con cada nivel
    if random.randint(1, spawn_rate) == 1:
        enemies.append([random.randint(0, 800 - enemy_size), 0])
        
    # Mover y dibujar enemigos
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemies.remove(enemy)
            score += 1  # Aumentar puntuación por esquivar
        else:
            draw_enemy(enemy[0], enemy[1])
            
        # Detectar colisiones
        if (player_x < enemy[0] + enemy_size and
            player_x + player_size > enemy[0] and
            player_y < enemy[1] + enemy_size and
            player_y + player_size > enemy[1]):
            game_over = True
            
    draw_player(player_x, player_y)
    
    # Mostrar información en pantalla
    draw_text(f"Puntuación: {score}", BLACK, 10, 10)
    draw_text(f"Nivel: {level}", BLACK, 10, 50)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()