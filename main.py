import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Inicializa o mixer do Pygame
pygame.mixer.init()

# Configura a tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dragon Fighters')  # Nome do jogo na barra de título

# Carregar música de fundo
pygame.mixer.music.load('background_music.mp3')  # Substitua pelo nome do seu arquivo de música
pygame.mixer.music.set_volume(0.5)  # Ajusta o volume (0.0 a 1.0)
pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# FPS
clock = pygame.time.Clock()
fps = 60

# Carregar imagens dos personagens
player1_idle = pygame.image.load('player1_idle.png')  # Imagem parada do jogador vermelho
player1_run = pygame.image.load('player1_run.png')  # Imagem andando do jogador vermelho
player1_attack1 = pygame.image.load('player1_attack1.png')  # Imagem de ataque 1 do jogador vermelho
player1_attack2 = pygame.image.load('player1_attack2.png')  # Imagem de ataque 2 do jogador vermelho
player2_idle = pygame.image.load('player2_idle.png')  # Imagem parada do jogador azul
player2_run = pygame.image.load('player2_run.png')  # Imagem andando do jogador azul
player2_attack1 = pygame.image.load('player2_attack1.png')  # Imagem de ataque 1 do jogador azul
player2_attack2 = pygame.image.load('player2_attack2.png')  # Imagem de ataque 2 do jogador azul

# Carregar imagem de fundo
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))  # Redimensiona a imagem para a tela

# Configuração dos personagens
player1 = pygame.Rect(50, 400, 50, 100)  # Jogador vermelho
player2 = pygame.Rect(700, 400, 50, 100)  # Jogador azul

# Configurações do salto
gravity = 0.5
jump_speed = -10
player1_velocity_y = 0
player2_velocity_y = 0
player1_jumping = False
player2_jumping = False

# Vida dos personagens
player1_health = 100
player2_health = 100

# Nicknames
player1_nickname = ""
player2_nickname = ""

# Estado do ataque
player1_attacking = False
player2_attacking = False
player1_attack_frame = 0
player2_attack_frame = 0

# Timers de ataque
player1_attack_start_time = 0
player2_attack_start_time = 0
player1_attack_cooldown = 200  # 0.2 segundos
player2_attack_cooldown = 200  # 0.2 segundos
player1_attack_interval = 200  # 0.2 segundos
player2_attack_interval = 200  # 0.2 segundos


# Função para desenhar o personagem
def draw_character(rect, image, flipped=False):
    if flipped:
        image = pygame.transform.flip(image, True, False)
    screen.blit(image, rect.topleft)


# Função para desenhar a barra de vida
def draw_health_bar(health, x, y):
    bar_width = 150
    bar_height = 20
    fill = (health / 100) * bar_width
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)
    pygame.draw.rect(screen, GREEN, (x, y, fill, bar_height))


# Função para desenhar texto
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


# Função para desenhar o botão
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, width, height)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        if mouse_click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, rect)

    draw_text(text, 30, BLACK, x + width / 2, y + height / 2)
    return False


# Função para inserir nickname
def input_nickname(player):
    input_box = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 25, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    font = pygame.font.Font(None, 32)
    text = ''
    active = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(BLACK)
        draw_text("Escolha um nome para o jogador 1" if player == 1 else "Escolha um nome para o jogador 2", 30, WHITE,
                  screen_width / 2, screen_height / 2 - 75)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text


# Tela de início
def start_screen():
    while True:
        screen.blit(background, (0, 0))  # Desenha o fundo
        draw_text("Dragon Fighters", 55, WHITE, screen_width / 2, screen_height / 3)  # Nome do jogo atualizado
        if draw_button("Iniciar", screen_width / 2 - 100, screen_height / 2 - 25, 200, 50, GRAY, WHITE):
            return

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Tela de nicknames
def nickname_screen():
    global player1_nickname, player2_nickname

    player1_nickname = input_nickname(1)
    player2_nickname = input_nickname(2)


# Tela final
def end_screen(winner_nickname):
    while True:
        screen.blit(background, (0, 0))  # Desenha o fundo
        draw_text(f"{winner_nickname} venceu!", 55, WHITE, screen_width / 2, screen_height / 3)
        if draw_button("Jogar Novamente", screen_width / 2 - 150, screen_height / 2 + 40, 300, 50, GRAY, WHITE):
            return

        if draw_button("Sair", screen_width / 2 - 75, screen_height / 2 + 100, 150, 50, GRAY, WHITE):
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Função para verificar se há colisão
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


# Função para verificar se um ataque está atingindo o oponente
def check_attack_collision(player_rect, attack_rect):
    return attack_rect.colliderect(player_rect)


# Loop principal do jogo
def game_loop():
    global player1_health, player2_health, player1, player2
    global player1_image, player2_image
    global player1_attacking, player2_attacking
    global player1_attack_start_time, player2_attack_start_time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Movimentação do player1
        if keys[pygame.K_a]:
            player1.x -= 5
            player1_facing_right = False
            player1_image = player1_run
        elif keys[pygame.K_d]:
            player1.x += 5
            player1_facing_right = True
            player1_image = player1_run
        else:
            if not player1_attacking:
                player1_image = player1_idle

        # Movimentação do player2
        if keys[pygame.K_LEFT]:
            player2.x -= 5
            player2_facing_right = False
            player2_image = player2_run
        elif keys[pygame.K_RIGHT]:
            player2.x += 5
            player2_facing_right = True
            player2_image = player2_run
        else:
            if not player2_attacking:
                player2_image = player2_idle

        # Controle do salto do player1
        if keys[pygame.K_w] and not player1_jumping:
            player1_velocity_y = jump_speed
            player1_jumping = True
        if player1_jumping:
            player1.y += player1_velocity_y
            player1_velocity_y += gravity
            if player1.y >= 400:
                player1.y = 400
                player1_jumping = False
                player1_velocity_y = 0

        # Controle do salto do player2
        if keys[pygame.K_UP] and not player2_jumping:
            player2_velocity_y = jump_speed
            player2_jumping = True
        if player2_jumping:
            player2.y += player2_velocity_y
            player2_velocity_y += gravity
            if player2.y >= 400:
                player2.y = 400
                player2_jumping = False
                player2_velocity_y = 0

        # Impede que os jogadores saiam da tela
        player1.x = max(0, min(screen_width - player1.width, player1.x))
        player1.y = max(0, min(screen_height - player1.height, player1.y))
        player2.x = max(0, min(screen_width - player2.width, player2.x))
        player2.y = max(0, min(screen_height - player2.height, player2.y))

        # Área de ataque do player1
        player1_attack_area = pygame.Rect(player1.x + 50, player1.y, 50, 100) if player1_facing_right else pygame.Rect(
            player1.x - 50, player1.y, 50, 100)

        # Área de ataque do player2
        player2_attack_area = pygame.Rect(player2.x + 50, player2.y, 50, 100) if player2_facing_right else pygame.Rect(
            player2.x - 50, player2.y, 50, 100)

        # Ataques
        if keys[pygame.K_SPACE]:  # Player 1 ataca
            if not player1_attacking:
                player1_attacking = True
                player1_attack_start_time = current_time
            elif current_time - player1_attack_start_time > player1_attack_cooldown:
                # Alterna entre as imagens de ataque
                if (current_time - player1_attack_start_time) % player1_attack_interval < player1_attack_interval / 2:
                    player1_image = player1_attack1
                else:
                    player1_image = player1_attack2

                # Verifica se o ataque do player1 atinge o player2
                if check_attack_collision(player2, player1_attack_area):
                    player2_health -= 1  # Reduz a vida do player2

        else:
            player1_attacking = False
            if not (keys[pygame.K_a] or keys[pygame.K_d]):  # Se o player1 não está se movendo
                player1_image = player1_idle

        if keys[pygame.K_RCTRL]:  # Player 2 ataca
            if not player2_attacking:
                player2_attacking = True
                player2_attack_start_time = current_time
            elif current_time - player2_attack_start_time > player2_attack_cooldown:
                # Alterna entre as imagens de ataque
                if (current_time - player2_attack_start_time) % player2_attack_interval < player2_attack_interval / 2:
                    player2_image = player2_attack1
                else:
                    player2_image = player2_attack2

                # Verifica se o ataque do player2 atinge o player1
                if check_attack_collision(player1, player2_attack_area):
                    player1_health -= 1  # Reduz a vida do player1

        else:
            player2_attacking = False
            if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):  # Se o player2 não está se movendo
                player2_image = player2_idle

        # Verifica se algum jogador perdeu
        if player1_health <= 0 or player2_health <= 0:
            if player1_health <= 0:
                winner_nickname = player2_nickname
            if player2_health <= 0:
                winner_nickname = player1_nickname
            end_screen(winner_nickname)
            break

        # Atualiza a tela
        screen.blit(background, (0, 0))  # Desenha o fundo

        # Desenha os personagens
        draw_character(player1, player1_image, not player1_facing_right)
        draw_character(player2, player2_image, not player2_facing_right)

        # Desenha as barras de vida com cabeçalhos
        draw_text(f"{player1_nickname} - {player1_health}", 30, WHITE, 125, 25)
        draw_health_bar(player1_health, 50, 50)  # Barra de vida do player1 (vermelho) no canto superior esquerdo

        draw_text(f"{player2_nickname} - {player2_health}", 30, WHITE, screen_width - 125, 25)
        draw_health_bar(player2_health, screen_width - 200,
                        50)  # Barra de vida do player2 (azul) no canto superior direito

        pygame.display.flip()

        # Limita os FPS
        clock.tick(fps)


# Tela de início
start_screen()

# Tela de nicknames
nickname_screen()

# Loop principal do jogo
while True:
    player1_health = 100
    player2_health = 100
    player1 = pygame.Rect(50, 400, 50, 100)  # Jogador vermelho
    player2 = pygame.Rect(700, 400, 50, 100)  # Jogador azul
    player1_image = player1_idle
    player2_image = player2_idle
    player1_velocity_y = 0
    player2_velocity_y = 0
    player1_jumping = False
    player2_jumping = False
    player1_attacking = False
    player2_attacking = False
    player1_attack_start_time = 0
    player2_attack_start_time = 0
    game_loop()
