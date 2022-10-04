class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.ay = 0
        self.width = width
        self.height = height
        self.speed = 10
        self.jumpCount = 10
        self.boostCount = 0
        self.totalBoost = 0
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.isJump = False
        self.isBoost = False
        self.isOnGround = False
        self.fall = 0
        self.gameOver = False
        self.fly = False
        self.win = False

        self.hitbox = pygame.Rect(self.x + 10, self.y + 5, 40, 125)

    def move(self, keys):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if keys[pygame.K_LEFT] and self.x > self.speed:
            #print('left')
            self.x -= self.speed
            self.standing = False
            self.right = False
            self.left = True

        elif keys[pygame.K_RIGHT] and self.x < 576 - self.width - self.speed:
            #print('right')
            self.x += self.speed
            self.standing = False
            self.left = False
            self.right = True

        elif not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.left = False
            self.right = False

    def update(self):
        if self.win != True:
            self.ay = ground.y - self.y
        if sky.y != 0 and not self.win:
            self.y += y_scroll
        self.hitbox = pygame.Rect(self.x + 10, self.y + 5, 40, 125)

    def draw(self, win):
        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.standing:
            win.blit(char[0], (self.x, self.y))
        else:
            win.blit(char[1], (self.x, self.y))

        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


class platform(object):
    def __init__(self, distance, p_iter):
        self.active = True
        self.floatCount = random.randint(0, 8)
        self.distance = distance
        self.p_iter = p_iter
        self.dx = random.randrange(-1, 2, 2)
        
        if p_iter == 1:
            self.ay = child.ay + self.distance
        else:
            self.ay = clouds[self.p_iter-1].ay + self.distance * 3

        if (self.ay >= 2300) and (self.ay <= 4600):
            self.p_type = 2
            self.boost = 11
        elif (self.ay > 4600) and (self.ay <= 6900):
            self.p_type = 3
            self.boost = 13
        elif (self.ay > 6900):
            self.p_type = 4
            self.boost = 14
        else:
            self.p_type = 1
            self.boost = 10  

        self.y = (ground.y - self.ay)
        self.find_type() 

        self.ran = game.ran


        if self.p_type == 1:
            self.x = int(math.sin((self.y-330)/(230 + self.ran)) * 300 + 293)
        elif self.p_type == 2:
            self.x = int(math.sin((self.y-800)/(300 + self.ran)) * 300 + 293)
        elif self.p_type == 3:
            self.x = int(math.sin((self.y-330)/(150 + self.ran)) * 300 + 293)
        elif self.p_type == 4:
            self.x = int(math.sin((self.y-330)/(100)) * 300 + 293)



        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def find_type(self):
        if self.p_type == 1:
            self.width = 24*2
            self.height = 18*2
        elif self.p_type == 2:
            self.width = 24*2
            self.height = 18*2
            self.vari = random.randint(1, 3)
        elif self.p_type == 3:
            self.width = 41*2
            self.height = 8 
            self.vari = random.randint(1,2)
        elif self.p_type == 4:  
            self.width = 26*2
            self.height = 16*2

    def update(self):
        self.ay = ground.y - self.y
        if self.active:
            self.y += 1
            self.y += y_scroll
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            if self.floatCount + 1 >= 21:
                self.floatCount = 0
            if self.p_type == 2:
                if self.x + self.width > 600:
                    self.x -= 1
                for i in range(1,5):
                    clouds[i+self.p_iter].active = False
                    if clouds[self.p_iter + i].p_type == 3 and clouds[self.p_iter + i].x < 0:
                        clouds[self.p_iter + i].x = 0
                    elif clouds[self.p_iter + i].p_type == 3 and clouds[self.p_iter + i].x + clouds[self.p_iter +i].width > 600:
                        clouds[self.p_iter + i].x = 600
                    else:
                        break
            if self.p_type == 3 and clouds[self.p_iter-2].p_type != 2:
                if self.x + self.width >= 600:
                    self.dx = -4
                elif self.x <= 0:
                    self.dx = 4
                self.x += self.dx
                for i in range(1,2):
                    clouds[i+self.p_iter].active = False
            if self.p_type == 4:
                if self.x + self.width >= 600:
                    self.dx = -6
                elif self.x <= 0:
                    self.dx = 6
                self.x += self.dx
                for i in range(1,4):
                    if i + self.p_iter < len(clouds):
                        clouds[i+self.p_iter].active = False
            colis = self.hitbox.colliderect(child.hitbox)
            #print(colis)
            if (colis == True) and (child.isBoost == False):
                child.isJump = False
                child.isBoost = True
                child.boostCount = self.boost                                                                                                                                               
                colis == False
                child.totalBoost = self.boost
                child.fall = 0
                self.active = False
            elif (colis == True) and (child.isBoost == True):
                child.boostCount = self.boost
                colis == False
                child.totalBoost = self.boost
                child.fall = 0
                self.active = False



        #     child.boostCount = self.boost / 5
        #     if (child.boostCount >= (-self.boost)) and (child.isBoost == False):
        #         neg = 1
        #     if child.boostCount < 0:
        #         neg = -1
        #     child.y -= (child.boostCount ** 2) * 0.35 * neg 
        #     child.boostCount -= 1
        # else:
        #     child.isBoost = False
        #     child.boostCount = 10
            
    #MARKED
    def find_range(self):
        if self.p_iter == 0:
            min_d = (random.randint(int(child.jumpCount/3), int(child.jumpCount/2)) + 10) * 2
            return min_d 
        elif self.p_iter > 0:
            min_d = random.randint(int(self.distance/3), int(self.boost)) * 2
            return min_d
    #MARKED

    def draw(self, win):
        if self.active:
            if self.p_type == 1:
                win.blit(wind[self.floatCount//3], (self.x, self.y))
                self.floatCount += 1
            elif self.p_type == 2:
                win.blit(cloudPF[self.vari], (self.x, self.y))
            elif self.p_type == 3:
                win.blit(thin[self.vari], (self.x, self.y))
            else:
                win.blit(ufo, (self.x, self.y))
            #draw in sprite
            #pygame.draw.rect(win, (255,255,255,255), self.hitbox, 2)


class floor(object):
    def __init__(self, x, y, width, height, vari):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vari = vari
        self.hitbox = (self.x, self.y, width, height)
        if self.vari == 2:
            self.ay = ground.y - self.y

    def update(self):
        self.y += y_scroll
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 1)

        colis = self.hitbox.colliderect(child.hitbox)
        if self.vari == 1:
            if colis and child.isJump == False:
                child.isOnGround = True
                child.fall = 0
            else:
                child.isOnGround = False
            self.rect = pygame.Rect(self.hitbox)
        if self.vari == 2:
            if colis == True:
                child.win = True
            win.blit(top, (self.x, self.y))


class dec(object):
    def __init__ (self, x, ay, d_type, dx):
        self.x = x
        self.ay = ay
        self.d_type = d_type
        self.dx = dx
        self.y = ground.y - self.ay
        self.flyCount = 0
        self.visible = False
        self.vel_def()

    def vel_def(self):
        if self.d_type == 1:
            self.vel = 10
            self.d_type = 1
        else:
            self.vel = 20
            self.d_type == 2

    def update(self):
        self.y = ground.y - self.ay
        if (child.ay + 924 >= self.ay):
            self.visible = True
            self.y += y_scroll
        else:
            self.visible = False

        if self.visible == True:
            if self.dx >= 0:
                self.x += 1
            else:
                self.x -= 1
            
    def draw(self, win):
        if self.visible == True:
            if self.flyCount + 1 >= 9:
                self.flyCount = 0
            if self.d_type == 1:
                if self.dx > 0:
                    #print('drawing type 1, right ' + str(self.x) + ' ' + str(self.y))
                    #pygame.draw.rect(win, (255,0,0), (self.x, self.y , 10, 10))
                    win.blit(birdRight[self.flyCount//3], (self.x, self.y))
                    self.flyCount += 1 
                elif self.dx < 0:
                    #print('drawing type 1, left' + str(self.x) + ' ' + str(self.y))
                    #pygame.draw.rect(win, (255,255,0), (self.x, self.y , 10, 10))
                    win.blit(birdLeft[self.flyCount//3], (self.x, self.y))
                    self.flyCount += 1
                else:
                    print('not sucessful')
            elif self.d_type == 2:
                if self.dx > 0:
                    #print('drawing type 2, right' + str(self.x) + ' ' + str(self.y))
                    #pygame.draw.rect(win, (255,0,0), (self.x, self.y , 30, 10))
                    win.blit(planeRight, (self.x, self.y))
                    self.flyCount += 1 
                elif self.dx < 0:
                    #print('drawing type 2, left' + str(self.x) + ' ' + str(self.y))
                    #pygame.draw.rect(win, (255,255,0), (self.x, self.y , 30, 10))
                    win.blit(planeLeft, (self.x, self.y))
                    self.flyCount += 1
                else:
                    print('not sucessful')

class button():
    def __init__(self, image, x, y, b_type):
        self.image = image
        self.x = x
        self.y = y
        self.b_type = b_type
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.show = True

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if (pygame.mouse.get_pressed()[0] == 1) and (self.clicked == False):
                self.clicked = True
                self.show = False
                if self.b_type == 'start':
                    game.main = True
                    game.menu = False
                elif self.b_type == 'esc':
                    game.main = False
                    game.menu = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            self.show = True

        if self.show:
            win.blit(self.image, (self.rect))

class status():
    def __init__(self, run, menu, main):
        self.run = run
        self.menu = menu
        self.main = main

    def update(self):
        if self.menu == True:
            self.main = False

        elif self.main == True:
            self.menu = False


def drawGame():
    win.blit(bg, (0, winSize[1]-2900*2 + child.ay/2))
    child.move(keys)
    child.update()
    child.draw(win)
    ground.update()
    sky.update()
    detectFall()
    if not child.gameOver:
        genPlatform()

    #cx = math.sin((child.y-150)/100) * 300 + 293
    #print(cx, child.y)
    #pygame.draw.rect(win, (255, 0, 0), (cx, child.y-30, 10, 10))
    for i in clouds.values():
        i.update()
        i.draw(win)
        if i.active == False:
            del i
    for i in decs.values():
        i.update()
        i.draw(win)

    #print(child.ay)
    pygame.display.update()

def genPlatform():
    clouds.setdefault(1, platform(child.jumpCount*1.8, 1))
    while not clouds[len(clouds)].ay > sky.ay:
        i = len(clouds) + 1
        clouds.setdefault(i, platform(clouds[i-1].distance, i))
        #print(clouds[i].x, clouds[i].y)
        pygame.draw.rect(win, (255, 0, 0), (clouds[i].hitbox))



def genDec():
    ci = 0
    for ay in range(500, 4000, 200):
        ci += 1
        d_type = random.randint(1, 6)
        dx = random.randrange(-1, 3, 2)
        if dx > 0:
            x = random.randint(0, 600/2)
        else:
            x = random.randint(600/2, 600)
        decs[ci] = dec(x, ay, d_type, dx)
        #print(decs[ci].x, decs[ci].ay, decs[ci].d_type, decs[ci].dx)

def detectFall():
    if child.fall >= 700:
        clouds.clear()
        child.gameOver = True
    if child.gameOver == True:
        game.main = False
        game.menu = True

def upscale(image, scale):
    image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
    return image


# def checkColis():
#     #hitbox_.append(child.x)
#     #hitbox_.append(child.y)

def drawMain():
    win.blit(bg0, (0, 0))

        
    bSkins.draw()
    bNight.draw()
    bRecords.draw()
    bStart.draw()




import pygame, math, random, os

pygame.init()
#====================================================================
#--------------------------------------------------------------------

# Load In assets
fn = 'assets/'
bg0 = pygame.image.load(fn + 'home_in.png')
b_skins = pygame.image.load(fn + 'b1.png')
b_night = pygame.image.load(fn + 'b2.png')
b_records = pygame.image.load(fn + 'b3.png')
b_start = pygame.image.load(fn + 'bstart.png')

bg0 = upscale(bg0, 4)
b_skins = upscale(b_skins, 4)
b_night = upscale(b_night, 4)
b_records = upscale(b_records, 4)
b_start = upscale(b_start, 4)

startAni = [pygame.image.load(fn + 'startAnimation1.png'), pygame.image.load(fn + 'startAnimation2.png'), pygame.image.load(fn + 'startAnimation3.png'), pygame.image.load(fn + 'startAnimation4.png'), pygame.image.load(fn + 'startAnimation5.png'), pygame.image.load(fn + 'startAnimation6.png'), pygame.image.load(fn + 'startAnimation7.png'), pygame.image.load(fn + 'startAnimation8.png'), pygame.image.load(fn + 'startAnimation9.png'), pygame.image.load(fn + 'startAnimation10.png'), pygame.image.load(fn + 'startAnimation11.png'), pygame.image.load(fn + 'startAnimation12.png'), pygame.image.load(fn + 'startAnimation13.png'), pygame.image.load(fn + 'startAnimation14.png')]
idleAni = [pygame.image.load(fn + 'mainscreen_idle1.png'), pygame.image.load(fn + 'mainscreen_idle2.png'), pygame.image.load(fn + 'mainscreen_idle3.png'), pygame.image.load(fn + 'mainscreen_idle4.png')]

for i in startAni:
    startAni[startAni.index(i)] = upscale(i, 4)
for i in idleAni:
    idleAni[idleAni.index(i)] = upscale(i, 4)
#--------------------------------------------------------------------
bg = pygame.image.load(fn + 'background.png')
char = [pygame.image.load(fn + 'player_idle.png'), pygame.image.load(fn + 'player_n.png')]
walkRight = [pygame.image.load(fn + 'player_Rwalk1.png'), pygame.image.load(fn + 'player_Rwalk2.png'), pygame.image.load(fn + 'player_Rwalk3.png'), pygame.image.load(fn + 'player_Rwalk4.png')]
walkLeft = [pygame.image.load(fn + 'player_Lwalk1.png'), pygame.image.load(fn + 'player_Lwalk2.png'), pygame.image.load(fn + 'player_Lwalk3.png'), pygame.image.load(fn + 'player_Lwalk4.png')]
birdRight = [pygame.image.load(fn + 'bird1.png'), pygame.image.load(fn + 'bird2.png'), pygame.image.load(fn + 'bird3.png')]
birdLeft = []
for i in range(len(birdRight)):
    birdLeft.append(pygame.transform.flip(birdRight[i-1], True, False))
planeRight = pygame.image.load(fn + 'airplane.png')
planeLeft = pygame.transform.flip(planeRight, True, False)
wind = [pygame.image.load(fn + 'wind1.png'), pygame.image.load(fn + 'wind2.png'), pygame.image.load(fn + 'wind3.png'), pygame.image.load(fn + 'wind4.png'), pygame.image.load(fn + 'wind5.png'), pygame.image.load(fn + 'wind6.png'), pygame.image.load(fn + 'wind7.png')]
cloudPF = [pygame.image.load(fn + 'cloudPF1.png'), pygame.image.load(fn + 'cloudPF2.png'), pygame.image.load(fn + 'cloudPF3.png'), pygame.image.load(fn + 'cloudPF4.png')]
thin = [pygame.image.load(fn + 'thin1.png'), pygame.image.load(fn + 'thin2.png'), pygame.image.load(fn + 'thin3.png')]
ufo = pygame.image.load(fn + 'finalPF.png')
top = pygame.image.load(fn + 'top.png')
winMes = pygame.image.load(fn + 'winMes.png')
esc = pygame.image.load(fn + 'b_esc.png')

bg = pygame.transform.scale2x(bg)
planeRight = pygame.transform.scale2x(planeRight)
planeLeft = pygame.transform.scale2x(planeLeft)
ufo = pygame.transform.scale2x(ufo)
top = pygame.transform.scale2x(top)
winMes = upscale(winMes, 8)
esc = upscale(esc, 3)


for i in range(len(thin)):
    thin[i] = pygame.transform.scale2x(thin[i])
for i in range(len(cloudPF)):
    cloudPF[i] = pygame.transform.scale2x(cloudPF[i])
for i in range(len(wind)):
    wind[i] = pygame.transform.scale2x(wind[i])
for i in range(len(birdRight)):
    birdRight[i] = pygame.transform.scale2x(birdRight[i])
for i in range(len(birdLeft)):
    birdLeft[i] = pygame.transform.scale2x(birdLeft[i])
for i in range(len(walkRight)):
    walkRight[i] = pygame.transform.scale2x(walkRight[i])
for i in range(len(walkLeft)):
    walkLeft[i] = pygame.transform.scale2x(walkLeft[i])
for i in range(len(char)):
    char[i] = pygame.transform.scale2x(char[i])



#=======================================================================
game = status(True, True, False)
transWin = (600, 924)
startWin = (216*4, 106*4)
winSize = (600, 824)
betwWin = (abs(int((winSize[0]-startWin[0])/2)), abs(int((winSize[1]-startWin[1])/2)))
while game.run == True:
    # Main Loop
    if game.menu:
        win = pygame.display.set_mode((startWin))
        bSkins = button(b_skins, 20, 136, 'skin')
        bNight = button(b_night, 20, 196, 's_night')
        bRecords = button(b_records, 20, 256, 'records')
        bStart = button(b_start, 16, 328, 'start')
        pygame.display.set_caption('Starting Menu')
        clock = pygame.time.Clock()
        idle = 0
        idle2 = 0
        

        while game.menu == True and game.run:

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.run = False

            drawMain()

            if idle + 1 < 14*4:
                idle += 1
                win.blit(startAni[int(idle/4)], (0, 0))
            elif idle + 1 == 14*4:
                win.blit(startAni[int(idle/4)], (0, 0))
                idle += 1
            else:
                idle2 += 1
                win.blit(idleAni[int(idle2/60)], (0, 0))
                if idle2 + 1 == 4*60:
                    idle2 = 0


            pygame.display.update()
            win.fill((0,0,0))

            game.update()




    elif game.main == True:
        win = pygame.display.set_mode((winSize))
        pygame.display.set_caption('Main Game')
        clock = pygame.time.Clock()
        game.ran = random.randint(0, 500)

        ground = floor(-10, winSize[1]-144, 1000, 200, 1)
        sky = floor(0, -8400-300, 600, 200, 2)
        child = player(30, ground.y, 32, 64)
        clouds = {}
        #clouds[0] = platform(random.randint(100,824), child.jumpCount)
        decs = {}
        genPlatform()
        genDec()
        y_scroll = 0
        #====================================================================
        while game.main and game.run:
        #====================================================================
            clock.tick(24)          # This is in mili-second
            y_scroll = 924 - 250 - child.y
            #print(child.ay)
            if not child.win:     
                keys = pygame.key.get_pressed()
            #print(ground.hitbox)

            print(child.y)

            # child.locate()
        #====================================================================

        #====================================================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.run = False
        #--------------------------------------------------------------------

            # for obj in decs:
            #     if obj.visible == False:
            #         decs.pop(decs.index(obj))

            if (child.isJump == False) and (child.isOnGround == True):
                if keys[pygame.K_UP]:
                    child.isJump = True
                    child.walkCount = 0
            elif child.isJump == True:
                if child.jumpCount >= -10 and child.isBoost != True:
                    neg = 1
                    if child.jumpCount < 0:
                        neg = -1
                    if (child.y - ((child.jumpCount ** 2) * 0.35 * neg)) >= ground.y:
                        child.y = ground.y
                        child.ax = 0
                        child.isJump = False
                        child.jumpCount = 10
                        pass
                    else:
                        child.y -= (child.jumpCount ** 2) * 0.35 * neg
                        child.jumpCount -= 1
                else:
                    child.isJump = False
                    child.jumpCount = 10


            if child.isBoost == True:
                child.isJump = False
                if child.boostCount < 0:
                    neg = -1
                else:
                    neg = 1
                child.y -= (child.boostCount ** 2) * 0.35 * neg
                child.boostCount -= 1
                if child.boostCount <= (-child.totalBoost):
                    child.boostCount = 0
                    child.isBoost = False

            if (child.isBoost == False) and (child.isJump == False) and (child.fly == False):
                if (child.y - ((child.totalBoost ** 2) * 0.35 * -1)) >= ground.y:
                    child.y = ground.y
                else:
                    child.y -= (child.totalBoost ** 2) * 0.35 * -1
                    child.fall += (child.totalBoost ** 2) * 0.35 * 1

            # colis = floor.rect.colliderect(child.rect)
            # print(colis)
            # if colis:
            #     child.isOnGround = True
            # else:
            #     child.isOnGround = False
            # if keys[pygame.K_UP]:
            #     child.y -= child.jumpCount

            if keys[pygame.K_ESCAPE]:
                game.menu = True
                game.main = False

            # if keys[pygame.K_DOWN]:
            #     #child.y += child.jumpCount
            #     child.y += 50

            # if keys[pygame.K_SPACE]:
            #     child.fly = True
            #     child.fall = 0
            #     child.y -= 50
            # else:
            #     child.fly = False


            if child.win == True:
                child.y -= 1
                child.fall = 0
                win.blit(winMes, (20, 450))
                bEsc = button(esc, 20, 450-winMes.get_height(), 'esc')
                pygame.display.update()
                while game.main:

                    keys = pygame.key.get_pressed()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game.main = False
                            break

                    if keys[pygame.K_ESCAPE]:
                        game.menu = True
                        game.main = False
                        

                    bEsc.draw()
                    game.update()
                    pygame.display.update()

                    # if i >= 50:
                    #     child.win = False
                    #     game.menu = True
                    #     game.main = False



            win.fill((0,0,0))
        #--------------------------------------------------------------------
        #====================================================================

        #====================================================================
            drawGame()

            game.update()
            pygame.display.update()

        pygame.quit()
