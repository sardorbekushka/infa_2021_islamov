import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
RASPBERRY = (255, 0, 125)
MAGENTA = (255, 0, 255)
VIOLET = (125, 0, 255)
BLUE = (0, 0, 255)
OCEAN = (0, 125, 255)
CYAN = (0, 255, 255)
TURQUOISE = (0, 255, 125)
GREEN = (0, 255, 0)
SPRING = (125, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 125, 0)
BLACK = (0, 0, 0)
COLORS = [RED, RASPBERRY, MAGENTA, VIOLET, BLUE, OCEAN,
          CYAN, TURQUOISE, GREEN, SPRING, YELLOW, ORANGE]
point = 0
balls_number = 30
pool = []
new_elements = []
level = 3
min_level = 3
special_score = 10
v_max = 3
font_size = 36


def new_ball():
    """
    создает новый шарик случайного радиуса, случайной скорости и случайного цвета в случайном месте

    :return: none
    """
    global pool
    x = randint(WIDTH//10, WIDTH//2)
    y = randint(HEIGHT//10, HEIGHT//2)
    r = randint(30, 50) / level
    v_x = randint(-v_max, v_max) * level
    v_y = randint(-v_max, v_max) * level
    color = COLORS[randint(0, 11)]
    pool.append([x, y, r, v_x, v_y, color])


def new_element():
    """
    создает новый элемент ссо случайными параметрами и сохраняет его в список

    :return: none
    """
    global new_elements
    x = randint(WIDTH // 10, WIDTH // 2)
    y = randint(HEIGHT // 10, HEIGHT // 2)
    r = randint(50, 70) // level
    new_elements.append([x, y, r])


def draw_balls():
    """
    Функция рисует заданное количество шариков

    :return: none
    """
    global pool
    for t in range(balls_number):
        pool[t][0] += pool[t][3]
        pool[t][1] += pool[t][4]
        circle(screen, pool[t][5], (pool[t][0], pool[t][1]), pool[t][2])


def star():
    """
    рисует на поверхности surf звезду случайного размера и цвета
    :return: surf
    """
    surf = pygame.Surface((10, 10))
    pygame.draw.polygon(surf, COLORS[randint(0, 11)],
                        ((5, 0), (9, 10), (0, 3), (10, 3), (1, 10)))
    return surf


def draw_new_elements():
    """
    перемещает ноыве элементы и рисует их на экране

    :return: none
    """
    global new_elements
    for t in range(len(new_elements)):
        new_elements[t][0] += randint(-v_max, v_max) * 2*level
        new_elements[t][1] += randint(-v_max, v_max) * 2*level
        r = new_elements[t][2]
        screen.blit(pygame.transform.scale(star(), (r, r)), (new_elements[t][0], new_elements[t][1]))
        pygame.display.update()


def bump_border(ball):
    """
    Функция отталкивает шарик от стен в случае столкновения

    :param ball: шарик, столкновение котрого проверяет функция
    :return: none
    """
    if abs(ball[0] - WIDTH/2) > WIDTH/2-ball[2]:
        ball[3] = -ball[3]
        ball[0] += ball[3]
    if abs(ball[1] - HEIGHT/2) > HEIGHT/2-ball[2]:
        ball[4] = -ball[4]
        ball[1] += ball[4]


def bump_balls():
    """
    Функция отталкивает шарики в случае столкновения

    :return: none
    """
    for p in range(balls_number):
        ball_1 = pool[p]
        for n in range(balls_number):
            if n != p:
                ball_2 = pool[n]
                m = ball_1[2] / ball_2[2]
                if ((ball_1[0]-ball_2[0])**2 + (ball_1[1]-ball_2[1])**2
                        <= (ball_1[2]+ball_2[2])**2):
                    ball_1[3], ball_2[3] = m*ball_2[3], ball_1[3]/m
                    ball_1[4], ball_2[4] = m*ball_2[4], ball_1[4]/m
                    ball_1[0] += ball_1[3]
                    ball_1[1] += ball_1[4]
                    ball_2[0] += ball_2[3]
                    ball_2[1] += ball_2[4]


def click(event_):
    """
    обрабатывает щелчок мыши: распознает словил ли пользователь шарик или новый элемент

    :param event_: event
    :return: none
    """
    global point, pool, new_elements
    for j in range(balls_number):
        r = pool[j][2]
        if (event_.pos[0] - pool[j][0]) ** 2 + (event_.pos[1] - pool[j][1]) ** 2 <= r ** 2:
            print('pop!')
            point += 1
            pool.pop(j)
            new_ball()
    for j in range(len(new_elements)):
        r = new_elements[j][2]
        if (event_.pos[0] - new_elements[j][0]) ** 2 + (event_.pos[1] - new_elements[j][1]) ** 2 <= r ** 2:
            print('POP!')
            point += 1
            new_elements.pop(j)
            new_element()
            point += special_score


def point_version(point_):
    """
    определят необходимый падеж слова очки

    :param point_: количество очков
    :return: слово в нужном падеже
    """
    if point_ % 10 == 1 and point_ % 100 != 11:
        version = 'очко'
    elif point_ % 10 in (2, 3, 4) and point_ % 100 not in (12, 13, 14):
        version = 'очка'
    else:
        version = 'очков'
    return version


name = input()

for i in range(balls_number):
    new_ball()

pygame.display.update()
clock = pygame.time.Clock()
finished = False
entered = False

font = pygame.font.SysFont('Roboto', font_size)

while not finished:
    clock.tick(FPS)
    pygame.key.start_text_input()
    name = pygame.TEXTINPUT
    pygame.key.stop_text_input()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print('Вы набрали', point, point_version(point) + '! время:', pygame.time.get_ticks()/1000, 'с')

    text = font.render('SCORE: ' + str(point), False, RED)
    screen.blit(text, (WIDTH-text.get_width(), 0))
    draw_balls()
    for k in range(balls_number):
        bump_border(pool[k])
    bump_balls()
    if level >= min_level:
        if randint(0, 500//level) == 500//level:
            new_element()
    draw_new_elements()
    for k in range(len(new_elements)):
        if (abs(new_elements[k][0]-WIDTH/2) > WIDTH/2) or \
                (abs(new_elements[k][1]-HEIGHT/2) > HEIGHT/2):
            new_elements.pop(k)
            new_element()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
