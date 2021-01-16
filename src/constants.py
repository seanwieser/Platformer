import PIL.Image
import os
import pygame as py
import numpy
py.init()
# CONSTANTS
WIN_WIDTH = 1000  # Window Width
WIN_HEIGHT = 700 # Window Height
INV_WIN_HEIGHT = WIN_HEIGHT // 7
PLAY_W = 41       # Box Width
PLAY_H = 42       # Box Height
GRAV = 1         # Gravity Acceleration
GROUND_H= 10
GROUND = WIN_HEIGHT - PLAY_H - INV_WIN_HEIGHT - GROUND_H # Creates ground condition from top of player
PLAYER_SPEED = 2 # Constant horizontal player speed
BULLET_SPEED = 13 # Constant horizontal bullet speed
MAX_INV = 5 # Amount of inventory slots (4-6 looks best)
UNI_FONT = py.font.SysFont('comicsans', 30, True)
INV_FONT = py.font.SysFont('comicsans', 20, True)




# --------------------LOADING ALL IMAGES----------------------
def loadSpriteSet(action, path, kind, amount, size = (0,0)):
    answer = []
    basePath = '/home/seanwieser/Platformer'+path
    for i in range(amount):
        string = action + str(i)
        if kind == 'pygame':  
            answer.append(py.image.load(basePath+string+'.png'))
        elif kind == 'Image':
            newString = string+'_'+str(i)
            newIm = PIL.Image.open(basePath+string+'.png')
            newIm = newIm.resize(size)
            newIm.save(basePath+newString+'.png', 'png')
            answer.append(py.image.load(basePath+newString+'.png'))
            os.remove(basePath+newString+'.png')
    return answer


# Load all different player sprite sets depending on action
playerImages = '/CowboySpritePack/'
IDLE = loadSpriteSet('idle_', playerImages+'Idle/', 'pygame', 4)
IDLE_PISTOL = loadSpriteSet('idlePistol_', playerImages+'Idle/', 'pygame', 4)
IDLE_SHOTGUN = loadSpriteSet('idleShotgun_', playerImages+'Idle/', 'pygame', 4)
WALK = loadSpriteSet('walk_', playerImages+'Walk/', 'pygame', 4)
WALK_PISTOL = loadSpriteSet('walkPistol_', playerImages+'Walk/', 'pygame', 4)
WALK_SHOTGUN = loadSpriteSet('walkShotgun_', playerImages+'Walk/', 'pygame', 4)
JUMP = loadSpriteSet('jump_', playerImages+'Jump/', 'pygame', 4)
JUMP_PISTOL = loadSpriteSet('jumpPistol_', playerImages+'Jump/', 'pygame', 4)
JUMP_SHOTGUN = loadSpriteSet('jumpShotgun_', playerImages+'Jump/', 'pygame', 4)
SHOOT_IDLE_PISTOL = loadSpriteSet('shootIdlePistol_', playerImages+'ShootIdle/', 'pygame', 4)
SHOOT_IDLE_SHOTGUN = loadSpriteSet('shootIdleShotgun_', playerImages+'ShootIdle/', 'pygame', 4)
SHOOT_WALK_PISTOL = loadSpriteSet('shootWalkPistol_', playerImages+'ShootWalk/', 'pygame', 4)
SHOOT_WALK_SHOTGUN = loadSpriteSet('shootWalkShotgun_', playerImages+'ShootWalk/', 'pygame', 4)
SHOOT_JUMP_PISTOL = loadSpriteSet('shootJumpPistol_', playerImages+'ShootJump/', 'pygame', 4)
SHOOT_JUMP_SHOTGUN = loadSpriteSet('shootJumpShotgun_', playerImages+'ShootJump/', 'pygame', 4)

# Get weapons list then associate with weapon names
WEAPONS = loadSpriteSet('weapon_',playerImages+'Weapons/', 'pygame', 2)
WEAPONS = dict(zip(['Pistol','Shotgun'],WEAPONS))

#Inventory Constants
INV_BG_COLOR = (43, 53, 57)
WEAPON_DIM = (WIN_WIDTH//(2*MAX_INV), INV_WIN_HEIGHT)
INV_BOX_THICK = 5
WEAPONS_INV = loadSpriteSet('weapon_', playerImages+'Weapons/', 'Image', 2, WEAPON_DIM)
WEAPONS_INV = dict(zip(['Pistol','Shotgun'],WEAPONS_INV))
INV_POS = []
for h in range(MAX_INV):
    INV_POS.append((h*WEAPON_DIM[0], WIN_HEIGHT-WEAPON_DIM[1]))
SPLIT_POS = (INV_POS[MAX_INV-1][0]+WEAPON_DIM[0], WIN_HEIGHT-INV_WIN_HEIGHT)
BAR_DIM = [SPLIT_POS[0]+2*INV_BOX_THICK, 0, WIN_WIDTH//4, INV_WIN_HEIGHT//4]

SPRITES = {
        "idle": IDLE,
        "idlePistol": IDLE_PISTOL,
        "idleShotgun": IDLE_SHOTGUN,
        "walk": WALK,
        "walkPistol": WALK_PISTOL,
        "walkShotgun": WALK_SHOTGUN,
        "jump": JUMP,
        "jumpPistol": JUMP_PISTOL,
        "jumpShotgun": JUMP_SHOTGUN,
        "shootIdlePistol": SHOOT_IDLE_PISTOL,
        "shootIdleShotgun": SHOOT_IDLE_SHOTGUN,
        "shootWalkPistol": SHOOT_WALK_PISTOL,
        "shootWalkShotgun": SHOOT_WALK_SHOTGUN,
        "shootJumpPistol": SHOOT_JUMP_PISTOL,
        "shootJumpShotgun": SHOOT_JUMP_SHOTGUN
}

# ------------------------HIT BOXES---------------------------
# dimensions -> (width, height, +xBox, +yBox)
# HITBOXES['action+gun+boxType'][spriteCount][dimension] = [left, right]
IDLE_BODY = (((20,20), (30,30), (17,4), (6,6)),\
              ((20,20), (30,30), (17,4), (6,6)),\
              ((20,20), (30,30), (17,4), (5,5)),\
              ((20,20), (30,30), (17,4), (5,5)))
IDLE_FEET = (((18,18), (6,6), (18,5), (36,36)),\
              ((18,18), (6,6), (18,5), (36,36)),\
              ((18,18), (7,7), (18,5), (35,35)),\
              ((18,18), (7,7), (18,5), (35,35)))
IDLE_PISTOL_BODY = (((20,20), (29,29), (17,4), (6,6)),\
                  ((20,20), (29,29), (17,4), (6,6)),\
                  ((20,20), (29,29), (17,4), (5,5)),\
                  ((20,20), (29,29), (17,4), (5,5)))
IDLE_PISTOL_FEET = (((18,18), (7,7), (18,5), (35,35)),\
                   ((18,18), (7,7), (18,5), (35,35)),\
                   ((18,18), (8,8), (18,5), (34,34)),\
                   ((18,18), (8,8), (18,5), (34,34)))
WALK_BODY = (((20,20), (28,28), (17,4), (4,4)),\
              ((20,20), (28,28), (17,4), (3,3)),\
              ((20,20), (28,28), (17,4), (4,4)),\
              ((20,20), (28,28), (17,4), (3,3)))
WALK_FEET = (((16,16), (10,10), (18,7), (32,32)),\
              ((10,10), (11,11), (22,9), (31,31)),\
              ((14,14), (10,10), (19,8), (32,32)),\
              ((10,10), (11,11), (22,9), (31,31)))

WALK_PISTOL_BODY = (((20,20), (29,29), (17,4), (5,5)),\
                  ((20,20), (27,27), (17,4), (4,4)),\
                  ((20,20), (29,29), (17,4), (5,5)),\
                  ((20,20), (27,27), (17,4), (4,4)))
WALK_PISTOL_FEET = (((16,16), (8,8), (18,7), (34,34)),\
                      ((12,12), (11,11), (21,8), (31,31)),\
                      ((14,14), (8,8), (19,8), (34,34)),\
                      ((12,12), (11,11), (21,8), (31,31)))
WALK_SHOTGUN_BODY = (((20,20), (29,29), (17,4), (5,5)),\
                      ((20,20), (30,30), (17,4), (4,4)),\
                      ((20,20), (29,29), (17,4), (5,5)),\
                      ((20,20), (30,30), (17,4), (4,4)))
WALK_SHOTGUN_FEET = (((16,16), (8,8), (18,7), (34,34)),\
                      ((12,12), (8,8), (21,8), (34,34)),\
                      ((14,14), (8,8), (19,8), (34,34)),\
                      ((12,12), (8,8), (21,8), (34,34)))
SHOOT_BODY = (((19,19), (28,28), (18,4), (6,6)),\
               ((19,19), (28,28), (18,4), (6,6)),\
               ((19,19), (28,28), (18,4), (6,6)),\
               ((19,19), (28,28), (18,4), (6,6)))
SHOOT_FEET = (((18,18), (8,8), (18,5), (34,34)),\
               ((18,18), (8,8), (18,5), (34,34)),\
               ((18,18), (8,8), (18,5), (34,34)),\
               ((18,18), (8,8), (18,5), (34,34)))
SHOOT_JUMP_BODY = (((19,19), (28,28), (18,5), (4,4)),\
                    ((19,19), (28,28), (18,5), (5,5)),\
                    ((19,19), (28,28), (18,5), (5,5)),\
                    ((19,19), (28,28), (18,5), (5,5)))
SHOOT_JUMP_FEET = (((19,19), (9,9), (16,6), (33,33)),\
                    ((19,19), (9,9), (16,6), (33,33)),\
                    ((19,19), (9,9), (16,6), (33,33)),\
                    ((19,19), (9,9), (16,6), (33,33)))
SHOOT_JUMP_SHOTGUN_FEET = (((15,15), (9,9), (19,6), (33,33)),\
                           ((15,15), (9,9), (19,6), (33,33)),\
                           ((15,15), (9,9), (19,6), (33,33)),\
                           ((15,15), (9,9), (19,6), (33,33)))
JUMP_BODY = (((19,19), (28,28), (17,5), (1,1)),\
             ((19,19), (28,28), (17,5), (1,1)),\
             ((19,19), (28,28), (17,5), (1,1)),\
             ((19,19), (28,28), (17,5), (1,1)))
JUMP_FEET = (((22,22), (12,12), (14,5), (30,30)),\
             ((22,22), (12,12), (14,5), (30,30)),\
             ((22,22), (12,12), (14,5), (30,30)),\
             ((22,22), (12,12), (14,5), (30,30)))
JUMP_PISTOL_BODY = (((19,19), (28,28), (17,5), (4,4)),\
                   ((19,19), (28,28), (17,5), (4,4)),\
                   ((19,19), (28,28), (17,5), (4,4)),\
                   ((19,19), (28,28), (17,5), (4,4)))
JUMP_PISTOL_FEET = (((19,19), (9,9), (16,6), (33,33)),\
                   ((19,19), (9,9), (16,6), (33,33)),\
                   ((19,19), (9,9), (16,6), (33,33)),\
                   ((19,19), (9,9), (16,6), (33,33)))
HIT_BOXES = {
           "idle_body": IDLE_BODY,
           "idle_feet": IDLE_FEET,
           "idlePistol_body": IDLE_PISTOL_BODY,
           "idlePistol_feet": IDLE_PISTOL_FEET,
           "idleShotgun_body": IDLE_PISTOL_BODY,
           "idleShotgun_feet": IDLE_PISTOL_FEET,
           
           "walk_body": WALK_BODY,
           "walk_feet": WALK_FEET,
           "walkPistol_body": WALK_PISTOL_BODY,
           "walkPistol_feet": WALK_PISTOL_FEET,
           "walkShotgun_body": WALK_SHOTGUN_BODY,
           "walkShotgun_feet": WALK_SHOTGUN_FEET,
           
           "shootIdlePistol_body": SHOOT_BODY,
           "shootIdlePistol_feet": SHOOT_FEET,
           "shootIdleShotgun_body": SHOOT_BODY,
           "shootIdleShotgun_feet": SHOOT_FEET,
           "shootWalkPistol_body": SHOOT_BODY,
           "shootWalkPistol_feet": SHOOT_FEET,
           "shootWalkShotgun_body": SHOOT_BODY,
           "shootWalkShotgun_feet": SHOOT_FEET,
           "shootJumpPistol_body": SHOOT_JUMP_BODY,
           "shootJumpPistol_feet": SHOOT_JUMP_FEET,
           "shootJumpShotgun_body": SHOOT_JUMP_BODY,
           "shootJumpShotgun_feet": SHOOT_JUMP_SHOTGUN_FEET,

           "jump_body": JUMP_BODY,
           "jump_feet": JUMP_FEET,
           "jumpPistol_body": JUMP_PISTOL_BODY,
           "jumpPistol_feet": JUMP_PISTOL_FEET,
           "jumpShotgun_body": JUMP_PISTOL_BODY,
           "jumpShotgun_feet": JUMP_PISTOL_FEET
}
