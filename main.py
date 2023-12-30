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

class Obstacles(object):
    def __init__(self, x, y, vel, width, height):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height
        


def redraw_game_window(ball):
    win.blit(bg, (0, 0))
    ball.draw(win)
    pygame.display.update()
    
ball = Ball(100, 370, 65)

run = True
while run:
    
    clock.tick(len(ball.picload))
    
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
        

    redraw_game_window(ball)

pygame.quit()
