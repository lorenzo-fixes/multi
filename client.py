import pygame
import socket
import pickle
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
CHARACTER_SIZE = 50
CHARACTER_SPEED = 5

# Connect to the server
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Multiplayer Game")

# Create local player
local_player = Player(RED, SCREEN_WIDTH // 2 - CHARACTER_SIZE // 2, SCREEN_HEIGHT - CHARACTER_SIZE - 50)

# Group for all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(local_player)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                local_player.speed_x = -CHARACTER_SPEED
            elif event.key == pygame.K_RIGHT:
                local_player.speed_x = CHARACTER_SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                local_player.speed_x = 0

    # Send player input to the server
    player_input = {"x": local_player.rect.x, "speed_x": local_player.speed_x}
    client_socket.send(pickle.dumps(player_input))

    # Receive game state updates from the server
    data = client_socket.recv(1024)
    game_state = pickle.loads(data)
    # Update local game state
    local_player.rect.x = game_state["player_x"]

    # Clear the screen
    screen.fill(BLUE)

    # Update and draw all sprites
    all_sprites.update()
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Close the socket and quit Pygame
client_socket.close()
pygame.quit()
sys.exit()
