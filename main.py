import pygame
import os
import time
import random

pygame.font.init()

# SET GAME DISPLAY
WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE INVADERS")

# LOAD SPACE SHIPS
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# LOAD BULLETS
RED_BULLET = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_BULLET = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_BULLET = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_BULLET = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# LOAD BACKGROUND IMAGE
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Bullets:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw_bullet(self, wind):
        wind.blit(self.image, (self.x, self.y))

    def bullet_movement(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.space_ship_image = None
        self.bullet_image = None
        self.bullets = []
        self.bullet_shots_counter = 0

    def draw_ship(self, wind):
        wind.blit(self.space_ship_image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw_bullet(wind)

    def move_bullets(self, velocity, obj):
        self.space_between_shots()
        for bullet in self.bullets:
            bullet.bullet_movement(velocity)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def space_between_shots(self):
        if self.bullet_shots_counter >= self.COOLDOWN:
            self.bullet_shots_counter = 0
        elif self.bullet_shots_counter > 0:
            self.bullet_shots_counter += 1

    def shoot_bullet(self):
        if self.bullet_shots_counter == 0:
            bullet = Bullets(self.x, self.y, self.bullet_image)
            self.bullets.append(bullet)
            self.bullet_shots_counter = 1

    def ship_width(self):
        return self.space_ship_image.get_width()

    def ship_height(self):
        return self.space_ship_image.get_height()


# CREATE PLAYER SHIP

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.space_ship_image = YELLOW_SPACE_SHIP
        self.bullet_image = YELLOW_BULLET
        self.mask = pygame.mask.from_surface(self.space_ship_image)
        self.maximum_player_health = health

    def move_bullets(self, velocity, objs):
        self.space_between_shots()
        for bullet in self.bullets:
            bullet.bullet_movement(velocity)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def draw_ship(self, wind):
        super().draw_ship(wind)
        self.player_healthbar(wind)

    def player_healthbar(self, wind):
        pygame.draw.rect(wind, (255, 0, 0), (self.x, self.y + self.space_ship_image.get_height() + 10, self.space_ship_image.get_width(), 10))
        pygame.draw.rect(wind, (0, 255, 0), (self.x, self.y + self.space_ship_image.get_height() + 10, self.space_ship_image.get_width() * (self.health/self.maximum_player_health), 10))


# CREATE ENEMY SHIPS

class Enemies(Ship):
    ENEMY_COLOURS = {
        "red": (RED_SPACE_SHIP, RED_BULLET),
        "green": (GREEN_SPACE_SHIP, GREEN_BULLET),
        "blue": (BLUE_SPACE_SHIP, BLUE_BULLET)
    }

    def __init__(self, x, y, colour, health=100):
        super().__init__(x, y, health)
        self.space_ship_image, self.bullet_image = self.ENEMY_COLOURS[colour]
        self.mask = pygame.mask.from_surface(self.space_ship_image)

    def enemy_movement(self, velocity):
        self.y += velocity

    def shoot_bullet(self):
        if self.bullet_shots_counter == 0:
            bullet = Bullets(self.x-20, self.y, self.bullet_image)
            self.bullets.append(bullet)
            self.bullet_shots_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 80
    level = 0
    lives = 4
    font_one = pygame.font.SysFont("comicsans", 40)
    font_two = pygame.font.SysFont("comicsans", 65)
    enemies = []
    level_wavelength = 5
    bullet_velocity = 5
    enemy_velocity = 1
    player_velocity = 5
    player_ship = Player(300, 500)
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    # SET BACKGROUND DISPLAY
    def redraw_window():
        WINDOW.blit(BACKGROUND, (0, 0))

        # SET BACKGROUND TEXT
        lives_label = font_one.render(f"Lives: {lives}", 1, (255, 255, 255))  # Lives Font
        level_label = font_one.render(f"Level: {level}", 1, (255, 255, 255))  # Level Font

        WINDOW.blit(lives_label, (10, 10))  # Draw Lives font on background
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))  # Draw Level font on background

        for enemy in enemies:
            enemy.draw_ship(WINDOW)  # DRAW ENEMY SHIPS

        player_ship.draw_ship(WINDOW)  # DRAW PLAYER SHIP

        if lost:
            lost_label = font_two.render("You Lost!!", 1, (255, 255, 255))  # Lost font
            WINDOW.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 300))  # Draw Lost font on background

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player_ship.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 2.25:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            level_wavelength += 5
            for i in range(level_wavelength):
                enemy = Enemies(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100),
                                random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # SET PLAYER MOVEMENTS
        keyboard_keys = pygame.key.get_pressed()
        if keyboard_keys[pygame.K_LEFT] and player_ship.x - player_velocity > 0:  # movement to the left
            player_ship.x -= player_velocity
        if keyboard_keys[
            pygame.K_RIGHT] and player_ship.x + player_velocity + player_ship.ship_width() < WIDTH:  # movement to the right
            player_ship.x += player_velocity
        if keyboard_keys[pygame.K_UP] and player_ship.y - player_velocity > 0:  # movement upward
            player_ship.y -= player_velocity
        if keyboard_keys[
            pygame.K_DOWN] and player_ship.y + player_velocity + player_ship.ship_height() + 15 < HEIGHT:  # movement downward
            player_ship.y += player_velocity
        if keyboard_keys[pygame.K_SPACE]:  # Player shooting
            player_ship.shoot_bullet()

        # SET ENEMY MOVEMENTS
        for enemy in enemies[:]:
            enemy.enemy_movement(enemy_velocity)
            enemy.move_bullets(bullet_velocity, player_ship)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot_bullet()  # Enemies shooting

            if collide(enemy, player_ship):
                player_ship.health -= 10
                enemies.remove(enemy)  # Player and enemy collision
            elif enemy.y + enemy.ship_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player_ship.move_bullets(-bullet_velocity, enemies)  # Movement of Player's bullets

def main_menu():
    font_three = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0, 0))
        title_label = font_three.render("Click the Mouse Button to Begin...", 1, (255, 255, 255))
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
