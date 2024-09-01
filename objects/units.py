import pygame
from objects.utils import timer
class baseunit:
    def __init__(self,x=0,y=0,width=100,height=100,image=None,color='red'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.color = color
        self.timer = timer(1)

    def createUnit(self):
        if self.image:
            return pygame.Rect(self.x,self.y,self.width,self.height)
        else:
            return pygame.Rect(self.x,self.y,self.width,self.height)

    def drawUnit(self,screen):
        if self.image:
            screen.blit(self.image,(self.x,self.y))
        else:
            pygame.draw.rect(screen,self.color,self.createUnit())
        self.action = self.timer.clockaction()

    def resizeUnit(self,width,height):
        self.width = width
        self.height = height
        if self.image:
            self.image = pygame.transform.scale(self.image,(width,height))
    def moveUnit(self,x,y):
        self.x = x
        self.y = y