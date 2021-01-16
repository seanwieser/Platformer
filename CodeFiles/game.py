from classes import *
from constants import *
import PIL.Image
import os
# Useful functions
def redrawGameWindow():
    global win
    win.fill((255,255,255))
    py.draw.rect(win, (0, 0, 0), (0, GROUND+PLAY_H, WIN_WIDTH, GROUND_H))
    player.draw(win)
    bulletManager.draw(win)
    py.display.update()

# Set up the window with dimensions, name, and clock
win = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
py.display.set_caption("Game")
clock = py.time.Clock()

# Create game objects
bulletManager = BulletManager()
gun1 = Gun('Pistol', 'Light', 10)
gun2 = Gun('Shotgun', 'Shotgun', 5)
gunManager = GunManager()
gunManager.add(gun1)
gunManager.add(gun2)
player = Player(PLAY_W, PLAY_H, SPRITES, bulletManager, gunManager)

# Game loop
run = True
pause = False
while run:
    clock.tick(40)
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            run = False
        if event.type == py.KEYDOWN and event.key == py.K_p: # causes a crash. pause is broken
            pause = not pause
    if not pause:
        keys = py.key.get_pressed()
        player.move(keys, events)
        bulletManager.moveBullets()
        redrawGameWindow()
    
py.quit()
