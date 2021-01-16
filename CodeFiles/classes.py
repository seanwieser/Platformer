from constants import *

class Player(object):
    def __init__(self, width, height, spriteDict, bulletManager, gunManager):
        #Physical Attributes
        self.width = width
        self.height = height
        self.xPos = WIN_WIDTH- 100
        self.yPos = 50
        self.xVel = 0
        self.yVel = 0
        self.rightMove = True
        self.onGround = False
        #Animation
        self.spriteDict = spriteDict
        self.spriteCount = 0
        self.spriteAct = 'idle' #may include 'shoot' prefix, no gun suffix
        self.spriteTimer = [0,0]
        #Gun Related
        self.hasGun = False
        self.canShoot = False
        self.showHitBoxes = False
        self.hitboxes = {'body': [0,0,0,0], 'feet': [0,0,0,0]} #[width, height, x, y]
        self.shooting = False
        self.bulletManager = bulletManager
        self.gunNum = 0 # index of equipped gun in self.guns
        self.gunManager = gunManager
        #Player Stats
        self.health = [6,10]
        self.armor = [5, 10]
        self.exp = [10, 100]
        self.level = 1
    def move(self, keys, events):
        for event in events:
            if event.type == py.KEYDOWN: # ensures a key event occurred
                if event.key == py.K_s and not self.shooting:
                    self.toggleGun()   
                if 49<=event.key and event.key<=len(self.gunManager.getGunNames())+48:
                    self.toggleGunNum(event.key-49)
                if event.key == py.K_f:
                    self.toggleGunNum(-1)
                if event.key == py.K_h:
                    self.showHitBoxes = not self.showHitBoxes
                if event.key == py.K_r and self.hasGun:
                    self.gunManager.reloadGun()
                    self.updateShootAbility()

                if self.canShoot and event.key == py.K_SPACE:
                    self.shoot()
                    xBullet = int(self.getPos()[0]+PLAY_W-20)
                    yBullet = int(self.getPos()[1]+(PLAY_H//2)+5)
                    newBullet = Bullet((xBullet,yBullet), 3, (0, 0 , 255), self.rightMove, BULLET_SPEED)
                    self.bulletManager.add(newBullet)
                    
        if keys[py.K_a] and self.xPos >= self.xVel:
            self.xVel = -PLAYER_SPEED
            self.rightMove = False
            self.newAction('walk')
        elif keys[py.K_d] and self.xPos <= WIN_WIDTH - self.width - self.xVel:
            self.xVel = PLAYER_SPEED
            self.rightMove = True
            self.newAction('walk')
        else:
            self.xVel = 0
            self.newAction('idle')
            
        self.onGround = (self.yPos >= GROUND)
        if self.onGround:
            self.yPos = GROUND
            self.yVel = 0
            if keys[py.K_w]:
                self.yVel = -20
                self.newAction('jump')
        else:
            self.yVel = self.yVel + GRAV
            self.newAction('jump')
        
        self.xPos = self.xPos + self.xVel 
        self.yPos = self.yPos + self.yVel
        self.adjustHitBoxes()

    def draw(self, win):
        self.drawAnimation(win)
        self.drawInventoryWindow(win)
        if self.showHitBoxes:
            self.drawHitBoxes(win)
        
    def drawAnimation(self, win):
        self.spriteTimer[0] += py.time.get_ticks() - self.spriteTimer[1]
        if self.spriteTimer[0]>250:
            self.spriteTimer[0] = 0
            self.spriteTimer[1] = py.time.get_ticks()
            if self.spriteCount == (len(self.spriteDict[self.curSprite()])-1):
                self.spriteCount = 0
                if self.shooting:
                    self.shooting = False
            else:
                self.spriteCount += 1
        playerImage = self.spriteDict[self.curSprite()][self.spriteCount]
        if not self.rightMove:
            playerImage = py.transform.flip(playerImage, True, False)
        win.blit(playerImage, self.getPos())

    def drawInventoryWindow(self, win):
        py.draw.rect(win, INV_BG_COLOR, (0, WIN_HEIGHT-INV_WIN_HEIGHT, \
                                         WIN_WIDTH, WIN_HEIGHT-INV_WIN_HEIGHT))
        py.draw.rect(win, (0,0,0), (SPLIT_POS[0], SPLIT_POS[1], INV_BOX_THICK, INV_WIN_HEIGHT), 0)
        self.drawBars(win)
        self.drawInventoryGunSlots(win)
        self.drawInventoryGuns(win)

    def drawBars(self, win):
        py.draw.rect(win, (0,0,0), (BAR_DIM[0], SPLIT_POS[1]+1/6*INV_WIN_HEIGHT, \
                                    BAR_DIM[2], BAR_DIM[3]), INV_BOX_THICK)
        py.draw.rect(win, (255,0,0), (BAR_DIM[0]+3, \
                                    SPLIT_POS[1]+1/6*INV_WIN_HEIGHT+2, \
                                    int((self.health[0]/self.health[1])*(BAR_DIM[2]-INV_BOX_THICK)), \
                                      BAR_DIM[3]-INV_BOX_THICK), 0)
        py.draw.rect(win, (0,0,0), (BAR_DIM[0], \
                                    SPLIT_POS[1]+1/2*INV_WIN_HEIGHT+3, \
                                    BAR_DIM[2], BAR_DIM[3]), INV_BOX_THICK)
        py.draw.rect(win, (0,0,255), (BAR_DIM[0]+3, \
                                    SPLIT_POS[1]+1/2*INV_WIN_HEIGHT+5, \
                                    int((self.armor[0]/self.armor[1])*(BAR_DIM[2]-INV_BOX_THICK)), \
                                      BAR_DIM[3]-INV_BOX_THICK), 0)
        py.draw.rect(win, (0,0,0), (7/8*WIN_WIDTH-1/3*BAR_DIM[2], \
                                    SPLIT_POS[1]+1/2*INV_WIN_HEIGHT+int(BAR_DIM[3]/2)+4, \
                                    BAR_DIM[2]*2/3, int(BAR_DIM[3]/2)), 3)
        py.draw.rect(win, (0,255,0), (7/8*WIN_WIDTH-1/3*BAR_DIM[2]+2, \
                                    SPLIT_POS[1]+1/2*INV_WIN_HEIGHT+int(BAR_DIM[3]/2)+6, \
                                    (self.exp[0]/self.exp[1])*(2/3*BAR_DIM[2]), int(BAR_DIM[3]/2)-4), 0)
        healthText = str(self.health[0])+'/'+str(self.health[1])
        healthTextSize = UNI_FONT.size(healthText)
        healthSurface = UNI_FONT.render(healthText, 1, (255,255,255))
        win.blit(healthSurface, (BAR_DIM[0]+BAR_DIM[2]//2-healthTextSize[0]//2,\
                                 SPLIT_POS[1]+1/6*INV_WIN_HEIGHT+1+int((BAR_DIM[3]-healthTextSize[1])/2)))
        armorText = str(self.armor[0])+'/'+str(self.armor[1])
        armorTextSize = UNI_FONT.size(armorText)
        armorSurface = UNI_FONT.render(armorText, 1, (255,255,255))
        win.blit(armorSurface, (BAR_DIM[0]+BAR_DIM[2]//2-healthTextSize[0]//2,\
                                SPLIT_POS[1]+1/2*INV_WIN_HEIGHT+4+int((BAR_DIM[3]-healthTextSize[1])/2)))
        lvlText = 'Lvl: ' + str(self.level)
        lvlTextSize = INV_FONT.size(lvlText)
        lvlSurface = INV_FONT.render(lvlText, 1, (255,255,255))
        win.blit(lvlSurface, (7/8*WIN_WIDTH-lvlTextSize[0]//2, \
                              SPLIT_POS[1]+1/2*INV_WIN_HEIGHT+int(BAR_DIM[3]+4)))
    def drawInventoryGunSlots(self, win):
        py.draw.rect(win, (0, 255, 0), (INV_POS[self.gunManager.getGunNum()][0], INV_POS[self.gunManager.getGunNum()][1], \
                                        WEAPON_DIM[0], WEAPON_DIM[1]), INV_BOX_THICK)
        for j in range(len(INV_POS)):
            weaponNumText = UNI_FONT.render(str(j+1), 1, (255,255,255), INV_BG_COLOR)
            win.blit(weaponNumText, numpy.array(INV_POS[j])+5)
            if j > len(self.gunManager.getGunNames())-1:
                emptyText = 'Empty'
                emptyTextSurface = UNI_FONT.render(emptyText, 1, (255, 255, 255), INV_BG_COLOR)
                emptyTextSize = UNI_FONT.size(emptyText)
                win.blit(emptyTextSurface, (int(INV_POS[j][0]+1/2*(WEAPON_DIM[0]-emptyTextSize[0])), \
                                 int(INV_POS[j][1]+1/2*(WEAPON_DIM[1]-emptyTextSize[1]))))
    def drawInventoryGuns(self, win):
        i = 0
        for gun in self.gunManager.getGuns():
            win.blit(WEAPONS_INV[gun.getName()], INV_POS[i])
            clipText = str(gun.getClipAmmo())+'/'+str(gun.getClipSize())
            clipSurface = INV_FONT.render(clipText, 1, (255,255,255), INV_BG_COLOR)
            xText = INV_POS[i][0] + WEAPON_DIM[0]//2 - INV_FONT.size(clipText)[0]//2
            win.blit(clipSurface, (xText, INV_POS[i][1]+INV_WIN_HEIGHT-34))

            ammoType = gun.getAmmoType()
            ammoInvText = str(ammoType)+": "+ str(self.gunManager.getAmmoAmount(ammoType))
            ammoSurface = INV_FONT.render(ammoInvText, 1, (255,255,255), INV_BG_COLOR)
            xAmmo = INV_POS[i][0] + WEAPON_DIM[0]//2 - INV_FONT.size(ammoInvText)[0]//2
            win.blit(ammoSurface, (xAmmo, INV_POS[i][1]+INV_WIN_HEIGHT-18))
            i+=1
            
    def adjustHitBoxes(self):
        dirIndex = 0
        endString = ['_body', '_feet']
        if self.rightMove:
            dirIndex += 1
        for boxType in self.hitboxes:
            for element in range(len(self.hitboxes[boxType])):
                dictKey = self.curSprite()+'_'+boxType
                self.hitboxes[boxType][element] \
                    = HIT_BOXES[dictKey][self.spriteCount][element][dirIndex]
    def drawHitBoxes(self, win):
        py.draw.rect(win, (255, 0, 0), (self.xPos+self.hitboxes['body'][2], \
                                        self.yPos+self.hitboxes['body'][3], \
                                        self.hitboxes['body'][0], \
                                        self.hitboxes['body'][1]), 1)
        py.draw.rect(win, (0, 255, 0), (self.xPos+self.hitboxes['feet'][2], \
                                        self.yPos+self.hitboxes['feet'][3], \
                                        self.hitboxes['feet'][0], \
                                        self.hitboxes['feet'][1]), 1)
    def shoot(self):
        self.shooting = True
        self.spriteCount = 0
        self.gunManager.manageClip(-1)
        self.updateShootAbility()
    def curSprite(self):
        answer = self.spriteAct
        if self.hasGun:
            return answer+self.gunManager.equippedGun().getName()
        return answer
    def newAction(self, newAct):
        if not self.shooting:
            self.spriteAct = newAct
        else:
            self.spriteAct = 'shoot'+newAct.capitalize()
    def updateShootAbility(self):
        if self.hasGun and self.gunManager.equippedGun().getClipAmmo() > 0:
            self.canShoot = True
        else:
            self.canShoot = False
        
    def toggleGunNum(self, newGunIndex):
        if newGunIndex >= 0:
            self.gunManager.setGunNum(newGunIndex)
        else:
            if self.gunManager.getGunNum() == self.gunManager.gunAmount()-1:
                self.gunManager.setGunNum(0)
            else:
                self.gunManager.incrementGunNum(1)
        self.updateShootAbility()
    def toggleGun(self):
        self.hasGun = not self.hasGun
        self.updateShootAbility()
    

        
    def getPos(self):
        return (self.xPos, self.yPos)
    
class Enemy(object):
    def __init__(self, width, height, spriteDict):
        self.width = width
        self.height = height
        self.spriteDict = spriteDict
        pass
    def draw(self, win):
        pass
    def move(self, path):
        pass

class BulletManager(object):
    def __init__(self):
        self.bullets = []
    def add(self, newBullet):
        self.bullets.append(newBullet)
    def moveBullets(self):
        for bullet in self.bullets:
            if bullet.getX() > WIN_WIDTH or bullet.getX() < 0:
                self.bullets.pop(self.bullets.index(bullet))
            bullet.pos = (bullet.pos[0]+bullet.vel, bullet.pos[1])
    def draw(self, win):
        for bullet in self.bullets:
            bullet.draw(win)

class Bullet(object):
    def __init__(self, pos, radius, color, rightMove, vel):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.rightMove = rightMove
        if not rightMove:
            vel = -vel
        self.vel = vel

    def getX(self):
        return self.pos[0]
    def draw(self, win):
        py.draw.circle(win, self.color, self.pos, int(self.radius))

class GunManager(object):
    def __init__(self):
        self.guns = []
        self.gunNum = 0
        self.ammo = {
                "Light": 20,
                "Heavy": 0,
                "Shotgun": 10,
                "Energy": 0
        }
        

    def add(self, newGun):
        self.guns.append(newGun)

    def getGunNames(self):
        answer = []
        for gun in self.guns:
            answer.append(gun.getName())
        return answer
    def getGuns(self):
        return self.guns
    def equippedGun(self):
        return self.guns[self.gunNum]
    def manageClip(self, delta):
        self.guns[self.gunNum].incrementClip(delta)
    def reloadGun(self):
        equippedGun = self.equippedGun()
        equippedAmmo = equippedGun.getAmmoType()
        delta = equippedGun.getClipSize() - equippedGun.getClipAmmo()
        if delta > 0:
            if delta >= self.ammo[equippedAmmo]:
                delta = self.ammo[equippedAmmo]
            self.manageClip(delta)
            self.ammo[equippedAmmo] -= delta

    def setGunNum(self, newGunNum):
        self.gunNum = newGunNum
    def gunAmount(self):
        return len(self.guns)
    def getAmmoAmount(self, kind):
        return self.ammo[kind]
    def getGunIndex(self, gunName):
        gunNames = self.getGunNames()
        return gunNames.index(gunName)
    def incrementGunNum(self, delta):
        self.gunNum += 1
    def getGunNum(self):
        return self.gunNum
       
class Gun(object):
    def __init__(self, gunName, ammoType, clipSize):
        self.gunName = gunName
        self.ammoType = ammoType
        self.clipSize = clipSize
        self.clip = 0

    def getClipSize(self):
        return self.clipSize
    def getAmmoType(self):
        return self.ammoType
    def getClipAmmo(self):
        return self.clip
    def getName(self):
        return self.gunName
    def incrementClip(self, delta):
        self.clip += delta
        



    
    
