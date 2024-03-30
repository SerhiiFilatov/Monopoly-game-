import sys
import pygame

import data
from building_cells import BuildingCells
from engine import Engine
from main_menu import MainMenu, Settings
from game_objects import GameBoard



class Monopoly:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Monopoly')
        self.board = pygame.image.load(data.MENU_IMAGE)
        self.main_window = pygame.display.set_mode((data.SCREEN_WIDTH, data.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_status = 'main_menu'
        self.menu_game_objects = []
        self.menu_mouse_handlers = []
        self.bc = BuildingCells()
        self.game_board = GameBoard()
        self.main_menu = MainMenu(self)
        self.engine = Engine(self)
        self.auction_opened = False

    @staticmethod
    def quit():
        sys.exit()

    def draw(self):
        self.main_window.blit(self.board, data.COORDINATES[11])
        for button in self.menu_game_objects:
            button.draw(self.main_window)
        self.game_board.cards_sprites.draw(self.main_window)
        self.bc.draw(self.main_window)
        if self.game_status == 'start':
            self.engine.auction.draw(self.main_window)
            self.engine.end_move_button.draw(self.main_window)
            self.engine.start_move_button.draw(self.main_window)
            self.engine.buy_button.draw(self.main_window)
            self.engine.lvl_up_button.draw(self.main_window)
            self.engine.players_sprites.draw(self.main_window)
            self.engine.player_info.draw(self.main_window)
            self.engine.bot_info.draw(self.main_window)
            self.engine.turn_info.draw(self.main_window)
        pygame.display.update()

    def update(self):
        self.clock.tick(60)
        for number in self.game_board.cards_sprites:
            if number.number == self.engine.cell:
                number.update(self.engine.game_board.cells[self.engine.cell].level)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.game_status == 'main_menu':
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    for handler in self.menu_mouse_handlers:
                        handler(event.type, event.pos)
            if self.game_status == 'start' and Settings.is_dice_roll_allowed:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.engine.end_move_button.handle_mouse_event(event.type, event.pos)
                    self.engine.start_move_button.handle_mouse_event(event.type, event.pos)
                    self.engine.buy_button.handle_mouse_event(event.type, event.pos)
                    self.engine.lvl_up_button.handle_mouse_event(event.type, event.pos)
                    for card in self.engine.game_board.cells:
                        card.handle_mouse_event(event_type=event.type,
                                                pos=event.pos,
                                                main_window=self.main_window,
                                                card=card,
                                                player=self.engine.player_pers)
                    self.engine.auction.handle_mouse_event(event.type, event.pos)


    def run(self):
        while self.game_status != 'finish':
            self.main_window.fill(data.WHITE)
            self.draw()
            self.update()
            self.handle_events()

        self.quit()