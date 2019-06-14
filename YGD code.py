'''
WARNING: THIS PROGRAM REQUIRES PYTHON AND PYGAME. USE 'pip install pygame'
to install pygame. This program was made by Daniel Baltruschat, William Raichura
and David Robinson.I am pleased to say that all of this is made by us(other than
python and the python modules obviously) and we have gotten no help from adults
except for in the compiling of the code.

Credits:
Code: Daniel Baltruschat Age 11
Background: David Robinson Age 11
Hero: Daniel Baltruschat Age 11
Dog: William Raichura Age 11
Flying: Daniel Baltruschat Age 11
Double: William Raichura Age 11
Devil: David Robinson Age 11
Ghost: William Raichura Age 11
Music: William Raichura Age 11
'''


import pygame
import time
import random
import pickle

pygame.init()
pygame.mixer.init()

display_width = 1200
display_height = 600
level = 1
added_new = True
latest = 0
num_monsters = [1, 0, 0, 0, 0]
music  = pygame.mixer.music.load('Music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()
try:
    file = open('data.pkl', 'rb')
    savedata = pickle.load(file)
except:
    savedata = ['Someone', 0]

xpos = 0


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, placement):
        global xpos
        self.placement = placement
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left = xpos + (self.placement - 1) * 1200
        self.rect.top = 0

    def update(self):
        global xpos
        self.rect.left = xpos + (self.placement - 1) * 1200
        self.rect.top = 0
        

class Hero(pygame.sprite.Sprite):
    def __init__(self, images, location):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.jumping = False
        self.jumped = False
        self.hp = 500
        self.damage = 50
        self.attacked = False
        self.attacking = False
        self.direction = 'right'
        self.speed = [0,0]
        self.images = images
        self.image_number = 0
        self.image = pygame.image.load(self.images[self.image_number])
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.top = location

    def move_left(self):
        global xpos
        self.direction = 'left'
        self.image_number = 2
        right = self.rect.right
        top = self.rect.top
        self.image = pygame.image.load(self.images[self.image_number])
        self.rect = self.image.get_rect()
        self.rect.right = right
        self.rect.top = top
        self.speed[0] = -5

    def move_right(self):
        global xpos
        self.direction = 'right'
        self.image_number = 0
        left = self.rect.left
        top = self.rect.top
        self.image = pygame.image.load(self.images[self.image_number])
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed[0] = 5

    def keyup(self):
        self.speed[0] = 0

    def jump(self):
        if not self.jumping:
            self.jumped = True
            self.jumping = True

    def update(self):
        global xpos
        
        self.moving = False

        if self.jumped:
            self.speed[1] = -14
            if self.rect.top <= 50:
                self.speed[1] = 0
                self.jumped = False

        if self.jumping:
            if not self.jumped and self.rect.top >= 357:
                self.jumping = False
            
        if self.rect.top < 357 and not self.jumped:
            self.speed[1] = 14
            
        if self.rect.top > 357 and not self.jumped:
            self.speed[1] = 0
            self.rect.top = 357

        if self.direction == 'right':
            if self.rect.left < 900:
                self.moving = True

            else:
                if xpos > -1200:
                    xpos = xpos - self.speed[0]

        if self.direction == 'left':
            if self.rect.right > 300:
                self.moving = True
                
            else:
                if xpos < 0:
                    xpos = xpos - self.speed[0]

        if self.moving:
            self.rect = self.rect.move(self.speed)

        else:
            self.rect = self.rect.move(0, self.speed[1])

        if self.hp <= 0:
            self.alive = False

    def attack(self):
        if self.attacked == False:
            self.attacked = True
            self.attacking = True
            self.now = time.time()
            if self.direction == 'left':
                right = self.rect.right
                self.image_number = 3
            if self.direction == 'right':
                left = self.rect.left
                self.image_number = 1
            top = self.rect.top
            self.image = pygame.image.load(self.images[self.image_number])
            self.rect = self.image.get_rect()
            if self.direction == 'left':
                self.rect.right = right
            if self.direction == 'right':
                self.rect.left = left
            self.rect.top = top

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, name, hp, image, damage):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.damage = damage
        self.hp = hp
        self.x = x
        self.speed = [0,0]
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = (xpos + self.x, 414)

    def text(self):
        font = pygame.font.Font(None, 20)
        self.hp_text = font.render('HP: ' + str(self.hp), 1, (0,0,0))
        gameDisplay.blit(self.hp_text, [self.rect.left, self.rect.top - 20])

class Dog(Monster):
    def update(self):
        if self.hp <= 0:
            self.kill()
        if self.rect.left > hero.rect.right:
            self.x -= 1
        else:
            self.x += 1
        self.rect.left = xpos + self.x

class Flying(Monster):
    def __init__(self, x, name, hp, image, damage):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.damage = damage
        self.hp = hp
        self.x = x
        self.speed = [0,0]
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = (xpos + self.x, 314)
        
    def update(self):
        if self.hp <= 0:
            self.kill()
        if self.rect.left > hero.rect.right:
            self.x -= 1
        else:
            self.x += 1
        if self.rect.bottom < 414:
            if self.rect.left >= hero.rect.left:
                if self.rect.left <= hero.rect.right:
                    self.rect.top += 4
            if self.rect.left >= hero.rect.left:
                if self.rect.left <= hero.rect.right:
                    self.rect.top += 4
        self.rect.left = xpos + self.x

class Double(Monster):
    def update(self):
        if self.hp <= 0:
            self.kill()
        if self.rect.left > hero.rect.right:
            self.x -= 3
        else:
            self.x += 3
        self.rect.left = xpos + self.x

class Devil(Monster):
    def __init__(self, x, name, hp, image, damage):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.damage = damage
        self.hp = hp
        self.x = x
        self.speed = [0, 0]
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = (xpos + self.x, 314)


    def update(self):
        if self.hp <= 0:
            self.kill()
        if self.rect.left > hero.rect.right:
            self.x -= 5
        else:
            self.x += 5
        if self.rect.bottom < 414:
            if self.rect.left >= hero.rect.left:
                if self.rect.left <= hero.rect.right:
                    self.rect.top += 10
            if self.rect.left >= hero.rect.left:
                if self.rect.left <= hero.rect.right:
                    self.rect.top += 10
        self.rect.left = xpos + self.x

class Ghost(Monster):
    def __init__(self, x, name, hp, image, damage):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.damage = damage
        self.hp = hp
        self.x = x
        self.flying = random.choice([True, False])
        self.speed = [0,0]
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        if self.flying:
            self.rect.left, self.rect.bottom = (xpos + self.x, 314)
        else:
            self.rect.left, self.rect.bottom = (xpos + self.x, 414)
        
    def update(self):
        if self.hp <= 0:
            self.kill()
        if self.rect.left > hero.rect.right:
            self.x -= 3
        else:
            self.x += 3
        if self.flying:
            if self.rect.bottom < 414:
                if self.rect.left >= hero.rect.left:
                    if self.rect.left <= hero.rect.right:
                        self.rect.top += 7
                if self.rect.left >= hero.rect.left:
                    if self.rect.left <= hero.rect.right:
                        self.rect.top += 7
        self.rect.left = xpos + self.x

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
x_change = 0
y_change = 0
gameExit = False
background1 = Background('background.png', 1)
background2 = Background('background.png', 2)
backgrounds = pygame.sprite.Group(background1, background2)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("You're Gonna Die(YGD)")
clock = pygame.time.Clock()
hero = Hero(['swordman_normal_right.png', 'swordman_hitting_right.png', 'swordman_normal_left.png', 'swordman_hitting_left.png'], [600, 357])
font = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 30)

def update():
    global level_text
    global hp_text
    global data_text
    hero.update()
    backgrounds.update()
    monsters.update()
    level_text = font.render('Level: ' + str(level), 1, (0,0,0))
    hp_text = font.render('HP: ' + str(hero.hp), 1, (0,0,0))
    data_text = font2.render('The highest score is set by %s who managed to get to level %i!' %(savedata[0], savedata[1]), 1, (255,0,0))

def detect():
    if hero.attacked == True:
        if hero.attacking == True:
            
            hit = pygame.sprite.spritecollide(hero, monsters, False)
            if hit:
                hit[0].hp -= hero.damage
                if hero.direction == 'right':
                    hit[0].x += 30
                else:
                    hit[0].x -= 30
                
            hero.attacking = False
            hero.image_number = hero.image_number - 1
            if hero.direction == 'left':
                right = hero.rect.right
            if hero.direction == 'right':
                left = hero.rect.left
            top = hero.rect.top
            hero.image = pygame.image.load(hero.images[hero.image_number])
            hero.rect = hero.image.get_rect()
            if hero.direction == 'left':
                hero.rect.right = right
            if hero.direction == 'right':
                hero.rect.left = left
            hero.rect.top = top
        else:
            if time.time() - hero.now >= 0.01:
                hero.attacked = False

def level_monsters():
    index = 0
    for num in num_monsters:
        for i in range(num):
            if index == 0:
                monster = Dog(random.randint(300, 2000), 'dog', 50, 'dog.png', 50)
            elif index == 1:
                monster = Flying(random.randint(300, 2000), 'flying', 100, 'flying.png', 75)
            elif index == 2:
                monster = Double(random.randint(300, 2000), 'double', 150, 'double.png', 100)
            elif index == 3:
                monster = Devil(random.randint(300, 2000), 'devil', 200, 'devil.png', 125)
            else:
                monster = Ghost(random.randint(300, 2000), 'ghost', 250, 'ghost.png', 175)

            monsters.add(monster)
        index += 1
                
def create_level():
    global monsters
    global num_monsters
    global monster_types
    global added_new

    latest = -1
    monsters.empty()

    for num in num_monsters:
        if num > 0:
            latest = latest + 1#finds the last one that exists

    if num_monsters[latest] == 2 and num_monsters[-1] <= 0:
        add_new = True
    else:
        add_new = False


    if num_monsters[latest] == 1:
        if added_new:
            add_new = False
            index = 0
            for num in num_monsters:
                if num > 0:
                    if index != latest:
                        num_monsters[index] += 2
                    else:
                        num_monsters[index] += 1
                    
                index += 1
    if add_new:
        added_new = True
        index = 0
        for num in num_monsters:
            if num > 0:
                num_monsters[index] -= 1
            index += 1
        num_monsters[latest + 1] = 1

    level_monsters()

monsters = pygame.sprite.Group()

level_monsters()

now = time.time()
passed = False

while not gameExit:
    if hero.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    hero.move_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    hero.move_right()
                if event.key == pygame.K_SPACE:
                    hero.jump()
            if event.type == pygame.KEYUP:
                    hero.keyup()
            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.attack()

            
        kill = pygame.sprite.spritecollide(hero, monsters, False)

        if time.time() - now >= 1:
            passed = False

        if kill and not passed and hero.attacking == False:
            passed = True
            hero.hp -= kill[0].damage
            if hero.direction == 'right':
               hero.rect.left -= 10
            else:
                hero.rect.left += 10
            now = time.time()

        update()
        gameDisplay.fill([255, 255, 255])
        backgrounds.draw(gameDisplay)
        monsters.draw(gameDisplay)
        gameDisplay.blit(hero.image, hero.rect)
        gameDisplay.blit(level_text, [10, 10])
        gameDisplay.blit(hp_text, [10, 60])
        gameDisplay.blit(data_text, [200, 10])
        for monster in monsters:
            monster.text()
        pygame.display.flip()
        clock.tick(30)
        detect()
        if len(monsters) <= 0:
            level += 1
            level_cleared = True
            create_level()
            hero.hp = 500
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
    else:
        gameExit = True

font = pygame.font.Font(None, 100)
gameover_text = font.render('GAME OVER', 1, (255,0,0))
font2 = pygame.font.Font(None, 40)
end_score_text = font2.render('Level: ' + str(level), 1, (0, 0, 0))

beat_high = False

if level > savedata[1]:
    beat_high = True
    file = open('data.pkl', 'wb')
    savedata[1] = level
    font3 = pygame.font.Font(None, 40)
    name_text = font3.render('Enter your name: ', 1, (0, 0, 0))
    name = ''

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if beat_high:
                if len(name) > 0:
                    savedata[0] = name
                else:
                    savedata[0] = 'Someone'
                pickle.dump(savedata, file)
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if beat_high:
                    if len(name) > 0:
                        savedata[0] = name
                    else:
                        savedata[0] = 'Someone'
                    pickle.dump(savedata, file)
                pygame.quit()
                quit()
            if event.key == pygame.K_BACKSPACE:
                if len(name) > 0:
                    namelist = list(name)
                    namelist.remove(namelist[-1])
                    name = ''.join(namelist)
            else:
                if len(name) <= 20:
                    name += event.unicode
                    if len(name) == 0:
                        name = name.upper()


    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    gameDisplay.fill([255,255,255])
    gameDisplay.blit(gameover_text, [375, 200])
    gameDisplay.blit(end_score_text, [520, 340])
    if beat_high:
        name_text = font3.render('Enter your name: ' + name, 1, (0, 0, 0))
        gameDisplay.blit(name_text, [10, 560])
    
    pygame.display.flip()
    clock.tick(30)
