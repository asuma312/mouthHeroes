import time

import pygame


class button:
    def __init__(self,x,y,width,height,function,color=(0,0,0),text=None,textcolor=(255,255,255),font=None,fontsize=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.function = function
        self.textcolor = textcolor
        self.font = font
        self.fontsize = fontsize
        self.rect = self.createButton()
        self.pressing = False
        self.clicked = False

    def createButton(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)

    def drawButton(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
        if self.text:
            font = pygame.font.Font(self.font,self.fontsize)
            text = font.render(self.text,True,self.textcolor)
            textrect = text.get_rect()
            textrect.center = (self.x+self.width//2,self.y+self.height//2)
            screen.blit(text,textrect)


    def isClicked(self,pos,event):
        self.buttonclicked = 0
        if self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.pressing = True
            self.clicked = False
        if self.pressing and event.type == pygame.MOUSEBUTTONUP:
            self.clicked = True
            self.pressing = False
        self.callBack()

    def callBack(self):
        if self.clicked:
            self.function()
            self.clicked = False
            self.pressing = False
            return True
        return False

class timer:
    def __init__(self,endtime):
        self.endtime = endtime
        self.prevtime = time.time()
        self.timepassed = 0

    def clock(self):
        now = time.time()
        dt = now - self.prevtime
        self.prevtime = now
        self.timepassed += dt

    def clockaction(self):
        self.clock()
        if self.timepassed >= self.endtime:
            self.timepassed = 0
            return True
        return False

class clickObj:

    def __init__(self,rect,clickcallback=None,holdcallback=None,clickargs=None,holdargs=None):
        self.pressing = False
        self.clicked = False
        self.rect = rect
        self.clickcallback = clickcallback
        self.clickargs = clickargs
        self.holdcallback = holdcallback
        self.holdargs = holdargs

    def detectClick(self,pos,event):
        self.clickFunction(pos,event)
        if self.holdcallback:
            self.holdFunction(pos, event)

    def clickFunction(self,pos,event):
        if self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.pressing = True
            self.clicked = False
        if self.pressing and event.type == pygame.MOUSEBUTTONUP:
            self.clicked = True
            self.pressing = False
        self.clickCallback()

    def clickCallback(self):
        if self.clicked:
            if not self.clickcallback:
                print('Clicked')
            else:
                self.callback(self.clickcallback,self.clickargs)
            self.clicked = False
            self.pressing = False
            return True
        return False


    def holdFunction(self,pos,event):
        if self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN:
            self.pressing = True
            self.clicked = False
        if self.pressing and not event.type == pygame.MOUSEBUTTONUP:
            self.holdCallback()
        else:
            self.pressing = False


    def holdCallback(self):
        if not self.holdcallback:
            print('Holding')
        else:
            self.callback(self.holdcallback,self.holdargs)

    def callback(self, function, args):
        if args is not None:
            args_tuple = tuple(args)
            function(*args_tuple)
        else:
            function()
