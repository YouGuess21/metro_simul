import pygame, sys, random
from pygame.math import Vector2

pygame.init()

FPS = 60
BG_COLOR = (0, 0, 0)
cell_size = 5
cell_number = 200

screen = pygame.display.set_mode((cell_size * cell_number * 1.8, cell_number * cell_size))
pygame.display.set_caption("Metro simulation")

def get_random_start_index(base_index):
    return max(0, base_index + random.randint(-30, 30))

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
    
    def to_set(self):
        return set((block.x, block.y) for block in self.route)

class SIGNAL:
    def __init__(self, pos):
        self.pos = pos
        self.flag = False

    def draw_signal(self):
        color = (0, 100, 0) if not self.flag else (200, 0, 0)
        sign_rect = pygame.Rect(self.pos.x * cell_size - 0.5 * cell_size, self.pos.y * cell_size - 0.5 * cell_size, 2 * cell_size, 2* cell_size)
        pygame.draw.rect(screen, color, sign_rect)

    def update_signal(self, flag):
        self.flag = flag

class SENSOR:
    def __init__(self, pos, ntype):
        self.pos = pos
        self.type = ntype # ntype is sensor type: 0 is caution, 1 safety
        self.flag = False

    def draw_sensor(self):
        sens_rect = pygame.Rect(self.pos.x * cell_size - 0.5 * cell_size, self.pos.y * cell_size - 0.5 * cell_size, 2 * cell_size, 2 * cell_size)
        pygame.draw.rect(screen, (235, 235, 235), sens_rect)
        bor_rect = pygame.Rect(self.pos.x * cell_size - 0.5 * cell_size, self.pos.y * cell_size - 0.5 * cell_size, 2 * cell_size, 2 * cell_size)
        pygame.draw.rect(screen, (0, 0, 0), bor_rect, 1)

class TRAIN:
    def __init__(self, track, start_index, length=5):
        self.color = (1, 225, 1)
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

    def check_signals(self, signals, signal_to_caution):
        train_head = (self.body[0].x, self.body[0].y)
        for sensor_pos in signal_to_caution.get(train_head, []):
            for signal in signals:
                if signal.pos == sensor_pos and signal.flag:  # Signal is red
                    self.stop = True
                    return
        self.stop = False


    def move_train(self):
        if not self.stop:
            self.position_indices = [(index - 1) % len(self.track.route) for index in self.position_indices]
            self.body = [self.track.route[i] for i in self.position_indices]


class MAIN:
    def __init__(self):
        self.track0 = TRACK(0)
        self.track1 = TRACK(1)
        self.track2 = TRACK(2)

        self.intersections = self.find_intersections()

        self.trains = []
        self.sensors = []
        self.signals = []

        for track, base_index in [(self.track0, 0), (self.track0, 150), (self.track0, 580),
                                  (self.track1, 0), (self.track1, 315), (self.track1, 630), (self.track1, 945),
                                  (self.track2, 0), (self.track2, 288), (self.track2, 574)]:
            random_start_index = get_random_start_index(base_index)
            self.trains.append(TRAIN(track, random_start_index))

        caution_sensor_positions = [
            (Vector2(260, 30), 0), (Vector2(270, 20), 0), (Vector2(225, 170), 0), (Vector2(205, 180), 0),
            (Vector2(215, 160), 0), (Vector2(152, 30), 0), (Vector2(162, 40), 0), (Vector2(130, 180), 0),
            (Vector2(150, 170), 0), (Vector2(140, 160), 0), (Vector2(340, 100), 0), (Vector2(330, 80), 0),
            (Vector2(320, 90), 0), (Vector2(50, 30), 0), (Vector2(60, 40), 0), (Vector2(20, 140), 0),
            (Vector2(40, 150), 0), (Vector2(30, 160), 0), (Vector2(83, 20), 0)
        ]

        for pos, sensor_type in caution_sensor_positions:
            self.sensors.append(SENSOR(pos, sensor_type))
        
        signal_positions = [
            (Vector2(260, 25)), (Vector2(275, 20)), (Vector2(227, 165)), (Vector2(202, 180)),
            (Vector2(219, 158)), (Vector2(150, 25)), (Vector2(166, 42)), (Vector2(126, 182)),
            (Vector2(150, 165)), (Vector2(145, 160)), (Vector2(341, 105)), (Vector2(335, 80)),
            (Vector2(320, 86)), (Vector2(50, 26)), (Vector2(56, 41)), (Vector2(20, 136)),
            (Vector2(40, 146)), (Vector2(26, 160)), (Vector2(86, 18))
        ]

        for pos in signal_positions:
            self.signals.append(SIGNAL(pos))

        safety_sensor_position = [
            (Vector2(285, 30), 1), (Vector2(270, 45), 1), (Vector2(190, 170), 1), (Vector2(205, 155), 1),
            (Vector2(215, 185), 1), (Vector2(177, 30), 1), (Vector2(162, 15), 1), (Vector2(130, 155), 1),
            (Vector2(115, 170), 1), (Vector2(140, 185), 1), (Vector2(315, 100), 1), (Vector2(330, 115), 1),
            (Vector2(345, 90), 1), (Vector2(98, 30), 1), (Vector2(60, 15), 1), (Vector2(45, 140), 1),
            (Vector2(15, 150), 1), (Vector2(30, 125), 1), (Vector2(83, 45), 1)
        ]

        for pos, sensor_type in safety_sensor_position:
            self.sensors.append(SENSOR(pos, sensor_type))

        self.caution_to_signal = {
            (260, 30): [Vector2(275, 20)], (270, 20): [Vector2(260, 25)], (225, 170): [Vector2(219, 158), Vector2(202, 180)],
            (205, 180): [Vector2(227, 165)], (215, 160): [Vector2(227, 165)], (152, 30): [Vector2(166, 42)],
            (162, 40): [Vector2(150, 25)], (130, 180): [Vector2(150, 165)], (150, 170): [Vector2(145, 160), Vector2(126, 182)],
            (140, 160): [Vector2(150, 165)], (340, 100): [Vector2(335, 80)], (330, 80): [Vector2(341, 105), Vector2(320, 86)],
            (320, 90): [Vector2(335, 80)], (50, 30): [Vector2(56, 41), Vector2(86, 18)], (60, 40): [Vector2(50, 26)],
            (20, 140): [Vector2(26, 160)], (40, 150): [Vector2(26, 160)], (30, 160): [Vector2(20, 136), Vector2(40, 146)],
            (83, 20): [Vector2(50, 26)]
        }

        self.caution_to_safety = {
            (260, 30): Vector2(285, 30), (270, 20): Vector2(270, 45), (225, 170): Vector2(190, 170),
            (205, 180): Vector2(205, 155), (215, 160): Vector2(215, 185), (152, 30): Vector2(177, 30),
            (162, 40): Vector2(162, 15), (130, 180): Vector2(130, 155), (150, 170): Vector2(115, 170),
            (140, 160): Vector2(140, 185), (340, 100): Vector2(315, 100), (330, 80): Vector2(330, 115),
            (320, 90): Vector2(345, 90), (50, 30): Vector2(98, 30), (60, 40): Vector2(60, 15),
            (20, 140): Vector2(45, 140), (40, 150): Vector2(15, 150), (30, 160): Vector2(30, 125),
            (83, 20): Vector2(83, 45)
        }

        self.signal_to_caution = {
            (260, 30): [Vector2(260, 25)], (270, 20): [Vector2(275, 20)], (225, 170): [Vector2(227, 165)],
            (205, 180): [Vector2(202, 180)], (215, 160): [Vector2(219, 158)], (152, 30): [Vector2(150, 25)],
            (162, 40): [Vector2(166, 42)], (130, 180): [Vector2(126, 182)], (150, 170): [Vector2(150, 165)],
            (140, 160): [Vector2(145, 160)], (340, 100): [Vector2(341, 105)], (330, 80): [Vector2(335, 80)],
            (320, 90): [Vector2(320, 86)], (50, 30): [Vector2(50, 26)], (60, 40): [Vector2(56, 41)],
            (20, 140): [Vector2(20, 136)], (40, 150): [Vector2(40, 146)], (30, 160): [Vector2(26, 160)],
            (83, 20): [Vector2(86, 18)]
        }

    def draw_elements(self):
        self.track0.draw_tracks()
        self.track1.draw_tracks()
        self.track2.draw_tracks()

        for sensor in self.sensors:
            sensor.draw_sensor()

        for train in self.trains:
            train.draw_train()

        for signal in self.signals:
            signal.draw_signal()

        for intersection in self.intersections:
            intersect_rect = pygame.Rect(intersection[0] * cell_size, intersection[1] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), intersect_rect)

            border_rect = pygame.Rect(
                intersection[0] * cell_size - 0.5 * cell_size - 5,
                intersection[1] * cell_size - 0.5 * cell_size - 5,
                cell_size * 2 + 10,
                cell_size * 2 + 10
            )
            pygame.draw.rect(screen, (50, 150, 50), border_rect, 1)

    def update(self):
        for train in self.trains:
            train.check_signals(self.signals, self.signal_to_caution)
            train.move_train()

            train_head = (train.body[0].x, train.body[0].y)

            for sensor in self.sensors:
                if (train_head == (sensor.pos.x, sensor.pos.y)):
                    if sensor.type == 0:
                        sensor.flag = True
                        if (sensor.pos.x, sensor.pos.y) in self.caution_to_signal:
                            for signal_pos in self.caution_to_signal[(sensor.pos.x, sensor.pos.y)]:
                                for signal in self.signals:
                                    if signal.pos == signal_pos:
                                        signal.update_signal(True)
                    elif sensor.type == 1:
                        sensor.flag = True
                        for caution_pos, safety_pos in self.caution_to_safety.items():
                            if safety_pos == sensor.pos:
                                for signal_pos in self.caution_to_signal[caution_pos]:
                                    for signal in self.signals:
                                        if signal.pos == signal_pos:
                                            signal.update_signal(False)

    def find_intersections(self):
        set0 = self.track0.to_set()
        set1 = self.track1.to_set()
        set2 = self.track2.to_set()

        intersections = set0.intersection(set1).union(set0.intersection(set2)).union(set1.intersection(set2)) # print(intersections)
        return intersections

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
