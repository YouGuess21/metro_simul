import pygame
import sys
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 1000
FPS = 60
TRAIN_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)
TRAIN_SIZE = 10
cell_size = 5
cell_number = 200

# Setup screen
screen = pygame.display.set_mode((cell_size * cell_number * 1.8, cell_number * cell_size ))
pygame.display.set_caption("Train Tracks")

# Tracks coordinates
# tracks = [
    # [(100, 100), (450, 100), (700, 100), (700, 200), (100, 200), (100, 100)],
    # [(100, 300), (700, 300), (700, 400), (100, 400), (100, 300)],
    # [(100, 500), (700, 500), (700, 600), (100, 600), (100, 500)],
# ]

class TRACK:
    def __init__(self, train_number):
        self.route = []
        if train_number == 0:
            self.color = (255, 165, 0)
            for i in range(30, 171):
                self.route.append(Vector2(30,i))
            for i in range(30, 331):
                self.route.append(Vector2(i, 170))
            for i in range(170, 29, -1):
                self.route.append(Vector2(330,i))
            for i in range(330, 30, -1):
                self.route.append(Vector2(i, 30))
        elif train_number == 1:
            self.color = (160, 32, 240)
            for i in range (30, 151):
                self.route.append(Vector2(1,i))
            for i in range (1, 131):
                self.route.append(Vector2(i, 150))
            for i in range (150, 199):
                self.route.append(Vector2(130, i))
            for i in range (130, 216):
                self.route.append(Vector2(i, 198))
            for i in range (198, 99, -1):
                self.route.append(Vector2(215, i))
            for i in range (215, 360):
                self.route.append(Vector2(i, 100))
            for i in range (100, 89, -1):
                self.route.append(Vector2(359,i))
            for i in range (359, 204, -1):
                self.route.append(Vector2(i, 90))
            for i in range (90, 189):
                self.route.append(Vector2(205,i))
            for i in range (205, 139, -1):
                self.route.append(Vector2(i, 188))
            for i in range (188, 139, -1):
                self.route.append(Vector2(140, i))
            for i in range (140, 9, -1):
                self.route.append(Vector2(i, 140))
            for i in range (140, 29, -1):
                self.route.append(Vector2(10, i))
            for i in range (10, 0, -1):
                self.route.append(Vector2(i, 30))
        else:
            self.color = (0, 255, 255)
            for i in range (162, 186):
                self.route.append(Vector2(i, 140))
            for i in range (140, 59, -1):
                self.route.append(Vector2(185, i))
            for i in range (185, 271):
                self.route.append(Vector2(i, 60))
            for i in range (60, 1, -1):
                self.route.append(Vector2(270, i))
            for i in range (270, 59, -1):
                self.route.append(Vector2(i, 2))
            for i in range (2, 91):
                self.route.append(Vector2(60, i))
            for i in range (60, 84):
                self.route.append(Vector2(i, 90))
            for i in range (90, 11, -1):
                self.route.append(Vector2(83, i))
            for i in range (83, 163):
                self.route.append(Vector2(i, 12))
            for i in range (12, 141):
                self.route.append(Vector2(162, i))

    def draw_tracks(self):
        for block in self.route:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size )
            pygame.draw.rect(screen ,self.color, block_rect)        

class MAIN:
    def __init__(self):
        self.track0 = TRACK(0)
        self.track1 = TRACK(1)
        self.track2 = TRACK(2)
    
    def draw_elements(self):
        self.track0.draw_tracks()
        self.track1.draw_tracks()
        self.track2.draw_tracks()

# Train class
# class Train:
#     def __init__(self, path, speed):
#         self.path = path
#         self.speed = speed
#         self.current_pos = 0
#         self.x, self.y = self.path[self.current_pos]

#     def update(self):
#         self.current_pos = (self.current_pos + self.speed) % len(self.path)
#         self.x, self.y = self.path[self.current_pos]

#     def draw(self, surface):
#         pygame.draw.rect(surface, TRAIN_COLOR, (self.x, self.y, TRAIN_SIZE, TRAIN_SIZE))

# # Create trains
# trains = [
#     Train(tracks[0], 1),
#     Train(tracks[1], 2),
#     Train(tracks[2], 1),
# ]

# Main game loop
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # # Update trains
    # for train in trains:
    #     train.update()

    # # Draw everything
    screen.fill(BG_COLOR)

    # # Draw tracks
    # for track in tracks:
    #     pygame.draw.lines(screen, TRACK_COLOR, False, track, 5)

    # # Draw trains
    # for train in trains:
    #     train.draw(screen)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(FPS)
