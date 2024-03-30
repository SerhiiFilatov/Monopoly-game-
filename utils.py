import os



class Position:
    def __init__(self, pos):
        self.pos = pos

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]


def find_object(obj, mouse_pos, surface):
    mouse = Position(mouse_pos)
    game_obj = Position(obj)
    surf = Position(surface)

    relative_mouse_x = mouse.x - surf.x
    relative_mouse_y = mouse.y - surf.y

    if (relative_mouse_x > game_obj.x and relative_mouse_x < game_obj.x + obj.width) and \
            (relative_mouse_y > game_obj.y and relative_mouse_y < game_obj.y + obj.height):
        return True
    else:
        return False


def get_building_lvl(direct, index=0):
    if os.path.isdir(direct) and index < len(os.listdir(direct)):
        return os.path.join(direct, os.listdir(direct)[index])
    else:
        return os.path.join(direct)