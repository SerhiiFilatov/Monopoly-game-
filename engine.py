import pygame
import random

import data
import main_menu
from game_objects import GameBoard, PlayerModel, InfoPanel, Auction
from main_menu import Settings
from text_object import TextObject



class Engine:
    def __init__(self, game):
        self.game = game
        self.players_sprites = pygame.sprite.Group()
        self.game_board = GameBoard()
        self.player_pers = PlayerModel(image=data.PLAYER_MODEL_1,
                                       coord=data.COORDINATES[45],
                                       card_type='player',
                                       money=10000)
        self.bot_pers = PlayerModel(image=data.PLAYER_MODEL_2,
                                    coord=data.COORDINATES[45],
                                    card_type='bot',
                                    money=10000)
        self.players_sprites.add(self.player_pers)
        self.players_sprites.add(self.bot_pers)
        self.cell = 0
        self.roll_result = 0
        self.game_rounds = [False, False]
        self.all_rounds = 0
        self.cell_level_increased = False
        self.special_objects = []
        self.auc_create = False
        self.create_objects()

    def create_objects(self):
        self.player_info = InfoPanel(177, 175, 150, 300, model=self.player_pers, image_path=data.GRUNGLE)
        self.bot_info = InfoPanel(794, 175, 150, 300, model=self.bot_pers, image_path=data.GRUNGLE)
        self.turn_info = InfoPanel(520, 180, 90, 30, turn=Settings, image_path=data.GRUNGLE)
        self.start_move_button = main_menu.Button(450, 275, 100, 40, text='Start move', command=self.player_turn)
        self.end_move_button = main_menu.Button(600, 275, 100, 40, text='End move', command=self.end_turn)
        self.buy_button = main_menu.Button(375, 350, 100, 40, text='Buy', command=self.player_buy_commerce)
        self.lvl_up_button = main_menu.Button(675, 350, 100, 40, text='Lvl_up', command=self.lvl_up)
        self.auction = Auction(425, 420, image_path=data.GRUNGLE)

    def dice_roll_result(self):
        self.roll_result = random.randint(10, 10)
        return self.roll_result

    def take_turn(self, player):
        self.create_special_cards_list()
        if Settings.turn_order == player:
            dice_res = self.dice_roll_result()
            current_loc = self.player_pers.current_position if player == 'player' else self.bot_pers.current_position
            new_loc = (current_loc + dice_res) % len(self.game_board.cells)

            if player == 'player':

                if self.player_pers.prison_status:
                    self.player_pers.time_in_prison -= 1
                    if self.player_pers.time_in_prison <= 0:
                        self.player_pers.prison_status = False

                else:
                    self.cell_level_increased = True
                    self.player_pers.move(new_coord=self.game_board.cells[new_loc].location, new_position=new_loc)

                    if self.game_board.cells[new_loc].owner == 'bot':
                        self.player_pers.wallet -= self.game_board.cells[new_loc].rent
                        self.bot_pers.wallet += self.game_board.cells[new_loc].rent
                        self.show_message(f'You paid the rent {self.game_board.cells[new_loc].rent}')

            else:

                if self.bot_pers.prison_status:
                    self.bot_pers.time_in_prison -= 1
                    if self.bot_pers.time_in_prison <= 0:
                        self.bot_pers.prison_status = False

                else:
                    self.bot_pers.move(new_coord=self.game_board.cells[new_loc].location, new_position=new_loc)
                    self.bot_buy_commerce()
                    self.bot_lvl_up()

                    if self.game_board.cells[new_loc].owner == 'player':
                        self.bot_pers.wallet -= self.game_board.cells[new_loc].rent
                        self.player_pers.wallet += self.game_board.cells[new_loc].rent
                        self.show_message(f'Bot paid the rent {self.game_board.cells[new_loc].rent}')

            if all(self.game_rounds):
                self.game_rounds = [False] * len(self.game_rounds)
                self.all_rounds += 1

            if current_loc > new_loc:
                self.process_start_cell(player)

            if self.game_board.cells[new_loc].card_type == 'customs_house':
                if player == 'player':
                    self.enter_customs(self.player_pers)
                else:
                    self.enter_customs(self.bot_pers)

            if self.game_board.cells[new_loc].card_type == 'court':
                if player == 'player':
                    self.enter_court(self.player_pers)
                else:
                    self.enter_court(self.bot_pers)

            if self.game_board.cells[new_loc].card_type == 'event':
                if player == 'player':
                    ...
                else:
                    ...

            Settings.turn_order = 'bot' if player == 'player' else 'player'
            self.roll_result = 0
            self.cell = new_loc

    def process_start_cell(self, player):
        start_money = 200
        if player == 'player':
            self.game_rounds[0] = True
            self.player_pers.wallet += start_money
            self.show_message("You passed START! Collect $200")
        else:
            self.game_rounds[1] = True
            self.bot_pers.wallet += start_money
            self.show_message("Bot passed START! Collect $200")

    def player_buy_commerce(self):
        cell = self.player_pers.current_position
        cell_owner = self.game_board.cells[cell].owner
        if cell_owner is None:
            if Settings.turn_order == 'bot':
                self.game_board.cells[cell].owner = 'player'
                self.player_pers.wallet -= self.game_board.cells[cell].price
                self.player_pers.real_estate.append(self.game_board.cells[cell].title)
                self.show_message(f'{self.game_board.cells[cell].owner} buy {self.game_board.cells[cell].title}')

    def bot_buy_commerce(self):
        cell = self.bot_pers.current_position
        cell_owner = self.game_board.cells[cell].owner
        if cell_owner is None:
            self.game_board.cells[cell].owner = 'bot'
            self.bot_pers.wallet -= self.game_board.cells[cell].price
            self.show_message(f'{self.game_board.cells[cell].owner} buy {self.game_board.cells[cell].title}')
            self.bot_pers.real_estate.append(self.game_board.cells[cell].title)

    def bot_sell_commerce(self):
        cell = self.player_pers.current_position if Settings.turn_order == 'bot' else self.bot_pers.current_position
        cell_owner = self.game_board.cells[cell].owner
        if Settings.turn_order != cell_owner and cell_owner != 'game_master':
            if self.game_board.cells[cell].owner == 'bot':
                if self.game_board.cells[cell].title in self.bot_pers.real_estate:
                    index_to_remove = self.bot_pers.real_estate.index(self.game_board.cells[cell].title)
                    self.bot_pers.wallet += self.game_board.cells[cell].price * 0.5
                    self.bot_pers.real_estate.pop(index_to_remove)
            self.game_board.cells[cell].owner = None

    def lvl_up(self):
        cell = self.player_pers.current_position
        cell_owner = self.game_board.cells[cell].owner
        current_player = self.player_pers
        if self.game_board.cells[cell].level < 4 and self.cell_level_increased:
            if cell_owner == 'player' and Settings.turn_order != cell_owner:
                self.increase_cell_level(cell, current_player)
                self.cell_level_increased = False
        else:
            self.show_message('max lvl')

    def bot_lvl_up(self):
        cell = self.bot_pers.current_position
        cell_owner = self.game_board.cells[cell].owner
        current_player = self.bot_pers
        if self.game_board.cells[cell].level < 4:
            if cell_owner == 'bot' and Settings.turn_order == cell_owner:
                self.increase_cell_level(cell, current_player)

    def increase_cell_level(self, cell, model):
        cell_data = self.game_board.cells[cell]
        cell_data.level += 1
        cell_data.price = int(cell_data.level * cell_data.price * 1)
        cell_data.rent = int(cell_data.price * 0.1)
        model.wallet -= cell_data.lvl_up_price
        cell_data.update_lvl_up_price(cell_data.price)

    @staticmethod
    def enter_customs(model):
        print()
        tax_amount_list = [0.1, 0.2, 0.15, 0.05]
        tax_amount = random.choice(tax_amount_list)
        tax = tax_amount * model.wallet
        model.wallet -= tax

    def enter_court(self, model):
        verdicts = ['prison']
        chosen_verdict = random.choice(verdicts)
        match chosen_verdict:
            case 'prison':
                pass
                # self.enter_prison(model)
            case 'repay':
                self.repay_debts()

    @staticmethod
    def enter_prison(model):
        model.prison_status = True
        # время в тюрьме
        model.time_in_prison = random.randint(1, 3)
        model.move(new_coord=data.COORDINATES[1], new_position=12)

    def repay_debts(self):
        models = [self.player_pers, self.bot_pers]
        debtor = random.choice(models)
        creditor = random.choice(models)
        if debtor == creditor:
            print('dead heat')
        else:
            debtor.wallet -= 1000
            creditor.wallet += 1000

    def create_special_cards_list(self):
        cell_data = self.game_board.cells
        self.special_objects = [card for card in cell_data
                                if card.card_type == "special_object" and card.owner == None]

    def player_turn(self):
        self.take_turn('player')

    def end_turn(self):
        self.take_turn('bot')

    def show_message(self, text, color=data.WHITE, font_name=None, font_size=30):
        message = TextObject(450, 200, lambda: text, color, font_name, font_size)
        message.draw(self.game.main_window)
        pygame.display.update()