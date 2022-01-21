# James Waller
# Orginal by did not have a name attached

import pygame
import random

# ----- CONSTANTS
WIDTH = 2580
HEIGHT = 1350
ENEMY_VEL = 15
LIVES = 1
TITLE = "Dodge the Poros"

# Create a background class
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Bg.jpg")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()

# Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Braum.webp")
        self.image = pygame.transform.scale(self.image, (130, 170))
        self.rect = self.image.get_rect()

        # Initialize velocity
        self.vel_x = 0

        # Spawn player at the bottom of the screen
        self.rect.bottom = HEIGHT - 75
        self.rect.right = WIDTH / 2

    # Update player
    def update(self):
        # Moves left and right
        self.rect.x += self.vel_x

    # Move left function
    def go_left(self):
        self.vel_x = -10
        #self.image = pygame.image.load("Images/Braum.webp")
        #self.image = pygame.transform.scale(self.image, (120, 150))

    # Move right function
    def go_right(self):
        self.vel_x = 10
        #self.image = pygame.image.load("Images/Braum.webp")
        #self.image = pygame.transform.scale(self.image, (54, 75))

    # Stop function
    def stop(self):
        self.vel_x = 0

class Bullet(pygame.sprite.Sprite):

    def __init__(self, coords: tuple):


        super().__init__()
        self.image = pygame.image.load('./Images/Ability.tiff')
        self.image = pygame.transform.scale(self.image, (36, 36))
        # self.image = pygame.Surface((5, 10))
        self.rect = self.image.get_rect()

        # Set the middle of the bullet to be at coords
        self.rect.center = coords

        self.vel_y = 3

    def update(self):
        self.rect.y -= self.vel_y

# Create enemy class, scale enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Poro.jpg")
        self.image = pygame.transform.scale(self.image, (107, 120))
        self.rect = self.image.get_rect()

        # Set enemy velocity
        self.vel_y = ENEMY_VEL

        # Spawn a poro randomly at the top of the screen
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-250, -150)

    def update(self):
        self.rect.y += self.vel_y

def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    game_over = False

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    poro_spawn_time = 1000
    last_poro_spawn = pygame.time.get_ticks()


    # Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_score_x = 10
    text_score_y = 10

    def display_score(x, y):
        score = font.render("Score: " + str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))

    # Lives
    lives_value = 1
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_lives_x = 10
    text_lives_y = 40

    def display_lives(x, y):
        lives = font.render("Lives: " + str(lives_value), True, (0, 0, 0))
        screen.blit(lives, (x, y))

    # Sprite groups
    all_sprite_group = pygame.sprite.Group()
    background_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    # Player and enemy creation
    player = Player()
    all_sprite_group.add(player)

    # Background creation
    bg = Background()
    background_group.add(bg)


    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Move player if user presses down on left/right arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_LEFT:
                    player.go_left()

            # Stop player if arrow key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()

        if pygame.key.get_pressed()[pygame.K_q]:
            bullet = Bullet(player.rect.midtop)

            ability_sprites.add(bullet)
            all_sprites.add(bullet)

        # Restrict player to stay on screen
        if player.rect.right > WIDTH:
            player.rect.right = WIDTH
        if player.rect.left < 0:
            player.rect.left = 0

    # --- Sprites

        all_sprites = pygame.sprite.Group()
        enemy_sprites = pygame.sprite.Group()
        ability_sprites = pygame.sprite.Group()


    # --- Ability

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True




        for ability in ability_sprites:
            enemies_bullet_collided = pygame.sprite.spritecollide(
                ability,
                enemy_sprites,
                True)

            if bullet.rect.y < 0:
                bullet.kill()


        # ----- LOGIC
        all_sprite_group.update()

        if not game_over:
            # poro spawn
            if pygame.time.get_ticks() > last_poro_spawn + poro_spawn_time:
                # Set the new time to this current time
                last_poro_spawn = pygame.time.get_ticks()
                # Spawn poro
                enemy = Enemy()
                all_sprite_group.add(enemy)
                enemy_group.add(enemy)

        # Player collides with a poro
        for enemy in enemy_group:
            # Kill if off screen
            if enemy.rect.bottom > HEIGHT:
                enemy.kill()
                # Add a point to score
                score_value += 1

        # Kill player if hit by poro
        enemies_hit = pygame.sprite.spritecollide(player, enemy_group, False)
        if len(enemies_hit) > 0:
            player.kill()
            lives_value -= 1

        # Game over
        if lives_value <= 0:
            game_over = True
            player.vel_x = 0

            for enemy in enemy_group:
                enemy.kill()

            # Stop background music
            pygame.mixer.music.stop()

        background_group.draw(screen)
        all_sprite_group.draw(screen)
        dirty_rectangles = all_sprite_group.draw(screen)

        display_score(text_score_x, text_score_y)
        display_lives(text_lives_x, text_lives_y)
        pygame.display.update(dirty_rectangles)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()