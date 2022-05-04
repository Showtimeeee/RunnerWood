import pygame
from sys import exit
from random import randint, choice


# класс персонаж
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # изображение игрока для анимации
        player_walk_1 = pygame.image.load('image/man2.png').convert_alpha()
        player_walk_2 = pygame.image.load('image/man3.png').convert_alpha()
        player_walk_3 = pygame.image.load('image/man4.png').convert_alpha()
        player_walk_4 = pygame.image.load('image/man5.png').convert_alpha()
        player_walk_5 = pygame.image.load('image/man6.png').convert_alpha()
        player_walk_6 = pygame.image.load('image/man7.png').convert_alpha()

        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6]
        self.player_index = 0
        # Прыжок
        self.player_jump = pygame.image.load('image/manJump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 500))
        self.gravity = 0

        # Звук прыжка
        self.jump_sound = pygame.mixer.Sound('sound/jump-sound-1.mp3')
        # громкость звука
        self.jump_sound.set_volume(0.5)

    # функция прыжка
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = -20
            # sound jump
            self.jump_sound.play()

    # функция гравитации(высота прыжка)
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

    # скорость анимации
    def animation_state(self):
        if self.rect.bottom < 500:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            # увеличиет скорость анимации перса при увелич скорости врагов
            if score > 10:
                self.player_index += 0.2
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# Препятствия(враги)
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('image/flyPng1.png')
            fly_2 = pygame.image.load('image/flyPng2.png')
            fly_3 = pygame.image.load('image/flyPng4.png')
            self.frames = [fly_1, fly_2, fly_3]
            y_pos = 350
        else:
            snail_1 = pygame.image.load('image/mushrums1.png').convert_alpha()
            snail_2 = pygame.image.load('image/mushrums2.png').convert_alpha()
            snail_3 = pygame.image.load('image/mushrums3.png').convert_alpha()
            snail_4 = pygame.image.load('image/mushrums4.png').convert_alpha()
            snail_5 = pygame.image.load('image/mushrums5.png').convert_alpha()
            self.frames = [snail_1, snail_2, snail_3, snail_4, snail_5]
            y_pos = 500

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        # скорость врагов
        self.rect.x -= 6
        if score > 10:
            self.rect.x -= 7
        if score > 20:
            self.rect.x -= 8
        if score > 30:
            self.rect.x -= 10

        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Функция набора очков
def display_score():

    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Очки: {current_time}', False,(64, 64, 64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf, score_rect)
    #print(current_time)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((900, 640))
pygame.display.set_caption('RunnerWood')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
score = 0
# фоновая музыка
bg_music = pygame.mixer.Sound('sound/Sound_turtles.mp3')
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# рисуем квадрат на поле, превращаем в картинку
sky_surface = pygame.image.load('image/2d_platformer_background.jpg').convert()
ground_surface = pygame.image.load('image/ground.bmp').convert()

# Изображение на начадьном экране, типа заставка
player_stand = pygame.image.load('image/2d_platf2.jpg').convert_alpha()
player_stand_rect = player_stand.get_rect(center=(420, 300))

# надпись название игры на заставке экрана
game_name = test_font.render('RunnerWood', False,(64, 64, 64))
game_name_rect = game_name.get_rect(center=(440, 130))
# нажмите пробел надпись на заставке
game_message = test_font.render('Нажмите пробел', False,(64, 64, 64))
game_message_rect = game_message.get_rect(center=(440, 200))

# Таймер
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # рандомно появляются враги
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 500))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Вы набрали: {score}', False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center=(440, 200))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)