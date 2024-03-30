SCREEN_WIDTH = 1170
SCREEN_HEIGHT = 800

WHITE = (255,255,255)
RED = (255, 0, 0)
MAROON = (127, 0, 0)
BLACK = (0,0,0)

FPS = 60
SPEED = 3

COORDINATES = {
    1: (0, 0),
    2: (130, 0),
    3: (260, 0),
    4: (390, 0),
    5: (520, 0),
    6: (650, 0),
    7: (780, 0),
    8: (910, 0),
    9: (1040, 0),
    10: (0, 160),
    11: (130, 160),
    12: (260, 160),
    13: (390, 160),
    14: (520, 160),
    15: (650, 160),
    16: (780, 160),
    17: (910, 160),
    18: (1040, 160),
    19: (0, 320),
    20: (130, 320),
    21: (260, 320),
    22: (390, 320),
    23: (520, 320),
    24: (650, 320),
    25: (780, 320),
    26: (910, 320),
    27: (1040, 320),
    28: (0, 480),
    29: (130, 480),
    30: (260, 480),
    31: (390, 480),
    32: (520, 480),
    33: (650, 480),
    34: (780, 480),
    35: (910, 480),
    36: (1040, 480),
    37: (0, 640),
    38: (130, 640),
    39: (260, 640),
    40: (390, 640),
    41: (520, 640),
    42: (650, 640),
    43: (780, 640),
    44: (910, 640),
    45: (1040, 640),
}

MENU_IMAGE = 'C:\\Users\\User\Desktop\Monopoly\images\center.png'
START_CELL = 'C:\\Users\\User\Desktop\Monopoly\images\start1.png'
EVENT_CELL = 'C:\\Users\\User\Desktop\Monopoly\images\event.png'
MILK_FARM = 'C:\\Users\\User\Desktop\Monopoly\images\milk_farm'
FACTORY = 'C:\\Users\\User\Desktop\Monopoly\images\\factory'
PLAYER_MODEL_1 = 'C:\\Users\\User\Desktop\Monopoly\images\klip2.png'
PLAYER_MODEL_2 = 'C:\\Users\\User\Desktop\Monopoly\images\klipartz.com.png'
GRUNGLE = 'C:\\Users\\User\Desktop\Monopoly\images\grunge2.jpg'
CUSTOMS_HOUSE = 'C:\\Users\\User\Desktop\Monopoly\images\customs house.png'
PRISON = 'C:\\Users\\User\Desktop\Monopoly\images\prison.png'
COURT = 'C:\\Users\\User\Desktop\Monopoly\images\court.png'
HOTEL = 'C:\\Users\\User\Desktop\Monopoly\images\hotel'
SHIPPORT = 'C:\\Users\\User\Desktop\Monopoly\images\shipport'

cell_data = [
        {"images": START_CELL, "coord": COORDINATES[45], "title": "start",
        "card_type": "start", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": MILK_FARM, "coord": COORDINATES[44], "title": "milk_farm 1",
        "card_type": "farms", "price": 100, "rent": 10, 'owner': None},

        {"images": EVENT_CELL, "coord": COORDINATES[43], "title": "event",
        "card_type": "event", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": FACTORY, "coord": COORDINATES[42], "title": "factory",
        "card_type": "factory", "price": 100, "rent": 0, 'owner': None},

        {"images": FACTORY, "coord": COORDINATES[41], "title": "factory",
        "card_type": "factory", "price": 100, "rent": 0, 'owner': None},

        {"images": EVENT_CELL, "coord": COORDINATES[40], "title": "event",
         "card_type": "event", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": HOTEL, "coord": COORDINATES[39], "title": "hotel",
         "card_type": "hotel", "price": 100, "rent": 0, 'owner': None},

        {"images": SHIPPORT, "coord": COORDINATES[38], "title": "port",
         "card_type": "special_object", "price": 100, "rent": 0, 'owner': None},

        {"images": CUSTOMS_HOUSE, "coord": COORDINATES[37], "title": "customs_house",
         "card_type": "customs_house", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": HOTEL, "coord": COORDINATES[28], "title": "hotel",
         "card_type": "hotel", "price": 100, "rent": 0, 'owner': None},

        {"images": HOTEL, "coord": COORDINATES[19], "title": "hotel",
         "card_type": "hotel", "price": 100, "rent": 0, 'owner': None},

        {"images": SHIPPORT, "coord": COORDINATES[10], "title": "port",
         "card_type": "special_object", "price": 100, "rent": 0, 'owner': None},

        {"images": PRISON, "coord": COORDINATES[1], "title": "prison",
         "card_type": "prison", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": FACTORY, "coord": COORDINATES[2], "title": "factory",
        "card_type": "factory", "price": 100, "rent": 0, 'owner': None},

        {"images": EVENT_CELL, "coord": COORDINATES[3], "title": "event",
         "card_type": "event", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": FACTORY, "coord": COORDINATES[4], "title": "factory",
        "card_type": "factory", "price": 100, "rent": 0, 'owner': None},

        {"images": EVENT_CELL, "coord": COORDINATES[5], "title": "event",
         "card_type": "event", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": FACTORY, "coord": COORDINATES[6], "title": "factory",
        "card_type": "factory", "price": 100, "rent": 0, 'owner': None},

        {"images": EVENT_CELL, "coord": COORDINATES[7], "title": "event",
         "card_type": "event", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": SHIPPORT, "coord": COORDINATES[8], "title": "port",
         "card_type": "special_object", "price": 100, "rent": 0, 'owner': None},

        {"images": COURT, "coord": COORDINATES[9], "title": "court",
         "card_type": "court", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": MILK_FARM, "coord": COORDINATES[18], "title": "milk_farm 1",
         "card_type": "farms", "price": 100, "rent": 10, 'owner': None},

        {"images": EVENT_CELL, "coord": COORDINATES[27], "title": "event",
         "card_type": "event", "price": 0, "rent": 0, 'owner': 'game_master'},

        {"images": FACTORY, "coord": COORDINATES[36], "title": "factory",
         "card_type": "factory", "price": 100, "rent": 0, 'owner': None},
]