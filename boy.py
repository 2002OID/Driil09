import math

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def time_out_5(e):
    return e[0] == 'TIME_OUT' and e[1] == 5.0


class Idle:
    @staticmethod  # 클래스를 여러개의 함수를 grouping 하는 용도로 활용 가능
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.statr_time > 5:
            boy.state_machine.hendle_event(('TIME_OUT', 0))
        print('Idel Doing')  # 디버깅용

    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.statr_time = get_time() #경과시간
        print('Idel Entering')  # 디버깅용

    @staticmethod
    def exit(boy):
        print('Idel Exiting')  # 디버깅용

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Sleep:

    @staticmethod  # 클래스를 여러개의 함수를 grouping 하는 용도로 활용 가능
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁 드르렁')  # 디버깅용

    @staticmethod
    def enter(boy):
        boy.frame = 0
        print('눕기')  # 디버깅용

    @staticmethod
    def exit(boy):
        print('일어서기')  # 디버깅용

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, math.pi / 2, '', boy.x - 25,
                                      boy.y - 25, 100, 100)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Sleep
        self.table = {
            Sleep: {space_down: Idle},
            Idle: {time_out: Sleep}
        }

    def start(self):
        self.cur_state.enter(self.boy)

    def hendle_event(self, e):
        for cheak_event, next_state in self.table[self.cur_state].items():
            if cheak_event(e):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
                return True
        return False

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        # self.frame = (self.frame + 1) % 8
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.hendle_event(('INPUT', event))
        pass

    def draw(self):
        # self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
        self.state_machine.draw()
