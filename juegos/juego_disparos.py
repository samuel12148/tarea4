import pygame
import random
import os
import sys
import math

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Defensa Espacial: Juego de Disparos")
clock = pygame.time.Clock()

# Cargar imágenes (si existen)
try:
    # Intentar cargar imágenes para el jugador, enemigos y balas
    player_img = pygame.image.load("nave.png")
    player_img = pygame.transform.scale(player_img, (50, 50))
    enemy_img = pygame.image.load("alien.png")
    enemy_img = pygame.transform.scale(enemy_img, (40, 40))
    bullet_img = pygame.image.load("bala.png")
    bullet_img = pygame.transform.scale(bullet_img, (5, 15))
    background_img = pygame.image.load("espacio.jpg")
    background_img = pygame.transform.scale(background_img, (800, 600))
    has_images = True
except:
    has_images = False
    print("No se encontraron imágenes. Usando formas geométricas.")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Jugador
player_size = 50
player_x = 400
player_y = 500
player_speed = 5
player_health = 100
max_health = 100

# Balas
bullets = []
bullet_speed = 7
bullet_cooldown = 0
bullet_cooldown_time = 15  # frames entre disparos

# Enemigos
enemies = []
enemy_size = 40
enemy_speed = 2
enemy_spawn_rate = 30

# Explosiones
explosions = []

# Puntuación y nivel
score = 0
level = 1
max_level = 3
game_over = False
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Función para dibujar jugador
def draw_player(x, y):
    if has_images:
        screen.blit(player_img, (x, y))
    else:
        # Dibujar nave espacial
        pygame.draw.polygon(screen, BLUE, [
            (x + player_size//2, y),  # Punta
            (x, y + player_size),     # Esquina inferior izquierda
            (x + player_size, y + player_size)  # Esquina inferior derecha
        ])
        pygame.draw.rect(screen, GREEN, (x + 15, y + 30, 20, 20))  # Cabina

# Función para dibujar enemigos
def draw_enemy(x, y, enemy_type=1):
    if has_images:
        screen.blit(enemy_img, (x, y))
    else:
        color = RED if enemy_type == 1 else PURPLE if enemy_type == 2 else YELLOW
        pygame.draw.circle(screen, color, (x + enemy_size//2, y + enemy_size//2), enemy_size//2)
        # Ojos alienígenas
        pygame.draw.circle(screen, BLACK, (x + 15, y + 15), 5)
        pygame.draw.circle(screen, BLACK, (x + 25, y + 15), 5)

# Función para dibujar balas
def draw_bullet(x, y):
    if has_images:
        screen.blit(bullet_img, (x, y))
    else:
        pygame.draw.rect(screen, YELLOW, (x, y, 5, 15))

# Función para dibujar explosiones
def draw_explosion(x, y, size):
    pygame.draw.circle(screen, YELLOW, (x, y), size)
    pygame.draw.circle(screen, RED, (x, y), size - 5)

# Función para mostrar texto en pantalla
def draw_text(text, color, x, y, font_type=font):
    img = font_type.render(text, True, color)
    screen.blit(img, (x, y))

# Función para mostrar barra de salud
def draw_health_bar():
    pygame.draw.rect(screen, RED, (10, 40, max_health, 20))
    pygame.draw.rect(screen, GREEN, (10, 40, player_health, 20))
    pygame.draw.rect(screen, WHITE, (10, 40, max_health, 20), 2)

# Función para mostrar pantalla de inicio
def show_start_screen():
    if has_images:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(BLACK)
        # Dibujar estrellas de fondo
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    draw_text("DEFENSA ESPACIAL", YELLOW, 250, 100)
    draw_text("Protege la Tierra de la invasión alienígena", WHITE, 180, 150)
    draw_text("Usa las flechas para moverte y ESPACIO para disparar", WHITE, 150, 200)
    draw_text("Destruye naves enemigas y evita que te alcancen", WHITE, 150, 250)
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
        screen.fill(BLACK)
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    draw_text("¡MISIÓN FALLIDA!", RED, 280, 100)
    draw_text(f"Puntuación final: {score}", WHITE, 300, 200)
    draw_text(f"Nivel alcanzado: {level}", WHITE, 300, 250)
    draw_text("La Tierra ha sido invadida...", WHITE, 280, 300)
    draw_text("Presiona ESPACIO para jugar de nuevo", WHITE, 200, 400)
    draw_text("Presiona ESC para salir", WHITE, 280, 450)
    
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
    
    draw_text(f"¡NIVEL {level} COMPLETADO!", YELLOW, 250, 200)
    draw_text(f"Puntos: {score}", WHITE, 350, 250)
    draw_text("Prepárate para el siguiente nivel", WHITE, 250, 300)
    draw_text("Presiona ESPACIO para continuar", WHITE, 230, 400)
    
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
    global player_x, player_y, bullets, enemies, explosions
    global score, level, game_over, player_health, bullet_cooldown
    player_x = 400
    player_y = 500
    bullets = []
    enemies = []
    explosions = []
    score = 0
    level = 1
    game_over = False
    player_health = max_health
    bullet_cooldown = 0

# Función para avanzar de nivel
def next_level():
    global level, enemies, enemy_speed, enemy_spawn_rate
    level += 1
    enemies = []
    
    # Aumentar dificultad según el nivel
    if level == 2:
        enemy_speed = 3
        enemy_spawn_rate = 25
    elif level == 3:
        enemy_speed = 4
        enemy_spawn_rate = 20

# Mostrar pantalla de inicio
show_start_screen()

# Bucle principal
running = True
while running:
    if has_images:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(BLACK)
        # Dibujar estrellas de fondo
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(screen, WHITE, (x, y), 1)
    
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
    
    # Disparar balas (con cooldown)
    if bullet_cooldown > 0:
        bullet_cooldown -= 1
        
    if keys[pygame.K_SPACE] and bullet_cooldown == 0:
        bullets.append([player_x + player_size//2 - 2, player_y])
        bullet_cooldown = bullet_cooldown_time
        
    # Generar enemigos según el nivel
    if random.randint(1, enemy_spawn_rate) == 1:
        enemy_type = 1
        if level >= 2 and random.random() < 0.3:  # 30% de enemigos tipo 2 en nivel 2+
            enemy_type = 2
        if level >= 3 and random.random() < 0.2:  # 20% de enemigos tipo 3 en nivel 3
            enemy_type = 3
            
        enemies.append([random.randint(0, 800 - enemy_size), 0, enemy_type])
        
    # Mover enemigos
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemies.remove(enemy)
            player_health -= 10  # Daño por dejar pasar enemigos
            if player_health <= 0:
                game_over = True
        else:
            draw_enemy(enemy[0], enemy[1], enemy[2])
            
    # Mover balas
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            draw_bullet(bullet[0], bullet[1])
            
    # Mover y dibujar explosiones
    for explosion in explosions[:]:
        explosion[2] += 1  # Aumentar tamaño
        if explosion[2] > 30:  # Tiempo máximo de explosión
            explosions.remove(explosion)
        else:
            draw_explosion(explosion[0], explosion[1], explosion[2])
            
    # Detectar colisiones bala-enemigo
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet[0] < enemy[0] + enemy_size and
                bullet[0] + 5 > enemy[0] and
                bullet[1] < enemy[1] + enemy_size and
                bullet[1] + 10 > enemy[1]):
                
                # Crear explosión
                explosions.append([enemy[0] + enemy_size//2, enemy[1] + enemy_size//2, 5])
                
                # Eliminar bala y enemigo
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    
                # Añadir puntos según tipo de enemigo
                points = 10 * enemy[2]  # Más puntos por enemigos más difíciles
                score += points
                
                break
    
    # Dibujar jugador
    draw_player(player_x, player_y)
    
    # Mostrar información en pantalla
    draw_text(f"Puntos: {score}", WHITE, 10, 10)
    draw_text(f"Nivel: {level}/{max_level}", WHITE, 700, 10)
    draw_text("Salud:", WHITE, 10, 15)
    draw_health_bar()
    
    # Comprobar si se completa el nivel
    if score >= level * 150:  # 150 puntos por nivel
        if level < max_level:
            show_level_complete()
            next_level()
        else:
            draw_text("¡VICTORIA! La Tierra está a salvo", GREEN, 200, 570)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()