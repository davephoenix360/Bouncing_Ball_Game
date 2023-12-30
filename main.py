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
        
class safeGround(object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def draw(self, win):
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
        safeGrounds += [safeGround(len(safeGrounds)*50, 425, HOLE_WIDTH, GROUND_HEIGHT, (200, 200, 0))]
        totalWidthCovered += HOLE_WIDTH
    
    return safeGrounds

HOLE_WIDTH = 50
GROUND_HEIGHT = 10
ball = Ball(100, 360, 65)
safeGrounds = []

run = True
while run:
    
    clock.tick(len(ball.picload))
    safeGrounds = makeSafeGround(safeGrounds, HOLE_WIDTH, GROUND_HEIGHT, screenwidth)
    
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
