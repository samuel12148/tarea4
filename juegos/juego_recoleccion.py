import pygame
import random
import os
import sys

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tesoros Perdidos: Juego de Recolección")
clock = pygame.time.Clock()

# Cargar imágenes (si existen)
try:
    # Intentar cargar imágenes para el jugador y objetos
    player_img = pygame.image.load("explorador.png")
    player_img = pygame.transform.scale(player_img, (40, 40))
    item_img = pygame.image.load("tesoro.png")
    item_img = pygame.transform.scale(item_img, (20, 20))
    background_img = pygame.image.load("jungla.jpg")
    background_img = pygame.transform.scale(background_img, (800, 600))
    has_images = True
except:
    has_images = False
    print("No se encontraron imágenes. Usando formas geométricas.")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Jugador
player_size = 40
player_x = 400
player_y = 300
player_speed = 5

# Objetos para recolectar
items = []
item_size = 20
item_spawn_rate = 30  # Frecuencia de aparición de objetos

# Obstáculos (en niveles más avanzados)
obstacles = []
obstacle_size = 30

# Puntuación y nivel
score = 0
level = 1
max_level = 3
game_over = False
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Tiempo de juego (para modo con tiempo)
game_time = 0
time_limit = 120  # 2 minutos por nivel

# Función para dibujar jugador
def draw_player(x, y):
    if has_images:
        screen.blit(player_img, (x, y))
    else:
        pygame.draw.circle(screen, GREEN, (x + player_size//2, y + player_size//2), player_size//2)
        # Detalles del explorador
        pygame.draw.circle(screen, BLUE, (x + 15, y + 15), 5)  # Ojo
        pygame.draw.circle(screen, BLUE, (x + 25, y + 15), 5)  # Ojo

# Función para dibujar objetos
def draw_item(x, y):
    if has_images:
        screen.blit(item_img, (x, y))
    else:
        pygame.draw.rect(screen, YELLOW, (x, y, item_size, item_size))
        # Detalles del tesoro
        pygame.draw.rect(screen, BROWN, (x + 5, y + 5, 10, 10))

# Función para dibujar obstáculos
def draw_obstacle(x, y):
    pygame.draw.rect(screen, BROWN, (x, y, obstacle_size, obstacle_size))
    pygame.draw.line(screen, BLACK, (x, y), (x + obstacle_size, y + obstacle_size), 2)
    pygame.draw.line(screen, BLACK, (x + obstacle_size, y), (x, y + obstacle_size), 2)

# Función para mostrar texto en pantalla
def draw_text(text, color, x, y, font_type=font):
    img = font_type.render(text, True, color)
    screen.blit(img, (x, y))

# Función para mostrar pantalla de inicio
def show_start_screen():
    if has_images:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((0, 100, 0))  # Fondo verde oscuro
    
    draw_text("TESOROS PERDIDOS", GOLD, 250, 100)
    draw_text("Recolecta todos los tesoros que puedas", WHITE, 200, 150)
    draw_text("Usa las flechas para mover al explorador", WHITE, 200, 200)
    draw_text("Evita los obstáculos en niveles avanzados", WHITE, 190, 250)
    draw_text("Presiona ESPACIO para comenzar", WHITE, 230, 350)
    draw_text(f"Niveles: 1-Fácil, 2-Medio, 3-Difícil", WHITE, 220, 400)
    
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
    if has_images:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((0, 100, 0))
    
    draw_text("¡JUEGO TERMINADO!", GOLD, 280, 100)
    draw_text(f"Puntuación final: {score}", WHITE, 300, 200)
    draw_text(f"Nivel alcanzado: {level}", WHITE, 300, 250)
    draw_text("Presiona ESPACIO para jugar de nuevo", WHITE, 200, 350)
    draw_text("Presiona ESC para salir", WHITE, 280, 400)
    
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

# Función para mostrar nivel completado
def show_level_complete():
    overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text(f"¡NIVEL {level} COMPLETADO!", GOLD, 250, 200)
    draw_text(f"Puntos: {score}", WHITE, 350, 250)
    draw_text("Presiona ESPACIO para continuar", WHITE, 230, 350)
    
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

# Función para reiniciar el juego
def reset_game():
    global player_x, player_y, items, obstacles, score, level, game_over, game_time
    player_x = 400
    player_y = 300
    items = []
    obstacles = []
    score = 0
    level = 1
    game_over = False
    game_time = 0

# Función para avanzar de nivel
def next_level():
    global level, items, obstacles, game_time
    level += 1
    items = []
    obstacles = []
    game_time = 0
    
    # Configurar obstáculos según el nivel
    if level >= 2:
        for _ in range(level * 2):
            obstacles.append([random.randint(0, 800 - obstacle_size), 
                              random.randint(0, 600 - obstacle_size)])

# Mostrar pantalla de inicio
show_start_screen()

# Bucle principal
running = True
while running:
    if has_images:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill((0, 100, 0))  # Fondo verde oscuro (jungla)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if game_over:
        show_game_over()
        continue
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < 600 - player_size:
        player_y += player_speed
        
    # Ajustar dificultad según nivel
    if level == 1:
        item_spawn_rate = 25
        player_speed = 5
    elif level == 2:
        item_spawn_rate = 20
        player_speed = 4
    elif level == 3:
        item_spawn_rate = 15
        player_speed = 3
        
    # Generar objetos
    if random.randint(1, item_spawn_rate) == 1:
        items.append([random.randint(0, 800 - item_size), 
                      random.randint(0, 600 - item_size)])
        
    # Recolectar objetos
    for item in items[:]:
        if (player_x < item[0] + item_size and
            player_x + player_size > item[0] and
            player_y < item[1] + item_size and
            player_y + player_size > item[1]):
            items.remove(item)
            score += 10 * level  # Más puntos en niveles superiores
            
    # Comprobar colisión con obstáculos (niveles 2 y 3)
    if level >= 2:
        for obstacle in obstacles:
            if (player_x < obstacle[0] + obstacle_size and
                player_x + player_size > obstacle[0] and
                player_y < obstacle[1] + obstacle_size and
                player_y + player_size > obstacle[1]):
                game_over = True
    
    # Dibujar obstáculos
    for obstacle in obstacles:
        draw_obstacle(obstacle[0], obstacle[1])
        
    # Dibujar objetos
    for item in items:
        draw_item(item[0], item[1])
        
    draw_player(player_x, player_y)
    
    # Mostrar información en pantalla
    draw_text(f"Puntos: {score}", WHITE, 10, 10)
    draw_text(f"Nivel: {level}/{max_level}", WHITE, 10, 50)
    
    # Comprobar si se completa el nivel
    if score >= level * 100:  # 100 puntos por nivel
        if level < max_level:
            show_level_complete()
            next_level()
        else:
            draw_text("¡FELICIDADES! Has completado todos los niveles", GOLD, 150, 550)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()