import pygame

import data



class BuildingCells:
    def __init__(self):
        self.width = data.SCREEN_WIDTH
        self.height = data.SCREEN_HEIGHT
        self.cell_size1 = 130
        self.cell_size2 = 160
        self.coord = {}
        self.font = pygame.font.Font(None, 15)

    def draw(self, surface):
        for x in range(0, self.width, self.cell_size1):
            for y in range(0, self.height, self.cell_size2):
                square_rect = pygame.Rect(x, y, self.cell_size1, self.cell_size2)
                pygame.draw.rect(surface, data.BLACK, square_rect, 1)
                square_number = (y // self.cell_size2) * (self.width // self.cell_size1) + (x // self.cell_size1) + 1
                square_text = self.font.render(str(f'{square_number}, {square_rect.topleft}'), True, data.BLACK)
                square_text_rect = square_text.get_rect(midbottom=square_rect.midbottom)
                surface.blit(square_text, square_text_rect)
                self.coord[square_number] = square_rect.topleft

    def wright(self):
        sorted_dict = dict(sorted(self.coord.items()))
        with open('4.txt', 'w') as file:
            for key, value in sorted_dict.items():
                file.write(f'{key}: {value},\n')