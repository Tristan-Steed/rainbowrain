import pygame
import random
import sys
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Get the screen info for fullscreen
screen_info = pygame.display.Info()
WINDOW_WIDTH = screen_info.current_w
WINDOW_HEIGHT = screen_info.current_h

# Constants
FPS = 60
RAINDROP_SPEED = 4
PLAYER_SPEED = 12
RAINDROP_SIZE = 15
PLAYER_WIDTH = 120
PLAYER_HEIGHT = 40  # Increased height for parabola
BOSS_SIZE = 80
BALL_DELAY = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Red Rain Defender')
clock = pygame.time.Clock()

# Game state
class GameState:
    def __init__(self):
        self.score = 0
        self.miss_count = 0
        self.boss_health = 100
        self.is_active = False
        self.player_x = WINDOW_WIDTH // 2
        self.balls = []
        self.ball_delay = 0
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.is_fullscreen = True
        self.victory = False

    def reset(self):
        self.score = 0
        self.miss_count = 0
        self.boss_health = 100
        self.is_active = True
        self.balls = []
        self.ball_delay = BALL_DELAY
        self.victory = False

class Ball:
    def __init__(self, boss_x, boss_y):
        self.x = boss_x
        self.y = boss_y
        self.color = RED
        self.is_caught = False
        self.speed_y = RAINDROP_SPEED
        self.speed_x = 0
        self.rect = pygame.Rect(self.x, self.y, RAINDROP_SIZE, RAINDROP_SIZE)
        self.is_active = True

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        # Bounce off walls
        if self.x <= 0 or self.x >= WINDOW_WIDTH:
            self.speed_x = -self.speed_x
            self.x = max(0, min(self.x, WINDOW_WIDTH))

    def reflect(self, paddle_x, paddle_width):
        # Calculate position relative to paddle center
        relative_x = (self.x - paddle_x) / (paddle_width / 2)
        
        # Use a concave parabolic function to determine reflection angle
        # y = -ax^2 + bx + c, where a determines the curve's steepness
        a = 0.5  # Controls the curve of the parabola
        normal_angle = math.atan(-2 * a * relative_x)  # Derivative of concave parabola gives normal
        
        # Calculate reflection angle based on normal
        incident_angle = math.atan2(self.speed_y, self.speed_x)
        reflection_angle = 2 * normal_angle - incident_angle
        
        # Set new velocity with increased speed
        speed = RAINDROP_SPEED * 1.5
        self.speed_x = speed * math.cos(reflection_angle)
        self.speed_y = -speed * math.sin(reflection_angle)
        
        self.is_caught = True
        self.color = BLUE

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), RAINDROP_SIZE // 2)

def draw_parabolic_paddle(surface, x, width, height, color):
    # Draw a concave parabolic paddle
    points = []
    center_x = x + width // 2
    a = 0.5  # Same as in Ball.reflect()
    
    for i in range(width + 1):
        relative_x = (i - width/2) / (width/2)
        y = -a * relative_x * relative_x * height  # Negative sign makes it concave
        points.append((x + i, WINDOW_HEIGHT - 100 + y))
    
    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, 3)

def toggle_fullscreen(game_state):
    global screen, WINDOW_WIDTH, WINDOW_HEIGHT
    game_state.is_fullscreen = not game_state.is_fullscreen
    if game_state.is_fullscreen:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800, 600))

def spawn_ball(boss_rect):
    return Ball(boss_rect.centerx, boss_rect.bottom)

def main():
    global screen
    game_state = GameState()
    player_rect = pygame.Rect(WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2, 
                            WINDOW_HEIGHT - 100, 
                            PLAYER_WIDTH, 
                            PLAYER_HEIGHT)
    boss_rect = pygame.Rect(WINDOW_WIDTH // 2 - BOSS_SIZE // 2, 
                          50, 
                          BOSS_SIZE, 
                          BOSS_SIZE)
    
    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and not game_state.is_active:
                    game_state.reset()
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_f:  # Toggle fullscreen
                    toggle_fullscreen(game_state)

        # Get keyboard input
        keys = pygame.key.get_pressed()
        if game_state.is_active:
            if keys[K_LEFT] and player_rect.left > 0:
                player_rect.x -= PLAYER_SPEED
            if keys[K_RIGHT] and player_rect.right < WINDOW_WIDTH:
                player_rect.x += PLAYER_SPEED

            # Move boss left and right slowly
            boss_rect.x += math.sin(pygame.time.get_ticks() / 1000) * 2
            boss_rect.x = max(0, min(boss_rect.x, WINDOW_WIDTH - BOSS_SIZE))

        # Game logic
        if game_state.is_active:
            # Handle ball spawning
            if game_state.ball_delay <= 0:
                game_state.balls.append(spawn_ball(boss_rect))
                game_state.ball_delay = BALL_DELAY
            else:
                game_state.ball_delay -= 1

            # Update and check all balls
            for ball in game_state.balls[:]:
                if not ball.is_active:
                    game_state.balls.remove(ball)
                    continue

                ball.update()

                # Check if caught by player
                if not ball.is_caught:
                    if (player_rect.left <= ball.x <= player_rect.right and
                        player_rect.top - RAINDROP_SIZE <= ball.y <= player_rect.bottom):
                        ball.reflect(player_rect.x, player_rect.width)
                        game_state.score += 1

                # Check if hit boss
                if ball.is_caught and ball.color == BLUE:
                    if (boss_rect.left <= ball.x <= boss_rect.right and
                        boss_rect.top <= ball.y <= boss_rect.bottom):
                        ball.is_active = False
                        game_state.boss_health -= 1
                        if game_state.boss_health <= 0:
                            game_state.is_active = False
                            game_state.victory = True

                # Check if missed
                if not ball.is_caught and ball.y > WINDOW_HEIGHT:
                    ball.is_active = False
                    game_state.miss_count += 1
                    if game_state.miss_count >= 4:
                        game_state.is_active = False

        # Drawing
        screen.fill(BLACK)

        # Draw parabolic paddle
        draw_parabolic_paddle(screen, player_rect.x, player_rect.width, player_rect.height, BLUE)

        # Draw boss
        pygame.draw.rect(screen, RED, boss_rect)

        # Draw all active balls
        for ball in game_state.balls:
            if ball.is_active:
                ball.draw(screen)

        # Draw score and health
        score_text = game_state.font.render(f'Score: {game_state.score}', True, WHITE)
        health_text = game_state.font.render(f'Boss Health: {game_state.boss_health}%', True, RED)
        lives_text = game_state.font.render(f'Lives: {"*" * (4 - game_state.miss_count)}', True, YELLOW)

        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (WINDOW_WIDTH - 200, 10))
        screen.blit(lives_text, (WINDOW_WIDTH // 2 - 50, 10))

        # Draw game over, victory, or start screen
        if not game_state.is_active:
            if game_state.victory:
                victory_text = game_state.big_font.render('VICTORY!', True, BLUE)
                final_score_text = game_state.font.render(f'Final Score: {game_state.score}', True, WHITE)
                screen.blit(victory_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
                screen.blit(final_score_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20))
            elif game_state.miss_count >= 4:
                game_over_text = game_state.big_font.render('GAME OVER', True, RED)
                final_score_text = game_state.font.render(f'Final Score: {game_state.score}', True, WHITE)
                screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50))
                screen.blit(final_score_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20))
            else:
                start_text = game_state.big_font.render('Press SPACE to Start', True, WHITE)
                screen.blit(start_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))

        # Draw controls info
        controls_text = game_state.font.render('F: Toggle Fullscreen | ESC: Quit', True, WHITE)
        screen.blit(controls_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

