import pygame
import time
import random

class Brick(pygame.sprite.Sprite):
    
    def __init__(self, img, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

class Food(pygame.sprite.Sprite):
    
    def __init__(self, img, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    
    def get_position(self):
        return (self.rect.x, self.rect.y)


class Snake(pygame.sprite.Sprite):
    
    def __init__(self, img, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.part = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.move = 30
        self.movedirection = (0,30)
        self.md = 'D'
        self.tail = []
        self.SHOOT_SOUND = pygame.mixer.Sound('shoot.wav')
        self.SHOOT_SOUND.set_volume(0.2)
        self.MOVETANK = pygame.mixer.Sound('move5.wav')
        self.MOVETANK.set_volume(0.6)
        self.S_EAT = pygame.mixer.Sound('eating.wav')
        self.S_EAT.set_volume(1)

    def update(self, md):
        keys = pygame.key.get_pressed()

        if md == 'U' and self.md != 'D':
            self.movedirection = (0, -self.move)
            self.md = 'U'
        elif md == 'D' and self.md != 'U':
            self.movedirection = (0, self.move)
            self.md = 'D'
        elif md == 'L' and self.md != 'R':
            self.movedirection = (-self.move, 0)
            self.md = 'L'
        elif md == 'R' and self.md != 'L':
            self.movedirection = (self.move, 0)
            self.md = 'R'     
        

        new_rect = self.rect.move(self.movedirection)
        self.updatetail()
        self.rect = new_rect

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for t in self.tail:
            screen.blit(self.part, t)

    def eatfood(self, food):
        pos = food.get_position()
        self.tail.append(Tail(self.part, pos))
        self.S_EAT.play()
        

    def updatetail(self):
        self.tail.append(Tail(self.part,(self.rect.x, self.rect.y)))
        self.tail = self.tail[1:]

class Tail(pygame.sprite.Sprite):

    def __init__(self, img, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    
    def get_position(self):
        return (self.rect.x, self.rect.y)


def spawnfood():
    pole = 30
    x = random.randrange(pole, pole*26, pole)
    y = random.randrange(pole*4, pole*29, pole)
    return (x, y)

def ifcolide(player, foods):
    global score
    global SHOOT_SOUND

    for t in player.tail:
        if pygame.sprite.collide_rect(t, player):
            SHOOT_SOUND.play()
            score = 0
            print('GAME OVER')
            player.tail.clear()
            player.rect.x = 30*14
            player.rect.y = 30*14
            foods.empty()
            break

    for f in foods:
        if pygame.sprite.collide_rect(player, f):
            foods.remove(f)
            player.eatfood(f)
            score += 1
            print(str(score))
            break

def ifbrickcolide(player, bricks):
    global score
    global foods
    global SHOOT_SOUND

    for b in bricks:
        if pygame.sprite.collide_rect(b, player):
            SHOOT_SOUND.play()
            score = 0
            print('GAME OVER')
            player.tail.clear()
            player.rect.x = 30*14
            player.rect.y = 30*14
            foods.empty()
            break            

            
pygame.init()
score = 0
pygame.display.set_caption('Snake')
bg = pygame.image.load('bg.png')
snake = pygame.image.load('snake.png')
food = pygame.image.load('food.png')
brick = pygame.image.load('brk.png')

w = 30
h = 30
pole = 30


bricks = pygame.sprite.Group()
foods = pygame.sprite.Group()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((w*27, h*30))

done = False

snk = Snake(snake, (pole*14, pole*14))

font = pygame.font.SysFont("Gargi", 72)
text = font.render("Hello, Snake", True, (0, 128, 0))


for i in range(27):
    for j in range(3,30):        
        if i == 0 or i == 26:
            bricks.add(Brick(brick,(i*30,j*30)))
        elif j == 3 or j == 29:
            bricks.add(Brick(brick,(i*30,j*30)))

for y in range (7, 26):
    bricks.add(Brick(brick,(20*30,y*30)))

for y in range (7, 26):
    bricks.add(Brick(brick,(6*30,y*30)))

SHOOT_SOUND = pygame.mixer.Sound('shoot.wav')
SHOOT_SOUND.set_volume(0.2)
MOVETANK = pygame.mixer.Sound('move5.wav')
MOVETANK.set_volume(0.6)
MUSIC = pygame.mixer.Sound('m.wav')
MUSIC.set_volume(0.6)
S_EAT = pygame.mixer.Sound('eating.wav')
S_EAT.set_volume(1)
MUSIC.play(-1)

md = 'U'
timer = 0 
while not done:
    clock.tick(10)
    events = pygame.event.get()


    
    text = font.render('Player Score: '+str(score), True, (0, 128, 0))

    if timer == 26:
        timer = 0
    
    if timer == 25:
        foods.add(Food(food, spawnfood()))


    
    for event in events:
 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                md = 'U'
            elif event.key == pygame.K_DOWN:
                md = 'D'
            elif event.key == pygame.K_LEFT:
                md = 'L'
            elif event.key == pygame.K_RIGHT:
                md = 'R'

    screen.fill((255,255,255))
    screen.blit(text, (0, 0))
    for i in range(27):
        for j in range(3,30):        
            screen.blit(bg, (i*30,j*30))


    snk.update(md)
    foods.draw(screen)
    bricks.draw(screen)
    snk.draw(screen)
    #pygame.display.flip()
    pygame.display.update()
    ifcolide(snk, foods)
    ifbrickcolide(snk, bricks)
    timer += 1

    for event in events:
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            break
    