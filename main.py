# importing libraries
import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from tilemap import *



class Game:
    def __init__(self):
        # this method initialises the game window and creates attributes for the game
        pg.init()
        # window attributes
        self.width = WIDTH
        self.fps_temp = FPS
        self.width_temp = WIDTH
        self.height = HEIGHT
        self.height_temp = HEIGHT
        self.fps = FPS
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        # main game attributes
        self.running = True
        self.winner = None
        self.paused = False
        self.coins = 0
        self.font = pg.font.match_font(FONT_NAME)
        # loads files when the game is instantiated
        self.load_data()

    def load_data(self):
        # this method loads all files needed in the game from the game folder
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.button_font = path.join(img_folder, BUTTON_FONT)
        self.button_img = pg.image.load(path.join(img_folder, BUTTON_IMG)).convert_alpha()
        self.menu_img = pg.image.load(path.join(img_folder, MENU_BG_IMG)).convert_alpha()
        self.title_img = pg.image.load(path.join(img_folder, TITLE_IMG)).convert_alpha()
        self.button_hover_img = pg.image.load(path.join(img_folder, BUTTON_HOVER_IMG)).convert_alpha()
        self.button_click_img = pg.image.load(path.join(img_folder, BUTTON_CLICK_IMG)).convert_alpha()
        self.map = Map(path.join(game_folder, 'map.txt'))
        # creates a dim screen overlay for the pause menu
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

    def new(self):
        # this method starts a new game, instantiates sprites for every menus and creates groups for every sprite
        self.state = "Main menu"
        self.player_unit = ""
        self.computer_unit = ""
        # creates groups for all the sprites
        self.all_sprites = pg.sprite.Group()
        self.main_menu = pg.sprite.Group()
        self.pre_gameplay = pg.sprite.Group()
        self.post_gameplay = pg.sprite.Group()
        self.gameplay = pg.sprite.Group()
        self.help = pg.sprite.Group()
        self.settings = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.sliders = pg.sprite.Group()
        self.units = pg.sprite.Group()
        self.soldier = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        # instantiates all the menu backgrounds for all menus
        Menu_background(self, WIDTH / 2, HEIGHT / 2, self.main_menu)
        Menu_background(self, WIDTH / 2, HEIGHT / 2, self.help)
        Menu_background(self, WIDTH / 2, HEIGHT / 2, self.settings)
        Menu_background(self, WIDTH / 2, HEIGHT / 2, self.pre_gameplay)
        Menu_background(self, WIDTH / 2, HEIGHT / 2, self.post_gameplay)
        # instantiates the title for the main menu
        tite = Title(self, WIDTH / 2, HEIGHT / 6)
        # iterates through the button list to instantiate buttons for all menus
        for i, a in MAIN_MENU_BUTTONS:
            Button(self, a[0], a[1], i, self.main_menu)
        for i, a in PLAYER_UNIT_SELECTION_BUTTONS:
            Button(self, a[0], a[1], i, self.pre_gameplay, 5/7)
            if i == "play":
                self.actual_play_button = Button(self, a[0], a[1], i, self.pre_gameplay)
        for i, a in COMPUTER_UNIT_SELECTION_BUTTONS:
            Button(self, a[0], a[1], i, self.pre_gameplay, 5/7)
        # instantiates close buttons for all menus
        Button(self, CLOSE_BUTTON[1], CLOSE_BUTTON[2], CLOSE_BUTTON[0], self.settings)
        Button(self, CLOSE_BUTTON[1] + (WIDTH/4), CLOSE_BUTTON[2], CLOSE_BUTTON[0], self.pre_gameplay)
        Button(self, CLOSE_BUTTON[1], CLOSE_BUTTON[2], CLOSE_BUTTON[0], self.help)
        Button(self, CLOSE_BUTTON[1], CLOSE_BUTTON[2], CLOSE_BUTTON[0], self.post_gameplay)
        # iterates through the slider list to instantiate sliders and slider bar
        for i, a in SLIDERS:
            Bar(self, a[0], a[1], self.settings)
            bar = fill_bar(self, a[0], a[1], self.settings)
            Slider(self, a[0], a[1], i, self.settings, bar)
        # instantiates the camera and runs the game
        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def run(self):
        # this method runs the main game loop which checks for inputs, updates the sprites and renders them onto the screen
        self.playing = True
        while self.playing:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - this method updates sprites in a certain group depending on the state of the game
        if self.state == "Main menu":
            self.main_menu.update()
        if self.state == "settings":
            self.settings.update()
        if self.state == "pre gameplay":
            self.pre_gameplay.update()
        if self.state == "gameplay" and not self.paused:
            self.gameplay.update()
            self.camera.update(self.player)
        if self.state == "post gameplay":
            self.post_gameplay.update()
        if self.state == "help":
            self.help.update()

    def events(self):
        # Game Loop - this method checks for inputs from the keyboard and mouse and responds to those inputs
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # check for mouse release
            if event.type == pg.MOUSEBUTTONUP:
                # runs code when a button is clicked
                for button in self.buttons:
                    if button.clicked:
                        button.clicked = False
                        if button.text == "close":
                            if self.state != "post gameplay":
                                self.state = "Main menu"
                            # game is reset if the close button on the game over screen is selected
                            if self.state == "post gameplay":
                                main()
                        if button.text == "play" and button != self.actual_play_button:
                            self.state = "pre gameplay"
                        # checks if the button was instantiated using items in a certain list
                        if button.text == "sniper" and [button.text,(button.rect.centerx, button.rect.centery)] in PLAYER_UNIT_SELECTION_BUTTONS:
                            self.player_unit = "sniper"
                        if button.text == "sword" and [button.text,(button.rect.centerx, button.rect.centery)] in PLAYER_UNIT_SELECTION_BUTTONS:
                            self.player_unit = "sword"
                        if button.text == "warhammer" and [button.text,(button.rect.centerx, button.rect.centery)] in PLAYER_UNIT_SELECTION_BUTTONS:
                            self.player_unit = "warhammer"
                        if button.text == "RPG" and [button.text,(button.rect.centerx, button.rect.centery)] in PLAYER_UNIT_SELECTION_BUTTONS:
                            self.player_unit = "RPG"
                        if button.text == "sniper" and [button.text,(button.rect.centerx, button.rect.centery)] in COMPUTER_UNIT_SELECTION_BUTTONS:
                            self.computer_unit = "sniper"
                        if button.text == "sword" and [button.text,(button.rect.centerx, button.rect.centery)] in COMPUTER_UNIT_SELECTION_BUTTONS:
                            self.computer_unit = "sword"
                        if button.text == "warhammer" and [button.text,(button.rect.centerx, button.rect.centery)] in COMPUTER_UNIT_SELECTION_BUTTONS:
                            self.computer_unit = "warhammer"
                        if button.text == "RPG" and [button.text,(button.rect.centerx, button.rect.centery)] in COMPUTER_UNIT_SELECTION_BUTTONS:
                            self.computer_unit = "RPG"
                        if button == self.actual_play_button and self.player_unit != "" and self.computer_unit != "":
                            # loads the game and all sprites in it
                            self.state = "gameplay"
                            empty_spots = []
                            # gets every tile in the map and checks the value and position of the tile
                            for row, tiles in enumerate(self.map.data):
                                for col, tile in enumerate(tiles):
                                    if tile == "1":
                                        Wall(self, col*2, row*2)
                                    if tile == "P":
                                        self.player = Player(self, col*2, row*2,self.player_unit)
                                        # instantiates player soldiers with the player
                                        for i in range(1, ENEMY_COUNT):
                                            Player_Soldier(self, col*2 - (i*2), row*2)
                                    if tile == "C":
                                        self.main_computer = Main_Computer(self, col*2, row*2,self.computer_unit)
                                        # instantiates computer soldiers with the computer
                                        for i in range(1, ENEMY_COUNT):
                                            Computer_Soldier(self, col*2 + (i*2), row*2)
                                    if tile == "S":
                                        self.special_item = Special_Item(self, col*2, row*2)
                                    if tile == ".":
                                        # spawns treasure chests in a random empty spot
                                        empty_spots.append([col,row])
                                        chest_spawn = random.randint(1,100)
                                        if chest_spawn == 10:
                                            Treasure_Chest(self, col*2, row*2)
                            self.main_computer.move_to = empty_spots
                        if button.text == "settings":
                            self.state = "settings"
                        if button.text == "help":
                            self.state = "help"
                # changes the game settngs depending on which slider is clicked
                for slider in self.sliders:
                    if slider.clicked:
                        slider.clicked = False
                        if slider.constant == "WIDTH":
                            self.width = self.width_temp + int((slider.rect.centerx -slider.minimum)/BAR_WIDTH * self.width_temp)
                            self.screen = pg.display.set_mode((self.width, self.height))
                        if slider.constant == "HEIGHT":
                            self.height = self.height_temp + int((slider.rect.centerx -slider.minimum)/BAR_WIDTH * self.height_temp)
                            self.screen = pg.display.set_mode((self.width, self.height))
                        if slider.constant == "FPS":
                            self.fps = self.fps_temp + int((slider.rect.centerx -slider.minimum)/BAR_WIDTH * self.fps_temp)
            # allows the player to spend coins on upgrading or selecting units
            if event.type == pg.KEYDOWN:
                # pauses or unpauses the game when P is pressed
                if event.key == pg.K_p:
                    self.paused = not self.paused
                # increases the health of all units and spends 800 coins when U is pressed
                if event.key == pg.K_u and self.coins >= 1000:
                    self.coins -= 800
                    for unit in self.units:
                        if unit.team == "player team":
                            unit.health += 20
                # spawns a new player soldier and spends 200 coins when N is pressed
                if event.key == pg.K_n and self.coins >= 1000:
                    self.coins -= 200
                    Player_Soldier(self, self.player.start_pos[0]- TILESIZE*8, self.player.start_pos[1])
                    # random chance of spawning computer soldier when player soldier is spawned
                    spawn = random.choice(["spawn", "not spawn"])
                    if spawn == "spawn":
                        Computer_Soldier(self, self.main_computer.start_pos[0]- TILESIZE*8, self.main_computer.start_pos[1])
    
    def draw(self):
        # Game Loop - this method draws sprites and text onto the screen depending on the state
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # renders sprites and text depending on the state
        if self.state == "Main menu":
            self.screen.fill(CYAN)
            self.main_menu.draw(self.screen)
        elif self.state == "pre gameplay":
            self.screen.fill(CYAN)
            self.pre_gameplay.draw(self.screen)
            self.draw_text("Unit Selection Screen", self.button_font, 60, BLACK, WIDTH / 2, HEIGHT / 5)
        elif self.state == "settings":
            self.screen.fill(CYAN)
            self.settings.draw(self.screen)
            self.draw_text("Settings", self.button_font, 60, BLACK, WIDTH / 2, HEIGHT / 5)
            self.draw_text("Width of screen", self.font, 22, BLACK, int(WIDTH / 1.22), int(HEIGHT / 3))
            self.draw_text("Height of screen", self.font, 22, BLACK, int(WIDTH / 1.22), int(HEIGHT / 2))
            self.draw_text("FPS", self.font, 22, BLACK, int(WIDTH / 1.23), int(HEIGHT * 2/3))
        elif self.state == "help":
            self.screen.fill(CYAN)
            self.help.draw(self.screen)
            self.draw_text("Help", self.button_font, 60, BLACK, WIDTH / 2, HEIGHT / 5)
            self.draw_text("WASD or arrow keys to move.", self.font, 22, BLACK, WIDTH / 2, HEIGHT / 3)
            self.draw_text("G to attack.", self.font, 22, BLACK, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Left mouse clicks to select and move soldiers", self.font, 22, BLACK, WIDTH / 2, HEIGHT * 2/3)
        elif self.state == "gameplay":
            self.screen.fill(BLACK)
            for sprite in self.gameplay:
                # renders the camera onto the screen
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            # renders the coin count at the corner of the screen
            self.draw_text("Coins: {}".format(self.coins), self.font, 30, GOLD, WIDTH - 10, 10, align="topright")
            if self.coins >= 1000:
                # tells the player they can spend their coins when they reach 1000 coins
                self.draw_text("Press U to upgrade units and press N to spawn a new soldier", self.font, 20, GOLD, WIDTH/3, 10)
            for unit in self.units:
                if isinstance(unit, Player_Soldier):
                    if unit.highlight == True:
                        rect=unit.rect
                        rect.center = unit.rect.center
                        pg.draw.rect(self.screen, RED, rect, 3)
                    if unit.selected == True:
                        rect=unit.rect
                        rect.center = unit.rect.center
                        pg.draw.rect(self.screen, CYAN, rect, 3)
        elif self.state == "post gameplay":
            self.screen.fill(CYAN)
            self.post_gameplay.draw(self.screen)
            self.draw_text("Game Over", self.button_font, 60, BLACK, WIDTH / 2, HEIGHT / 5)
            self.draw_text("Winner: {}".format(self.winner), self.font, 22, BLACK, WIDTH / 2, HEIGHT / 3)
            self.draw_text("Coin count: {}".format(self.coins), self.font, 22, BLACK, WIDTH / 2, HEIGHT / 2)
        # renders the dim screen and paused text if the game is paused
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, font_name, size, color, x, y, align="center"):
        # this method draws text on the screen
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)



# this is where the main game loop is run
def main():
    g = Game()
    while g.running:
        g.new()
    pg.quit()
main()
