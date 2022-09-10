from pygame import *
from random import randint

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

font.init()
font1 = font.Font(None, 80)
win = font1.render("You win", True, (255, 255, 255))
lose = font1.render("You lose", True, (0, 0, 0))

font2 = font.Font(None, 36)

score = 0
lost = 0
max_lost = 3
goal = 10

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet) 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, 400, 80, 100, 10)
fire_sound = mixer.Sound("fire.ogg")
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, 620), -40,80,50, randint(1,5))
    monsters.add(monster)
asteroid = sprite.Group()
for i in range(1,3)
    asteroid = Enemy(img_ast,randint(30,670), -40,80, 50, randint(1,7))
    asteroid.add(asteroid)
bullets = sprite.Group()
finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
              if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if not finish:
        window.blit(back, (0, 0))
        ship.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, 620), -40,80,50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        text_score = font2.render("Score: "+str(score), 1, (255,255,255))
        window.blit(text_score, (10, 20))

        display.update()
    time.delay(60)
