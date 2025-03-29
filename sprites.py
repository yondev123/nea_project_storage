# importing libraries
import pygame as pg
import math
import random
from settings import *
from collections import deque
vec = pg.math.Vector2

            
class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, text, group, scale = 1):
        # this method initialises the button as an image of a button in the group buttons
        self.groups = group, game.buttons
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.scale = scale
        self.image = self.load_img(self.game.button_img, self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.text = text
        self.clicked = False

    def button_func(self):
        # this method changes the button image when mouse is hovering over/clicking the button
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not(pg.mouse.get_pressed()[0]):
            self.image = self.load_img(self.game.button_hover_img, self.scale)
        elif self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            self.image = self.load_img(self.game.button_click_img, self.scale)
            self.clicked = True
        else:
            self.image = self.load_img(self.game.button_img, self.scale)

    def load_img(self, image, scale):
        # this method scales the image and removes the white background
        image = pg.transform.scale(image, (int(BUTTON_WIDTH * scale), int(BUTTON_HEIGHT * scale)))
        image.set_colorkey(WHITE)
        return image

    def draw_button_text(self, screen,  text, font_name, size, color):
        # this method draws the text onto the button and puts the text at the centre of the button
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        screen.image.blit(text_surface, (screen.rect.width/2+(int(BUTTON_TEXT_X_OFFSET*self.scale)/4)*len(text), screen.rect.height/2 + int(BUTTON_TEXT_Y_OFFSET*self.scale)))

    def update(self):
        # this method updates the button by rendering text onto it and giving it functionality
        self.button_func()
        self.draw_button_text(self, self.text, self.game.button_font, int(BUTTON_TEXT_SIZE * self.scale), BLACK)


class Slider(pg.sprite.Sprite):
    def __init__(self, game, x, y, constant, group, fill_bar):
        # this method initialises the slider as a circular button image in the group sliders
        self.groups = group, game.sliders
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.constant = constant
        self.fill_bar = fill_bar
        self.fill_bar.slider = self
        self.fill_bar.sliding = True
        self.image = self.load_img(self.game.button_img)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.minimum = ""
        self.temp = self.rect.centerx
        self.clicked = False

    def slider_func(self):
        # this method changes the slider image when mouse is hovering over/clicking the slider and when the mouse is being moved
        mouse_pos = pg.mouse.get_pos()
        # checks if the mouse is hovering over the button
        if self.rect.collidepoint(mouse_pos) and not(pg.mouse.get_pressed()[0]):
            self.image = self.load_img(self.game.button_hover_img)
        # checks if the mouse is clicking the button
        elif self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:
            self.image = self.load_img(self.game.button_click_img)
            self.clicked = True
            x, y = pg.mouse.get_pos()
            # limits the position of the x and y position of the slider
            maximum = int(self.temp + BAR_WIDTH/2)
            self.minimum = int(self.temp - BAR_WIDTH / 2)
            self.rect.centerx = min(max(self.minimum, x), maximum)
        else:
            self.image = self.load_img(self.game.button_img)

    def load_img(self, image):
        # this method scales the image and removes the white background
        image = pg.transform.scale(image, (SLIDER_LENGTH, SLIDER_LENGTH))
        image.set_colorkey(WHITE)
        return image


    def update(self):
        # this method updates the slider by giving it functionality
        self.slider_func()


class fill_bar(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        # this method initialises the fill bar as a blue rectangle
        self.groups = group
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.sliding = False
        self.slider = None
        self.image = pg.Surface((BAR_WIDTH, BAR_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.image.fill(CYAN)
        self.rect.center = (x, y)

    def update(self):
        # this method updates the fill bar by moving the fill bar with the slider
        if self.sliding:
            #changes the length and position of the fill bar depending on where the slider is
            self.image = pg.Surface((BAR_WIDTH/2 - (self.slider.temp - self.slider.rect.centerx), BAR_HEIGHT))
            self.image.fill(CYAN)
            self.rect.width = self.image.get_width()
            self.rect.centerx = (self.slider.rect.centerx + self.rect.left)/2


class Bar(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        # this method initialises the slider bar as a white rectangle
        self.groups = group
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = pg.Surface((BAR_WIDTH, BAR_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Menu_background(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        # this method initialises the menu background as an image of a menu background
        self.groups = group
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = game.menu_img
        self.image = pg.transform.scale(self.image, (MENU_BG_WIDTH, MENU_BG_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Title(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # this method initialises the title as an image of the title
        self.groups = game.main_menu
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = game.title_img
        self.image = pg.transform.scale(self.image, (TITLE_WIDTH, TITLE_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # thie method initilises the wall as a dark grey square in the group walls
        self.groups = game.gameplay, game.walls
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = pg.Surface((TILESIZE*2, TILESIZE*2))
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect()
        self.rect.center = (x*TILESIZE, y*TILESIZE)


class Special_Item(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # this method initilises the special item as a light grey square 
        self.groups = game.gameplay
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.center = (x*TILESIZE, y*TILESIZE)

    def update(self):
        # this method updates the special item by checking if it collides with a unit
        hits = pg.sprite.spritecollide(self, self.game.units, False)
        # destroys the item if a unit touches it and changes bool to carrying
        if hits:
            hits[0].carrying_item = True
            self.kill()
            

class Treasure_Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # this method initilises the treasure chest as a brown square
        self.groups = game.gameplay
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x*TILESIZE, y*TILESIZE)

    def update(self):
        # the method updates the treasure chest by checking if it colldies with a unit of the player team
        hits = pg.sprite.spritecollide(self, self.game.units, False)
        if hits and hits[0].team == "player team":
            # gives the player coins if they touch a treasure chest
            self.kill()
            self.game.coins += 200

class Unit(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # this method initialises a unit as a square surface in the group units
        self.groups = game.gameplay, game.units
        self.game = game
        self.health = ""
        self.team = ""
        self.speed = ""
        self.direction = "left"
        self.last_attack = 0
        self.carrying_item = False
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        # soldier units are 3/4 the size of a main unit
        if isinstance(self, Player_Soldier) or isinstance(self, Computer_Soldier) :
            self.image = pg.Surface((TILESIZE*(3/4), TILESIZE*(3/4)))
        else:
            self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x*TILESIZE, y*TILESIZE)
        self.graph = self.game.map
        self.path = None
        self.coord_path = None
        self.stop_unit = True
        self.stop_coord = True
        self.new_path = False
        self.node = None
        counter = 0

    def delta_time_speed(self, speed_value):
        # this method multiples delta time by speed to make the speed inversely proportional to the frame rate
        value = speed_value
        value = float(value)
        value *= self.game.delta_time
        value = round(value)
        self.speed = value


    def attack(self, unit_type):
        # this method gives the different types of units unique attacks
        if not self.carrying_item:
            if unit_type == "sniper":
                self.sniper_attack()
            if unit_type == "RPG":
                self.RPG_attack()
            if unit_type == "sword":
                self.sword_attack()
            if unit_type == "warhammer":
                self.warhammer_attack()


    def move(self, direction):
        # this method moves the Unit in a the direction specified and checks for collisions between units and walls
        if direction == "left":
            self.direction = "left"
            self.rect.centerx -= self.speed
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for unit in self.game.units:
                if unit != self:
                    hits2 =  pg.sprite.collide_rect(self, unit)
                    if hits2 == True:
                        break
            # if the unit collides with a wall or unit, then they move right until they aren't
            if hits or hits2:
                self.rect.centerx += self.speed
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                for unit in self.game.units:
                    if unit != self:
                        hits2 =  pg.sprite.collide_rect(self, unit)
                        if hits2 == True:
                            break
        if direction == "right":
            self.direction = "right"
            self.rect.centerx += self.speed
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for unit in self.game.units:
                if unit != self:
                    hits2 =  pg.sprite.collide_rect(self, unit)
                    if hits2 == True:
                        break
            # if the unit collides with a wall or unit, then they move left until they aren't
            if hits or hits2:
                self.rect.centerx -= self.speed
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                for unit in self.game.units:
                    if unit != self:
                        hits2 =  pg.sprite.collide_rect(self, unit)
                        if hits2 == True:
                            break
        if direction == "up":
            self.direction = "up"
            self.rect.centery -= self.speed
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for unit in self.game.units:
                if unit != self:
                    hits2 =  pg.sprite.collide_rect(self, unit)
                    if hits2 == True:
                        break
            # if the unit collides with a wall or unit, then they move down until they aren't
            if hits or hits2:
                self.rect.centery += self.speed
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                for unit in self.game.units:
                    if unit != self:
                        hits2 =  pg.sprite.collide_rect(self, unit)
                        if hits2 == True:
                            break
        if direction == "down":
            self.direction = "down"
            self.rect.centery += self.speed
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            for unit in self.game.units:
                if unit != self:
                    hits2 =  pg.sprite.collide_rect(self, unit)
                    if hits2 == True:
                        break
            # if the unit collides with a wall or unit, then they move up until they aren't
            if hits or hits2:
                self.rect.centery -= self.speed
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                for unit in self.game.units:
                    if unit != self:
                        hits2 =  pg.sprite.collide_rect(self, unit)
                        if hits2 == True:
                            break

    def sniper_attack(self):
        # this method fires a sniper bullet at a certain rate
        now = pg.time.get_ticks()
        if now - self.last_attack > SNIPER_RATE:
            self.last_attack = now
            Bullet(self.rect.centerx, self.rect.centery, self.game, self.direction, self)

    def RPG_attack(self):
        # this method fires an explosive bullet at a certain rate
        now = pg.time.get_ticks()
        if now - self.last_attack > RPG_RATE:
            self.last_attack = now
            Bullet(self.rect.centerx, self.rect.centery, self.game, self.direction, self)

    def sword_attack(self):
        # this method deals damage to any unit within range
        now = pg.time.get_ticks()
        if now - self.last_attack > SWORD_RATE:
            self.last_attack = now
            sword_rect = pg.Rect(self.rect.centerx+10, self.rect.centery, self.rect.width, self.rect.height)
            for unit in self.game.units:
                if sword_rect.colliderect(unit.rect) and unit.team != self.team:
                    unit.health -= SWORD_DAMAGE

    def warhammer_attack(self):
        # this method deals more damage to any unit within range
        now = pg.time.get_ticks()
        if now - self.last_attack > WARHAMMER_RATE:
            self.last_attack = now
            warhammer_rect = pg.Rect(self.rect.centerx+10, self.rect.centery, self.rect.width+5, self.rect.height)
            for unit in self.game.units:
                if warhammer_rect.colliderect(unit.rect) and unit.team != self.team:
                    unit.health -= WARHAMMER_DAMAGE

    def check_health(self):
        # this method checks the health of a unit, draws a health bar and kills the unit if they lose their health
        if self.health > self.full_health/100*60:
            col = GREEN
        elif self.health > self.full_health/100*30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / self.full_health)
        self.health_bar = pg.Rect(0, 10, width, 7)
        if self.health < self.full_health:
            pg.draw.rect(self.image, col, self.health_bar)
        # klls the unit if they lose all their health
        if self.health <= 0:
            if not self.game.player and not self.game.main_computer:
                self.kill()
                if self.team == "computer team":
                    self.game.coins += 20
            else:
                # respawns the unit if they are player or main computer unit
                start_pos = self.start_pos
                self.kill()
                if self.team == "player team":
                    self.game.player = Player(self.game, start_pos[0], start_pos[1], self.game.player_unit)
                if self.team == "computer team":
                    self.game.main_computer = Main_Computer(self.game, start_pos[0], start_pos[1], self.game.computer_unit)
                    self.game.coins += 40
            self.carrying_item = False

    def vec2int(self, v):
        # this method converts vectors to tuples with integers
        return (int(v.x), int(v.y))

    def breadth_first_search(self, graph, start):
        # this method does a breadth first search from a specified vector using a queue
        frontier = deque()
        frontier.append(start)
        path = {}
        path[self.vec2int(start)] = None
        while len(frontier) > 0:
            current = frontier.popleft()
            for next in graph.find_neighbors(current):
                if self.vec2int(next) not in path:
                    frontier.append(next)
                    path[self.vec2int(next)] = current - next
        return path

    def add_walls(self):
        # this method adds the wall nodes to the graph
        for wall in self.game.walls:
            wall_vec = vec(wall.rect.centerx / TILESIZE /2, wall.rect.centery / TILESIZE / 2)
            self.graph.walls.append(wall_vec)

    def search_unit(self, unit):
        # this method does a breadth first search from a unit
        unit_vec = vec(unit.rect.centerx / TILESIZE / 2, unit.rect.centery / TILESIZE / 2)
        path = self.breadth_first_search(self.graph, unit_vec)
        return path

    def move_to_unit(self, unit):
        # this method moves the unit object to the unit specified using breadth first search
        unit.path_finding()
        # the center left of the unit is converted into a node if the player is moving left
        if self.direction == "left":
            node = (round((self.rect.centerx+(TILESIZE/2))/TILESIZE/2), round(self.rect.centery/TILESIZE/2))
        # the center right of the player is converted into a node if the player is moving right
        if self.direction == "right":
            node = (round((self.rect.centerx-(TILESIZE/2))/TILESIZE/2), round(self.rect.centery/TILESIZE/2))
        # the center top of the player is converted into a node if the player is moving up
        if self.direction == "up":
            node = (round(self.rect.centerx/TILESIZE/2), round((self.rect.centery+(TILESIZE/2))/TILESIZE/2))
        # the center bottom of the player is converted into a node if the player is moving down
        if self.direction == "down":
            node = (round(self.rect.centerx/TILESIZE/2), round((self.rect.centery-(TILESIZE/2))/TILESIZE/2))
        # if there is a path to a unit, then the value of the node key in the path dictionary is used to determine the direction the player moves
        if unit.path != None:
            self.node = node
            dir = unit.path[node]
            if dir:
                if dir.x == 1:
                    self.move("right")
                if dir.x == -1:
                    self.move("left")
                if dir.y == -1:
                    self.move("up")
                if dir.y == 1:
                    self.move("down")

    def move_to_coord(self,node_vec):
        # this method moves the unit object to the position specified using breadth first search
        if len(self.game.walls) == 944 and self.stop_coord == True:
            self.add_walls()
            self.coord_path = self.breadth_first_search(self.graph, node_vec)
            self.stop_coord = False
        # same code as move_to_unit method with node_vec and coord_path instead of node and path
        if self.direction == "left":
            node = (round((self.rect.centerx+(TILESIZE/2))/TILESIZE/2), round(self.rect.centery/TILESIZE/2))
        if self.direction == "right":
            node = (round((self.rect.centerx-(TILESIZE/2))/TILESIZE/2), round(self.rect.centery/TILESIZE/2))
        if self.direction == "up":
            node = (round(self.rect.centerx/TILESIZE/2), round((self.rect.centery+(TILESIZE/2))/TILESIZE/2))
        if self.direction == "down":
            node = (round(self.rect.centerx/TILESIZE/2), round((self.rect.centery-(TILESIZE/2))/TILESIZE/2))
        if self.coord_path != None:
            self.node_vec = node
            dir = self.coord_path[node]
            if dir:
                if dir.x == 1:
                    self.move("right")
                if dir.x == -1:
                    self.move("left")
                if dir.y == -1:
                    self.move("up")
                if dir.y == 1:
                    self.move("down")
            # reassigns the position the main computer moves to if they have reached the coordinate
            elif isinstance(self, Main_Computer):
                self.stop_random = True
                self.stop_coord = True
            # ends soldier movement to if they have reached the coordinate
            elif (isinstance(self, Player_Soldier)):
                self.stop_coord = True
                self.selected = False
                self.is_clicked = False

    def update_path(self):
        # this method creates a new path to a unit when the unit moves
        if self.direction == "left":
            node = (round((self.rect.centerx+(TILESIZE/2))/TILESIZE/2), round(self.rect.centery/TILESIZE/2))
        if self.direction == "right":
            node = (round((self.rect.centerx-(TILESIZE/2))/TILESIZE/2), round(self.rect.centery/TILESIZE/2))
        if self.direction == "up":
            node = (round(self.rect.centerx/TILESIZE/2), round((self.rect.centery+(TILESIZE/2))/TILESIZE/2))
        if self.direction == "down":
            node = (round(self.rect.centerx/TILESIZE/2), round((self.rect.centery-(TILESIZE/2))/TILESIZE/2))
        # if there is a path and the current node is not the same as the old node then a new path is created
        if self.path != None:
            if node != self.node:
                self.node = node
                self.path = self.breadth_first_search(self.graph, vec(node))
                        
    def AI_attack(self):
        # this method makes Computer controlled units attack a unit of the opposite team when they are close enough
        for unit in self.game.units:
            if unit.team != self.team:
                if math.hypot(unit.rect.centerx-self.rect.centerx, unit.rect.centery-self.rect.centery) < TILESIZE * 2:
                    if self.selected_unit == "sniper" or self.selected_unit == "RPG":
                        self.attack(self.selected_unit)
                if math.hypot(unit.rect.centerx-self.rect.centerx, unit.rect.centery-self.rect.centery) < TILESIZE:
                    if self.selected_unit == "sword" or self.selected_unit == "warhammer":
                        self.attack(self.selected_unit)

    def soldier_selected(self, mouse_pos):
        # this method moves a soldier to the mouse position when they are selected
        mouse_pos_node = vec(round(mouse_pos[0]/TILESIZE/2), round(mouse_pos[1]/TILESIZE/2))
        self.move_to_coord(mouse_pos_node)

    def check_win(self):
        # this method checks if either team has satisfied the win condition and if so changes the state to post gameplay with that team as the winner
        if self.carrying_item == True:
            if self.team == "computer team" and self.rect.collidepoint(self.game.player.start_pos):
                self.game.winner = "computer team"
                self.game.state = "post gameplay"
            if self.team == "player team" and self.rect.collidepoint(self.game.main_computer.start_pos):
                self.game.winner = "player team"
                self.game.state = "post gameplay"
                
    def path_finding(self):
        # this method produces a path to a unit and updates that path
        if len(self.game.walls) == 944 and self.stop_unit == False:
            self.update_path()
        if len(self.game.walls) == 944 and self.stop_unit == True:
            self.add_walls()
            self.path = self.search_unit(self)
            self.stop_unit = False
    
            
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, game, direction, unit):
        # this method instantiates the bullet as a yellow square in the group bullets
        self.game = game
        self.unit = unit
        self.direction = direction
        self.groups = game.gameplay, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups, self.game.all_sprites)
        self.image = pg.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = BULLET_SPEED

    def update(self):
        # this method updates the bullet by moving the bullet in a certain direction and checking for collisions into walls or units
        if self.direction == "left": 
            self.rect.x -= self.speed
        if self.direction == "right": 
            self.rect.x += self.speed
        if self.direction == "down":
            self.rect.y += self.speed
        if self.direction == "up": 
            self.rect.y -= self.speed
        # destroys the bullet if it hits a wall
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.kill()
        # deals damage to a unit it hits a unit
        hits2 = pg.sprite.spritecollide(self, self.game.units, False)
        if hits2 and hits2[0].team != self.unit.team:
            # deals damage only to that unit if it is a sniper bullet
            if self.unit.selected_unit == "sniper":
                hits2[0].health -= SNIPER_DAMAGE
            # does damage to any unit close to it if it is from an RPG
            if self.unit.selected_unit == "RPG":
                for unit in self.game.units:
                    if unit.team != self.unit.team and math.hypot(hits2[0].rect.centerx-unit.rect.centerx, hits2[0].rect.centery-unit.rect.centery) < RPG_RADIUS:
                        unit.health -= EXPLOSION_DAMAGE
            self.kill()


class Player(Unit):
    def __init__(self, game, x, y, selected_unit):
        # this methood initialises the player unit as a square with its colour depending on what unit was selected
        self.selected_unit = selected_unit
        super().__init__(game, x, y)
        self.team = "player team"
        self.speed = PLAYER_SPEED
        self.health = 100
        self.start_pos = self.rect.center
        self.full_health = self.health
        # changes the units colour depending on the unit selected in the unit selection menu
        if self.selected_unit == "sword":
            self.image.fill(GREEN)
        if self.selected_unit == "warhammer":
            self.image.fill(RED)
        if self.selected_unit == "RPG":
            self.image.fill(CYAN)
        if self.selected_unit == "sniper":
            self.image.fill(YELLOW)

    def update(self):
        # this method updates the player by moving the player if WASD or arrow keys are pressed and attacking if the g key is pressed
        self.check_health()
        self.delta_time_speed(PLAYER_SPEED)
        self.check_win()
        # moves the player depending on what key was pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.move("left")
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.move("right")
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.move("up")
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.move("down")
        if keys[pg.K_g]:
            self.attack(self.selected_unit)


class Main_Computer(Unit):
    def __init__(self, game, x, y, selected_unit):
        # this method initilises the main computer unit as a square with its colour depending on what unit was selected
        self.selected_unit = selected_unit
        super().__init__(game, x, y)
        self.team = "computer team"
        self.speed = COMPUTER_SPEED
        self.health = 100
        self.start_pos = self.rect.center
        self.full_health = self.health
        self.state = "wandering"
        self.move_to = []
        self.stop_random = True
        self.node_vec = None
        # changes the units colour depending on the unit selected in the unit selection menu
        if self.selected_unit == "sword":
            self.image.fill(GREEN)
        if self.selected_unit == "warhammer":
            self.image.fill(RED)
        if self.selected_unit == "RPG":
            self.image.fill(CYAN)
        if self.selected_unit == "sniper":
            self.image.fill(YELLOW)

    def update(self):
        # this method updates the main computer by changing its state and attacking units of the other team that get close enough
        self.AI_states()
        self.delta_time_speed(COMPUTER_SPEED)
        self.check_health()
        self.AI_attack()

    def AI_states(self):
        # this method changes the state that the unit is in depending on if they are near the player or carrying an item
        for unit in self.game.units:
            if unit.team != self.team:
                if math.hypot(unit.rect.centerx-self.rect.centerx, unit.rect.centery-self.rect.centery) < TILESIZE * 4:
                    self.state = "hunting"
            if unit.team == self.team:
                if unit.carrying_item == True:
                    self.state = "escaping"
        if self.state == "wandering":
            # makes the unit move to random positions
            if self.stop_random == True:
                self.node_vec = random.choice(self.move_to)
                self.stop_random = False
            self.node_vec = vec(self.node_vec[0], self.node_vec[1])
            self.move_to_coord(self.node_vec)
        if self.state == "hunting":
            # makes the unit chase the player
            self.move_to_unit(self.game.player)
        if self.state == "escaping":
            # makes the unit try to win the game
            start_node = vec(round(self.game.player.start_pos[0]/TILESIZE/2), round(self.game.player.start_pos[1]/TILESIZE/2))
            self.move_to_coord(start_node)


class Player_Soldier(Unit):
    def __init__(self, game, x, y):
        # this method initilaises the player soldier as a white square
        super().__init__(game, x, y)
        self.team = "player team"
        self.selected_unit = "sword"
        self.selected = False
        self.image.fill(WHITE)
        self.health = 500
        self.full_health = self.health
        self.start_pos = self.rect.center
        self.speed = SOLDIER_SPEED
        self.old_pos = 0
        self.last_move = 0
        self.highlight = False
        self.is_clicked = False

    def update(self):
        # this method updates the player soldier by following the player and checking if it is selected
        self.check_health()
        self.AI_attack()
        self.delta_time_speed(SOLDIER_SPEED)
        self.check_selection()
        self.check_win()
        # moves the unit in the maze and then pathfinds
        if self.rect.centerx < 0:
            now = pg.time.get_ticks()
            if now - self.last_move > 100:
                self.last_move = now
                self.move("right")
        elif self.selected == False:
                self.move_to_unit(self.game.player)

    def check_selection(self):
        # this method checks if the soldier has been clicked by the mouse and then moves it after the second mouse click
        mouse_pos = pg.mouse.get_pos()
        if self.selected == False:
            if self.rect.collidepoint(mouse_pos):
                self.highlight = True
                if pg.mouse.get_pressed()[0]:
                    print("selected")
                    self.selected = True
                    self.old_pos = mouse_pos
            else:
                self.highlight = False
        # moves the selected unit to the next clicked position
        if self.selected == True:
            if pg.mouse.get_pressed()[0] and mouse_pos != self.old_pos:
                print("clicked")
                self.is_clicked = True
            if self.is_clicked == True:
                self.old_pos = mouse_pos
                self.soldier_selected(mouse_pos)

class Computer_Soldier(Unit):
    def __init__(self, game, x, y):
        # this method initialises the computer soldier as a white square
        super().__init__(game, x, y)
        self.team = "computer team"
        self.selected_unit = "sword"
        self.image.fill(WHITE)
        self.start_pos = self.rect.center
        self.health = 50
        self.full_health = self.health
        self.speed = SOLDIER_SPEED
        self.old_pos = 0
        self.last_move = 0
        self.is_clicked = False

    def update(self):
        # this method updates the computer soldier by following the player 
        self.check_health()
        self.AI_attack()
        self.delta_time_speed(SOLDIER_SPEED)
        self.check_win()
        # moves the unit in the maze and then pathfinds
        if self.rect.centerx > WIDTH*TILESIZE*2:
            now = pg.time.get_ticks()
            if now - self.last_move > 100:
                self.last_move = now
                self.move("left")
        else:
            self.move_to_unit(self.game.main_computer)

    
