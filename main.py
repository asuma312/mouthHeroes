import time
import pygame
from objects.utils import button
from objects.grid import gridController
from units.basesoldier import basesoldier

class mainLoop:
    def __init__(self,fps=60):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

        self.datacontroller = dataController()
        self.screencontroller = screenController()

        menuscreen = menu(screen,self.datacontroller,self.screencontroller)
        gamescreen = maingame(screen,self.datacontroller,self.screencontroller)
        screens = {
            'menu':menuscreen,
            'game':gamescreen
        }
        for item,key in screens.items():
            _dict = {item:key}
            self.screencontroller.addScreen(_dict)


        self.screencontroller.setScreen('menu')

        self.clock = pygame.time.Clock()
        self.fps = fps

    def run(self):
        prev_time = time.time()

        while True:
            now,dt,prev_time = self.timerate(prev_time)
            for event in pygame.event.get():
                self.screencontroller.detectEvents(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screencontroller.run()
            pygame.display.update()
            self.clock.tick(self.fps)


    def timerate(self,prev_time):
        now = time.time()
        dt = now - prev_time
        prev_time = now
        return now,dt,prev_time

class screenController:
    def __init__(self):
        self.screens = {}
        self.currentscreen = None

    def addScreen(self,screen):
        self.screens = {**self.screens,**screen}

    def detectEvents(self,event):
        self.screens[self.currentscreen].detect_events(event)

    def setScreen(self,screen):
        self.currentscreen = screen

    def run(self):
        self.screens[self.currentscreen].run()

class dataController:
    def __init__(self):
        pass


class menu:
    def __init__(self,screen,datacontroller,screencontroller):
        self.datacontroller = datacontroller
        self.screencontroller = screencontroller
        self.screen = screen
        self.pbutton = self.printButton()


    def main(self):
        self.backgroundcolor = 'yellow'
        self.screen.fill(self.backgroundcolor)
        self.pbutton.drawButton(self.screen)


    def run(self):
        self.main()


    def detect_events(self, event):
        self.pbutton.isClicked(pygame.mouse.get_pos(),event)

    def printButton(self):
        def printtext():
            print('Changing to game')
            self.screencontroller.setScreen('game')
        newbutton = button(100,100,100,100,printtext)
        return newbutton

class maingame:
    def __init__(self,screen,datacontroller,screencontroller):
        self.datacontroller = datacontroller
        self.screencontroller = screencontroller
        self.screen = screen

        self.sidebar = self.sideBar(screen)

    def main(self):
        self.backgroundcolor = 'green'
        self.screen.fill(self.backgroundcolor)
        self.sidebar.draw()

    def run(self):
        self.main()

    def detect_events(self, event):
        self.sidebar.sidebarGrids.dectecClickOnGrid(pygame.mouse.get_pos(),event)


    class sideBar:
        def __init__(self,screen):
            self.screen = screen
            maxwidth = self.screen.get_width() * 0.3
            maxheight = self.screen.get_height()
            sidebarx = self.screen.get_width() - maxwidth
            sidebary = 0
            self.color = 'blue'
            self.rect = pygame.Rect(sidebarx,sidebary,maxwidth,maxheight)
            self.units = [basesoldier]
            self.sidebarGrids = self.sideBarGrid()

        def sideBarGrid(self):
            qtdgridsx = 2
            qtdgridsy = 10

            gridcontroler = gridController(self.screen,startx=self.rect.x,starty=self.rect.y)
            gridcontroler.createGridBasedOnSize(self.rect.width,self.rect.height,(qtdgridsx,qtdgridsy))
            for unit in self.units:
                gridindex = gridcontroler.addUnitOnGrid(unit())
                grid = gridcontroler.grids[gridindex]
                gridcontroler.setupClickFunction(self.sidebarFunction,(grid,'test'),grid)
            return gridcontroler

        def sidebarFunction(self,grid,test):
            print('Clicked on sidebar gqqrid')
            return


        def draw(self):
            pygame.draw.rect(self.screen,self.color,self.rect)
            self.sidebarGrids.drawGrids()



if __name__ == '__main__':

    main = mainLoop()
    main.run()