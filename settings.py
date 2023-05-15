GAME_NAME = "Heroes Adventure"

GRAPHICS_PATH = "./graphics"
AUDIO_PATH = "./audio"
ICON_PATH = GRAPHICS_PATH + "/icon/icon.png"
# HERO SETTINGS
HERO_COL = "394"
# HERO_NAME = "Archangel"
HERO_NAME = "Knight"
HERO_IMAGES_PATH = GRAPHICS_PATH + "/hero/" + HERO_NAME

WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 32

START_POSITION = (2000, 1430)

HITBOX_OFFSET = {"hero": -20, "object": -40, "grass": -10, "invisible": 0}

MAX_STATS = {
    "Archangel": {
        "attack": 100,
        "defence": 100,
        "spellpower": 100,
        "knowledge": 100,
    },
    "Knight": {
        "attack": 100,
        "defence": 100,
        "spellpower": 100,
        "knowledge": 100,
    },
}


STATS = {
    "Archangel": {
        "health": 100,
        "attack": 20,
        "defence": 20,
        "damage": 50,
        "speed": 10,
        "energy": 100,
        "spellpower": 1,
        "knowledge": 5,
    },
    "Knight": {
        "health": 100,
        "attack": 20,
        "defence": 20,
        "damage": 50,
        "speed": 10,
        "energy": 100,
        "spellpower": 1,
        "knowledge": 5,
    },
}

# spells
spell_data = {
    "magic_arrow": {
        "cost": 10,
        "strength": 35,
        "factor": 5,
        "graphic": GRAPHICS_PATH + "/spells/magic_arrow/magic_arrow.png",
    },
    "cure": {
        "cost": 10,
        "strength": 10,
        "factor": 2,
        "graphic": GRAPHICS_PATH + "/spells/cure/cure.png",
    },
}


# enemies

monster_data = {
    "imp": {
        "health": 15,
        "damage": 1,
        "speed": 4,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "familiar": {
        "health": 100,
        "damage": 2,
        "speed": 2,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 400,
    },
    "pit_lord": {
        "health": 20,
        "damage": 2,
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "efreet_sultan": {
        "health": 20,
        "damage": 2,
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "horned_demon": {
        "health": 20,
        "damage": 2,
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
}

# monster_names = {
#     "390": "familiar",
#     "391": "horned_demon",
#     "392": "pit_lord",
#     "393": "efreet_sultan",
# }

monster_names = {
    "0": "familiar",
    "391": "familiar",
    "392": "familiar",
    "393": "familiar",
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 70
UI_FONT = GRAPHICS_PATH + "/font/joystix.ttf"
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
UI_BORDER_COLOR_LACK = "red"
TEXT_COLOR = "#EEEEEE"

# ui colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"
