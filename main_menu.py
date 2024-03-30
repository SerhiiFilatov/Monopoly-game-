import pygame
from dataclasses import dataclass



@dataclass
class Settings:
    player_colour = 'cat'
    turn_order = 'player'
    is_dice_roll_allowed = True



class Button:
    def __init__(self, x, y, w, h, text, command=lambda x: None):
        self.borders = pygame.Rect(x, y, w, h)
        self.command = command
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.type = None

    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)

    def handle_mouse_down(self, pos):
        if self.borders.collidepoint(pos):
            self.command()

    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, (86, 90, 94), self.borders, border_radius=20)
        if self.text:
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = self.borders.center
            surface.blit(text_surface, text_rect)



class SettingObjects:
    def __init__(self, x, y, w, h, type, value, command):
        self.borders = pygame.Rect(x, y, w, h)
        self.command = command
        self.type = type
        self.value = value
        self.active_status = False
        self.is_expanded = False
        self.original_width = w
        self.original_height = h

    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)

    def handle_mouse_down(self, pos):
        if self.borders.collidepoint(pos):
            if not self.active_status:
                self.activate()
            else:
                self.deactivate()

    def activate(self):
        self.command()
        self.active_status = True
        if self.type == 'player_model':
            Settings.player_colour = self.value
        if self.type == 'turn_order':
            Settings.turn_order = self.value
        if not self.is_expanded:
            self.is_expanded = True
            self.borders.width += 6
            self.borders.height += 6

    def deactivate(self):
        self.active_status = False
        if self.is_expanded:
            self.is_expanded = False
            self.borders.width = self.original_width
            self.borders.height = self.original_height

    def update(self):
        if not self.active_status:
            self.is_expanded = False

    def draw(self, surface):
        if self.active_status:
            color = (0, 127, 14)
        else:
            color = (86, 90, 94)
        pygame.draw.rect(surface, color, self.borders, border_radius=20)



class MainMenu():
    def __init__(self, monopoly):
        self.Monopoly = monopoly
        self.position = (160, 160)
        self.main_menu_buttons = []
        self.main_menu_mouse_handlers = []
        self.settings_obj = []
        self.settings_obj_mouse_handlers = []
        self.create_buttons()

    def create_buttons(self):

        def on_start():
            for b in self.main_menu_buttons:
                self.Monopoly.menu_game_objects.remove(b)
            for b in self.main_menu_mouse_handlers:
                self.Monopoly.menu_mouse_handlers.remove(b)
            self.Monopoly.game_status = 'start'

        def on_settings():
            for b in self.main_menu_buttons:
                self.Monopoly.menu_mouse_handlers.remove(b.handle_mouse_event)
                if b.text == 'Start':
                    self.Monopoly.menu_game_objects.remove(b)
                if b.text == 'Exit':
                    self.Monopoly.menu_game_objects.remove(b)
            for b in self.main_menu_buttons:
                if b.text == 'Settings':
                    b.borders = pygame.Rect(650, 200, 100, 50)
                    b.text = 'choose your figure'
            self.create_set_obj()

        def on_quit():
            self.Monopoly.game_status = 'finish'

        def add_but_obj(x, y, w, h, text, command):
            but_obj = Button(x, y, w, h, text, command)
            self.main_menu_buttons.append(but_obj)
            self.main_menu_mouse_handlers.append(but_obj.handle_mouse_event)
            self.Monopoly.menu_game_objects.append(but_obj)
            self.Monopoly.menu_mouse_handlers.append(but_obj.handle_mouse_event)

        main_buttons_data = {
            'start': ('Start', on_start),
            'settings': ('Settings', on_settings),
            'finish': ('Exit', on_quit)
        }

        for i, (text, click_handler) in enumerate(main_buttons_data.values()):
            add_but_obj(x=750, y=200 + (50 + 50) * i, w=100, h=50, text=text, command=click_handler)

    def create_set_obj(self):

        def deactivate_mark_model():
            for b in self.settings_obj:
                if b.type == 'player_model':
                    b.deactivate()

        def deactivate_turn_order():
            for b in self.settings_obj:
                if b.type == 'turn_order':
                    b.deactivate()

        def back_to_menu():
            self.Monopoly.menu_game_objects.clear()
            self.Monopoly.menu_mouse_handlers.clear()
            self.main_menu_buttons.clear()
            self.main_menu_mouse_handlers.clear()
            self.create_buttons()

        def add_set_obj(x, y, w, h, type, value, command):
            set_obj = SettingObjects(x, y, w, h, type, value, command)
            self.settings_obj.append(set_obj)
            self.settings_obj_mouse_handlers.append(set_obj.handle_mouse_event)
            self.Monopoly.menu_game_objects.append(set_obj)
            self.Monopoly.menu_mouse_handlers.append(set_obj.handle_mouse_event)

        set_obj_data = {
            'red': ('cat', deactivate_mark_model),
            'green': ('dog', deactivate_mark_model),
            'blue': ('bird', deactivate_mark_model)
        }

        set_obj_data_turn_order = {
            'player': ('player', deactivate_turn_order),
            'bot': ('bot', deactivate_turn_order),
        }

        for i, (model, click_handler) in enumerate(set_obj_data.values()):
            add_set_obj(x=650 + (50 + 50) * i, y=300, w=50, h=50,
                        type='player_model', value=model, command=click_handler)

        for i, (turn, click_handler) in enumerate(set_obj_data_turn_order.values()):
            add_set_obj(x=650 + (50 + 50) * i, y=400, w=50, h=50,
                        type='turn_order', value=turn, command=click_handler)

        but_back = Button(x=650, y=500, w=100, h=50, text='Back', command=back_to_menu)
        self.settings_obj.append(but_back)
        self.settings_obj_mouse_handlers.append(but_back.handle_mouse_event)
        self.Monopoly.menu_game_objects.append(but_back)
        self.Monopoly.menu_mouse_handlers.append(but_back.handle_mouse_event)