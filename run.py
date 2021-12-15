from src.visualization import World
from src.ball import Ball
from src.racket import Racket
from src.analyzer import Analyzer
from src.prognosticator import Prognosticator
import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('src/config.ini')

    """World settings"""
    WORLD_HEIGHT = config.getint('WORLD', 'height')
    WORLD_WIDTH = config.getint('WORLD', 'width')

    START_FRAME = config.getint('WORLD', 'start_frame_y')
    END_FRAME = config.getint('WORLD', 'end_frame_y')

    FRAME_COLOR = config.get('VISUALIZATION', 'frame_color')
    FRAME_COLOR = tuple(int(k.strip()) for k in FRAME_COLOR[1:-1].split(','))

    BALL_RADIUS = config.getint('BALL', 'ball_radius')
    BALL_COLOR = config.get('VISUALIZATION', 'ball_color')
    BALL_COLOR = tuple(int(k.strip()) for k in BALL_COLOR[1:-1].split(','))

    RACKET_COLOR = config.get('VISUALIZATION', 'racket_color')
    RACKET_COLOR = tuple(int(k.strip()) for k in RACKET_COLOR[1:-1].split(','))

    VERT_DECREASE = config.getfloat('DECREASE', 'vert_decrease')
    HOR_DECREASE = config.getfloat('DECREASE', 'hor_decrease')

    world = World(WORLD_HEIGHT, WORLD_WIDTH,
                  START_FRAME, END_FRAME, FRAME_COLOR,
                  BALL_COLOR, BALL_RADIUS,
                  RACKET_COLOR)

    """ball settings"""
    BALL_START_X = config.getint('BALL', 'center_x')
    BALL_START_Y = config.getint('BALL', 'center_y')

    HORIZONTAL_V = config.getint('BALL', 'horizontal_v')
    HORIZONTAL_A = config.getfloat('BALL', 'horizontal_a')

    VERTICAL_V = config.getint('BALL', 'vertical_v')
    VERTICAL_A = config.getfloat('BALL', 'vertical_a')

    ball = Ball(BALL_START_X, BALL_START_Y, BALL_RADIUS)

    ball.horizontal_v = HORIZONTAL_V
    ball.horizontal_a = HORIZONTAL_A

    ball.vertical_v = VERTICAL_V
    ball.vertical_a = VERTICAL_A

    """racket settings"""
    RACKET_CENTER_Y = config.getint('RACKET', 'center_y')
    RACKET_SIZE = config.getint('RACKET', 'size')
    RACKET_PLANE_X = config.getint('RACKET', 'racket_plane_x')

    racket = Racket(RACKET_PLANE_X, RACKET_CENTER_Y, RACKET_SIZE)

    """analyzer settings"""
    analyzer = Analyzer(START_FRAME, END_FRAME)

    """prognosticator settings"""
    prognosticator = Prognosticator()

    """main part"""
    time = 0
    while ball.right_border_x < WORLD_WIDTH and ball.down_border_y < WORLD_HEIGHT and ball.upper_border_y > 0:
        time += 1
        ball.horizontal_shift(time)
        ball.vertical_shift(time)
        ball.vertical_acceleration_decrease(VERT_DECREASE)
        ball.update_borders()
        world.visualize(ball.center_y, ball.center_x, racket.plane_x, racket.center_y, racket.size)
        aim = analyzer.analyze()
        if aim is not None:
            racket.aiming(WORLD_HEIGHT, aim[1])
            prognosticator.collect_data(aim)
        else:
            if prognosticator.data:
                prognosis = prognosticator.prognostication(WORLD_WIDTH, BALL_RADIUS)
                racket.aiming(WORLD_HEIGHT, prognosis)
                prognosticator.data.clear()

    print('------------')
    print('results:')
    print('ball center coordinates is ', ball.center_x, ball.center_y)
    print('racket center y is ', racket.center_y)
    racket_upper_edge = racket.get_racket_upper_edge_y()
    print('racket upper edge', racket_upper_edge)
    racket_down_edge = racket.get_racket_down_edge_y()
    print('racket down edge', racket_down_edge)
    if racket_upper_edge <= ball.center_y <= racket_down_edge:
        print('SUCCESS!!!')
    else:
        print('FAIL!!!')


