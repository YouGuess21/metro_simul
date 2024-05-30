import pygame
import sys
from pygame.math import Vector2

pygame.init()

FPS = 60
BG_COLOR = (0, 0, 0)
cell_size = 5
cell_number = 200

screen = pygame.display.set_mode((cell_size * cell_number * 1.8, cell_number * cell_size))
pygame.display.set_caption("Train Tracks")

class TRACK:
    def __init__(self, train_number):
        self.route = []
        if train_number == 0:
            self.color = (255, 165, 0)
            for i in range(30, 171):
                self.route.append(Vector2(30, i))
            for i in range(30, 331):
                self.route.append(Vector2(i, 170))
            for i in range(170, 29, -1):
                self.route.append(Vector2(330, i))
            for i in range(330, 30, -1):
                self.route.append(Vector2(i, 30))
        elif train_number == 1:
            self.color = (160, 32, 240)
            for i in range(30, 151):
                self.route.append(Vector2(1, i))
            for i in range(1, 131):
                self.route.append(Vector2(i, 150))
            for i in range(150, 199):
                self.route.append(Vector2(130, i))
            for i in range(130, 216):
                self.route.append(Vector2(i, 198))
            for i in range(198, 99, -1):
                self.route.append(Vector2(215, i))
            for i in range(215, 360):
                self.route.append(Vector2(i, 100))
            for i in range(100, 89, -1):
                self.route.append(Vector2(359, i))
            for i in range(359, 204, -1):
                self.route.append(Vector2(i, 90))
            for i in range(90, 189):
                self.route.append(Vector2(205, i))
            for i in range(205, 139, -1):
                self.route.append(Vector2(i, 188))
            for i in range(188, 139, -1):
                self.route.append(Vector2(140, i))
            for i in range(140, 9, -1):
                self.route.append(Vector2(i, 140))
            for i in range(140, 29, -1):
                self.route.append(Vector2(10, i))
            for i in range(10, 0, -1):
                self.route.append(Vector2(i, 30))
        else:
            self.color = (0, 255, 255)
            for i in range(162, 186):
                self.route.append(Vector2(i, 140))
            for i in range(140, 59, -1):
                self.route.append(Vector2(185, i))
            for i in range(185, 271):
                self.route.append(Vector2(i, 60))
            for i in range(60, 1, -1):
                self.route.append(Vector2(270, i))
            for i in range(270, 59, -1):
                self.route.append(Vector2(i, 2))
            for i in range(2, 91):
                self.route.append(Vector2(60, i))
            for i in range(60, 84):
                self.route.append(Vector2(i, 90))
            for i in range(90, 11, -1):
                self.route.append(Vector2(83, i))
            for i in range(83, 163):
                self.route.append(Vector2(i, 12))
            for i in range(12, 141):
                self.route.append(Vector2(162, i))

    def draw_tracks(self):
        for block in self.route:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, block_rect)

class TRAIN:
    def __init__(self, track, start_index, length=5):
        self.color = (0, 255, 0)
        self.track = track
        self.start_index = start_index
        self.position_indices = [(start_index + i) % len(self.track.route) for i in range(length)]
        self.body = [self.track.route[i] for i in self.position_indices]

    def draw_train(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size - 0.5 * cell_size, block.y * cell_size - 0.5 * cell_size, cell_size * 2, cell_size * 2)
            pygame.draw.rect(screen, self.color, block_rect)

            border_rect = pygame.Rect(block.x * cell_size - 0.5 * cell_size, block.y * cell_size - 0.5 * cell_size, cell_size * 2, cell_size * 2)
            pygame.draw.rect(screen, (0, 0, 0), border_rect, 1)  # The last argument is the width of the border


    def move_train(self):
        self.position_indices = [(index + 1) % len(self.track.route) for index in self.position_indices]
        self.body = [self.track.route[i] for i in self.position_indices]

class MAIN:
    def __init__(self):
        self.track0 = TRACK(0)
        self.track1 = TRACK(1)
        self.track2 = TRACK(2)

        self.train0 = TRAIN(self.track0, start_index=0, length=4)  
        self.train1 = TRAIN(self.track0, start_index=294, length=4)  
        self.train2 = TRAIN(self.track0, start_index=580, length=4) 
        self.train3 = TRAIN(self.track1, start_index=0, length=4)  
        self.train4 = TRAIN(self.track1, start_index=315, length=4)  
        self.train5 = TRAIN(self.track1, start_index=630, length=4)  
        self.train6 = TRAIN(self.track1, start_index=945, length=4) 
        self.train7 = TRAIN(self.track2, start_index=0, length=4) 
        self.train8 = TRAIN(self.track2, start_index=288, length=4)  
        self.train9 = TRAIN(self.track2, start_index=574, length=4)   
 
    def draw_elements(self):
        self.track0.draw_tracks()
        self.track1.draw_tracks()
        self.track2.draw_tracks()
        self.train0.draw_train()
        self.train1.draw_train()
        self.train2.draw_train()
        self.train3.draw_train()
        self.train4.draw_train()
        self.train5.draw_train()
        self.train6.draw_train()
        self.train7.draw_train()
        self.train8.draw_train()
        self.train9.draw_train()

    def update(self):
        self.train0.move_train()
        self.train1.move_train()
        self.train2.move_train()
        self.train3.move_train()
        self.train4.move_train()
        self.train5.move_train()
        self.train6.move_train()
        self.train7.move_train()
        self.train8.move_train()
        self.train9.move_train()

clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

    screen.fill(BG_COLOR)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(FPS)
