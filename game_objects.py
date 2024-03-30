import pygame
import data
import main_menu
import utils

from text_object import TextObject

banner = pygame.image.load(data.GRUNGLE)



class GameCard(pygame.sprite.Sprite):
    def __init__(self, images, coord, number, title, card_type, price, rent, owner, banner):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.banner = banner
        self.price = price
        self.rent = price * 0.1
        self.card_type = card_type
        self.title = title
        self.location = coord
        self.owner = owner
        self.number = number
        self.level = 0
        self.assets = utils.get_building_lvl(direct=images)
        self.image1 = pygame.image.load(self.assets)
        self.image = pygame.transform.scale(self.image1, (130, 160))
        self.rect = self.image.get_rect(topleft=self.location)
        self.check_lvl = self.level
        self.lvl_up_price = price * 0.1
        self.font = pygame.font.Font(None, 36)

    def update(self, new_level) -> None:
        try:
            if self.level >= self.check_lvl:
                self.assets = utils.get_building_lvl(direct=self.images, index=new_level)
                self.image = pygame.image.load(self.assets)
                self.check_lvl = self.level
        except (TypeError, FileNotFoundError):
            pass

    def handle_mouse_event(self, event_type, pos, main_window, card, player):
        if event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos, main_window, card, player)

    def handle_mouse_down(self, pos, main_window, card, player):
        if self.rect.collidepoint(pos):
            self.show_info(main_window, card, player)

    def update_lvl_up_price(self, new_price):
        self.lvl_up_price = int(new_price * 0.2 * self.level)

    def show_info(self, main_window, card, player):

        def sell_commerce():
            if card.owner == 'player':
                print('test func')
                index_to_remove = player.real_estate.index(card.title)
                player.real_estate.pop(index_to_remove)
                player.wallet += card.price * 0.5
                card.owner = None

        def pay_a_fine():
            if card.card_type == 'prison':
                print('check pay')
                player.wallet -= 1000
                player.prison_status = False

        self.sell_button = main_menu.Button(105, 96, 40, 40, text='Sell', command=sell_commerce)
        self.pay_fine_button = main_menu.Button(105, 96, 40, 40, text='Pay', command=pay_a_fine)

        info_text = [
            f"Title: {card.title}",
            f"Price: {card.price} Rent: {card.rent}",
            f"Owner: {card.owner}",
            f"Level: {card.level}",
        ]

        if card.level < 4:
            info_text.append(f"Lvl ip price: {card.lvl_up_price}")

        info_font = pygame.font.Font(None, 28)
        text_height = info_font.get_height()

        banner = self.banner.copy()
        banner_copy = pygame.transform.scale(banner, (250, 140))

        banner_draw = pygame.Surface(banner_copy.get_size())
        banner_draw.blit(banner_copy, (0, 0))

        for i, line in enumerate(info_text):
            text_surface = info_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft=(10, i * text_height))
            banner_draw.blit(text_surface, text_rect)

        if card.owner == 'player':
            self.sell_button.draw(banner_draw)

        if card.card_type == 'prison' and player.prison_status:
            self.pay_fine_button.draw(banner_draw)

        main_window.blit(banner_draw, (450, 485))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    if utils.find_object(obj=self.sell_button.borders, mouse_pos=click_pos, surface=(450, 485)):
                        sell_commerce()
                        pay_a_fine()
                        waiting_for_input = False
                    else:
                        waiting_for_input = False



class GameBoard:
    def __init__(self):
        self.cells = []
        self.cards_sprites = pygame.sprite.Group()
        self.cell_num = 0
        self.add_cards()

    def add_cards(self):
        for cell_info in data.cell_data:
            cell = GameCard(banner=banner, number=self.cell_num, **cell_info)
            self.cell_num += 1
            self.cells.append(cell)
            self.cards_sprites.add(cell)



class PlayerModel(pygame.sprite.Sprite):
    def __init__(self, image, coord, card_type, money):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft=coord)
        self.card_type = card_type
        self.wallet = int(money)
        self.current_position = 0
        self.prison_status = False
        self.time_in_prison = 0
        self.real_estate = []

    def move(self, new_coord, new_position):
        self.rect.topleft = new_coord
        self.current_position = new_position



class InfoPanel:
    def __init__(self, x, y, w, h, image_path, model=None, turn=None):
        self.image = pygame.image.load(image_path)
        self.model = model
        self.set = turn
        self.pos = x, y
        self.w_h = w, h

    def draw(self, surface):

        if self.model:
            info_text = [
                '',
                f'{self.model.card_type}',
                f"Money: {self.model.wallet}",
                "Real estate:",
            ]
            for x in self.model.real_estate:
                info_text.append(x)
        elif self.set:
            info_text = [f'Next move:', self.set.turn_order]

        info_font = pygame.font.Font(None, 23)
        text_color = (0, 0, 0)

        image_copy1 = self.image.copy()
        image_copy = pygame.transform.scale(image_copy1, self.w_h)

        image_draw = pygame.Surface(image_copy.get_size())
        image_draw.blit(image_copy, (0, 0))

        text_height = info_font.get_height()

        for i, line in enumerate(info_text):
            text_surface = info_font.render(line, True, text_color)
            text_rect = text_surface.get_rect(topleft=(10, i * text_height))
            image_draw.blit(text_surface, text_rect)

        surface.blit(image_draw, self.pos)



class Auction:
    def __init__(self, x, y, image_path):
        self.x, self.y = x, y
        self.image = pygame.image.load(image_path)
        self.refuse_button = main_menu.Button(105, 150, 80, 40, text='Refuse', command=self.refuse)
        self.increase_button = main_menu.Button(185, 40, 40, 40, text='+', command=self.increase_the_rate)
        self.decrease_button = main_menu.Button(75, 40, 40, 40, text='-', command=self.decrease_the_rate)
        self.should_draw = True

    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEBUTTONDOWN:
                if utils.find_object(obj=self.refuse_button.borders, mouse_pos=pos, surface=(425, 420)):
                    self.refuse_button.command()
                    self.should_draw = False
                if utils.find_object(obj=self.increase_button.borders, mouse_pos=pos, surface=(425, 420)):
                    self.increase_button.command()
                if utils.find_object(obj=self.decrease_button.borders, mouse_pos=pos, surface=(425, 420)):
                    self.decrease_button.command()

    def refuse(self):
        print('refuse')
        self.should_draw = False

    def increase_the_rate(self):
        print('+')

    def decrease_the_rate(self):
        print('-')

    def draw(self, surface):
        if not self.should_draw:
            return

        image_copy = self.image.copy()
        new_image = pygame.transform.scale(image_copy, (300, 200))

        self.increase_button.draw(new_image)
        self.decrease_button.draw(new_image)
        self.refuse_button.draw(new_image)

        surface.blit(new_image, (self.x, self.y))