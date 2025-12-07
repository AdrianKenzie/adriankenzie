from pygame import *
from random import randint

font.init()
font1 = font.Font(None, 80)
win_text = font1.render('YOU WIN!', True, (255, 255, 255))
lose_text = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "sky.jpg"
img_bullet = "bullet.png"
img_hero = "stack.png"
img_enemy = "lawan.png"

score = 0
goal = 1000
lost = 0
max_lost = 120
shooting = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
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
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        rocket = Rocket(img_bullet, self.rect.centerx - 10, self.rect.top, 25, 40, -7)
        bullets.add(rocket)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Rocket(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        hits = sprite.spritecollide(self, monsters, False)
        if hits:
            self.explode()
            self.kill()
    def explode(self):
        explosion_radius = 80
        draw.circle(window, (255, 120, 0), (self.rect.centerx, self.rect.centery), explosion_radius)
        global score
        for m in monsters:
            dist = ((m.rect.centerx - self.rect.centerx) ** 2 + (m.rect.centery - self.rect.centery) ** 2) ** 0.5
            if dist < explosion_radius:
                m.kill()
                score += 1
                new_enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(new_enemy)

win_width = 700
win_height = 500
display.set_caption("VirusBlitz")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                shooting = True
        elif e.type == KEYUP:
            if e.key == K_SPACE:
                shooting = False

    if not finish:
        window.blit(background, (0, 0))
        text = font2.render(f"Kills: {score} / {goal}", True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render(f"Missed: {lost}", True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        if shooting:
            fire_sound.play()
            ship.fire()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose_text, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))

        display.update()
    time.delay(50)
