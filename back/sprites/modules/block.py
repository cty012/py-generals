import utils.colors as c
import utils.fonts as f
import utils.functions as utils


class Block:
    def __init__(self, pos, size, owner=None, num=0, terrain='blank', *, align=(0, 0)):
        self.size = size
        self.pos = utils.top_left(pos, (self.size, self.size), align=align)
        # contents
        self.owner = owner
        self.num = num
        self.visible = False
        self.terrain = terrain  # blank, base, city, mountain

    def in_range(self, pos, *, pan=(0, 0)):
        return self.pos[0] + pan[0] < pos[0] < self.pos[0] + self.size + pan[0] and \
               self.pos[1] + pan[1] < pos[1] < self.pos[1] + self.size + pan[1]

    def get_prop(self, prop):
        return eval(f'self.{prop}')

    def set_prop(self, prop, value):
        exec(f'self.{prop} = {value}')

    def fit(self):
        self.num = min(self.num, 9999)
        self.num = max(self.num, -9999)

    def move(self, other):
        if self.num < 1:
            return []
        elif self.owner == other.owner:
            other.num += (self.num - 1)
            self.num = 1
            other.fit()
            return []
        else:
            other.num -= (self.num - 1)
            self.num = 1
            other.fit()
            if other.num < 0:
                enemy = other.owner
                other.owner = self.owner
                other.num = -other.num
                if other.terrain == 'base':
                    return ['conquer', self.owner, enemy]
            return []

    def show(self, ui, players, *, pan=(0, 0)):
        center = (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2)
        # background
        if not self.visible:
            color = c.dark_gray
        elif self.owner is None:
            color = {'blank': c.gray_0, 'mountain': c.gray_1, 'city': c.gray_2}[self.terrain]
        else:
            color = players[self.owner]['color']
        ui.show_div(self.pos, (self.size, self.size), color=color, pan=pan)
        # terrain
        if self.terrain != 'blank' and (self.visible or self.terrain == 'mountain'):
            ui.show_img_by_path(center, f'{self.terrain}.png', align=(1, 1), pan=pan)  # TODO: show terrain
        # number
        if self.visible and self.num > 0:
            ui.show_text(
                center, str(self.num), f.get_font('quicksand', 15, 'otf'),
                color=c.white, save='num', align=(1, 1), pan=pan)
