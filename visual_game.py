import pygame
import random
import sys

WIDTH, HEIGHT = 600, 800
FPS = 60
PLAYER_SPEED = 6
BULLET_SPEED = -10
ENEMY_SPEED_START = 2
ENEMY_SPAWN_RATE = 30  # smaller is faster

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)


def clamp(val, a, b):
    return max(a, min(b, val))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((60, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.surf, BLUE, [(0, 20), (30, 0), (60, 20)])
        self.rect = self.surf.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))
        self.speed = PLAYER_SPEED
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.x = clamp(self.rect.x, 0, WIDTH - self.rect.width)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((4, 10))
        self.surf.fill(YELLOW)
        self.rect = self.surf.get_rect(midbottom=(x, y))
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        size = random.randint(24, 48)
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, RED, (size // 2, size // 2), size // 2)
        self.rect = self.surf.get_rect(midtop=(random.randint(20, WIDTH - 20), -size))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    rect.topleft = (x, y)
    surf.blit(txt, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Defender")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0
    spawn_timer = 0
    enemy_speed = ENEMY_SPEED_START
    spawn_rate = ENEMY_SPAWN_RATE
    level = 1

    running = True
    paused = False
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_SPACE and not paused and not game_over:
                    # fire bullet
                    b = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(b)
                    all_sprites.add(b)
                if event.key == pygame.K_r and game_over:
                    # reset game
                    for s in all_sprites:
                        s.kill()
                    all_sprites.empty()
                    bullets.empty()
                    enemies.empty()
                    player = Player()
                    all_sprites.add(player)
                    score = 0
                    spawn_timer = 0
                    enemy_speed = ENEMY_SPEED_START
                    spawn_rate = ENEMY_SPAWN_RATE
                    level = 1
                    game_over = False

        if paused or game_over:
            # show pause or game over screen
            screen.fill(BLACK)
            if game_over:
                draw_text(screen, "GAME OVER", 64, WIDTH // 2 - 160, HEIGHT // 2 - 80, RED)
                draw_text(screen, f"Score: {score}", 36, WIDTH // 2 - 60, HEIGHT // 2 - 10)
                draw_text(screen, "Press R to restart or ESC to quit", 24, WIDTH // 2 - 150, HEIGHT // 2 + 40)
            else:
                draw_text(screen, "PAUSED", 64, WIDTH // 2 - 100, HEIGHT // 2 - 40, YELLOW)
                draw_text(screen, "Press P to resume", 28, WIDTH // 2 - 100, HEIGHT // 2 + 30)
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        player.update(keys)

        # spawn enemies
        spawn_timer += 1
        if spawn_timer >= spawn_rate:
            spawn_timer = 0
            e = Enemy(enemy_speed)
            enemies.add(e)
            all_sprites.add(e)

        # update sprites
        bullets.update()
        enemies.update()

        # collisions: bullets -> enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for h in hits:
            score += 10

        # collisions: enemies -> player
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            player.lives -= 1
            if player.lives <= 0:
                game_over = True

        # level up
        if score // 100 + 1 > level:
            level += 1
            enemy_speed += 0.8
            spawn_rate = max(8, spawn_rate - 3)

        # draw
        screen.fill((12, 12, 20))
        all_sprites.draw(screen)

        # HUD
        draw_text(screen, f"Score: {score}", 28, 10, 10)
        draw_text(screen, f"Lives: {player.lives}", 28, WIDTH - 140, 10)
        draw_text(screen, f"Level: {level}", 24, WIDTH - 140, 40)
        draw_text(screen, "P: Pause | Space: Shoot | Esc: Quit", 20, 10, HEIGHT - 30, color=(180, 180, 180))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
