import pygame
pygame.init()

screenwidth, screenheight = (1200, 500)

win = pygame.display.set_mode((screenwidth, screenheight))

pygame.display.set_caption("Bouncing Ball Game")
bg = pygame.image.load('Backgrounds/background1.png')

clock = pygame.time.Clock() 

class Ball(object):
    def __init__(self, x, y, diameter):
        self.x = x
        self.y = y
        self.diameter = diameter
        self.vel = 5
        self.picload = 16*[pygame.image.load('Characters/red1.png'), pygame.image.load('Characters/red2.png'), pygame.image.load('Characters/red3.png'), pygame.image.load('Characters/red4.png')]
        self.rollCount = 0
        self.isMovingLeft = False
        self.isMovingRight = False
        self.isJump = False
        self.jumpCount = 20
        
        
    def draw(self, win):
        
        if self.isMovingRight:
            self.rollCount += 1
            if self.x < screenwidth - self.diameter:
                self.x += self.vel
            
        elif self.isMovingLeft:
            self.rollCount -= 1 
            if self.x > 0:
                self.x -= self.vel
            
        else:
            self.rollCount = 0
    
        self.rollCount %= len(self.picload)
        win.blit(self.picload[self.rollCount], (self.x, self.y))
        #pygame.draw.rect(win, (0, 0, 0), self.hitbox)
        
    
    def fell(self, win):
        font2 = pygame.font.SysFont('comicsans', 20, True)
        text2 = font2.render('You fell in a hole', 1, (255, 0, 0))
        win.blit(text2, (screenwidth/2 - (text2.get_width()/2), screenheight/2 - (text2.get_height()/2)))
        
class safeGround(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True
        
    def draw(self, win):
        if self.visible:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        

""" class Obstacles(object):
    def __init__(self, x, y, vel, width, height):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height
        
    def draw(self):
        
        pass """


def redraw_game_window(ball, safeGrounds):
    win.blit(bg, (0, 0))
    ball.draw(win)
    
    for safeG in safeGrounds:
        safeG.draw(win)
    
    pygame.display.update()
    
def makeSafeGround(safeGrounds, HOLE_WIDTH, GROUND_HEIGHT, screenwidth):
    totalWidthCovered = 0
    for safeG in safeGrounds:
        totalWidthCovered += safeG.width

    while totalWidthCovered != screenwidth:
        safeGrounds += [safeGround(len(safeGrounds)*HOLE_WIDTH, 425, HOLE_WIDTH, GROUND_HEIGHT, (200, 200, 0))]
        totalWidthCovered += HOLE_WIDTH
    
    return safeGrounds

font = pygame.font.SysFont('comicsans', 20, True)
HOLE_WIDTH = 80
GROUND_HEIGHT = 10
ball = Ball(100, 360, 65)
safeGrounds = []
holesCheck = [True]*int(screenwidth/HOLE_WIDTH)
level = 0 # This controls the speed of the holes on floor
holeControl = -1 * (20-level)


run = True
while run:
    
    clock.tick(len(ball.picload))
    
    # Ground Controller
    safeGrounds = makeSafeGround(safeGrounds, HOLE_WIDTH, GROUND_HEIGHT, screenwidth)
    holesCheck = [True]*int(screenwidth/HOLE_WIDTH)
    
    if holeControl <= ((len(holesCheck) * -1) + 1) * (20-level):
        holeControl = ((holeControl * -1)/(20-level)) % (len(holesCheck))
        holeControl = -1 * holeControl
    
    holesCheck[int(holeControl/(20-level))] = False
    holeControl -= 1
    
    for i in range(len(holesCheck)):
        if holesCheck[i] == False:
            safeGrounds[i].visible = False 
        else:
            safeGrounds[i].visible = True
    
    # End of Ground Controller
    
    actualHole = safeGrounds[holesCheck.index(False)]
    if (ball.y + ball.diameter + 2) > actualHole.y and (ball.x + ball.diameter > actualHole.x + actualHole.width/2) and (ball.x < actualHole.x + actualHole.width/2):
        print('fell', actualHole.x, actualHole.y)
        print('ball', ball.x, ball.y)
        #ball.fell(win)
        pass
        
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if not(ball.isJump):
        if keys[pygame.K_UP]:
            ball.isJump = True
            
    else:
        if ball.jumpCount >= -20:

            control = 1
            
            if ball.jumpCount < 0:
                control = -1
                
            if ball.y - (control * (ball.jumpCount ** 2) * 0.05) > 0:
                ball.y -= (control * (ball.jumpCount ** 2) * 0.05)
            
            else:
                ball.jumpCount = -1 * ball.jumpCount
            
            ball.jumpCount -= 1
        
        else:
            ball.jumpCount = 20
            ball.isJump = False
            
        
    if keys[pygame.K_RIGHT]:
        ball.isMovingRight = True
        ball.isMovingLeft = False
        
    elif keys[pygame.K_LEFT]:
        ball.isMovingRight = False
        ball.isMovingLeft = True
        
    else:
        ball.isMovingRight = False
        ball.isMovingLeft = False
        

    redraw_game_window(ball, safeGrounds)

pygame.quit()
