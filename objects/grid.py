import pygame
from objects.utils import clickObj

class grid:
    def __init__(self,gridsize,gridwidth,screen,x,y,gridcolor,clickfunction=None,holdfunction=None,colored=False):
        self.gridsize = gridsize
        self.gridwidth = gridwidth
        self.screen = screen
        self.colored = colored
        self.gridcolor = gridcolor
        self.grid = self.createGrid(x,y)
        self.unit = None
        self.clickobj = clickObj(self.grid,clickfunction,holdfunction)



    def drawGrid(self,screen):
        if self.colored:
            pygame.draw.rect(screen,self.gridcolor,self.grid)
        else:
            pygame.draw.rect(screen,self.gridcolor,self.grid,width=1)

    def updateClickFunction(self,function,args):
        self.clickobj.clickcallback = function
        self.clickobj.clickargs = args
        print(args)

    def updateHoldFunction(self,function,args):
        self.clickobj.holdcallback = function
        self.clickobj.holdargs = args

    def createGrid(self,x,y):
        rect = pygame.Rect(x,y,self.gridsize,self.gridsize)
        return rect

    def isClicked(self,pos,event):
        self.clickobj.detectClick(pos,event)
    def setupUnit(self,unit):
        self.unit = unit

class gridController:
    def __init__(self,screen,startx=0,starty=0):
        self.grids = []
        self.screen = screen
        self.startx = startx
        self.starty = starty
    def addGrid(self,grid):
        self.grids.append(grid)

    def drawGrids(self):
        for grid in self.grids:
            grid.drawGrid(grid.screen)
            if grid.unit:
                grid.unit.drawUnit(grid.screen)

    def createGrid(self,gridwidth,gridheight,screen,x,y,gridcolor='white',colored=False):
        x = x + self.startx
        y = y + self.starty
        gridobj = grid(gridwidth,gridheight,screen,x,y,gridcolor,colored)
        self.addGrid(gridobj)
        return gridobj

    def addUnitOnGrid(self,unit,gridindex=-1):
        if gridindex == -1:
            lastgrid = [g for g in self.grids if not g.unit]
            if len(lastgrid)<1:
                #arrumar dps
                raise Exception('No grid available')
            lastgrid = lastgrid[0]
            gridindex = self.grids.index(lastgrid)
        #depois dscobrir pq tem q dividir por 2
        unit.moveUnit(lastgrid.grid.x,lastgrid.grid.y)
        unit.resizeUnit(lastgrid.grid.width,lastgrid.grid.height // 2)
        lastgrid.setupUnit(unit)
        return gridindex

    def setupClickFunction(self,function,args,gridobj:grid):
        gridobj.updateClickFunction(function,args)

    def setupHoldFunction(self,function,args,gridindex):
        grid = self.grids[gridindex]
        grid.updateHoldFunction(function,args)

    def createGridBasedOnSize(self,width,height,qtdxy=None,widthheight=None):
        if not qtdxy and not widthheight:
            raise Exception('You must provide either a tuple telling quantity for x and y or height and width')
        if qtdxy:
            qtdx = qtdxy[0]
            qtdy = qtdxy[1]
            gridwidth = width//qtdx
            gridheight = height//qtdy
            for x in range(qtdx):
                for y in range(qtdy):
                    self.createGrid(gridwidth,gridheight,self.screen,x*gridwidth,y*gridheight)
            return self.grids
        if widthheight:
            gridwidth = widthheight[0]
            gridheight = widthheight[1]
            qtdx = width//gridwidth
            qtdy = height//gridheight
            for x in range(qtdx):
                for y in range(qtdy):
                    self.createGrid(gridwidth,gridheight,self.screen,x*gridwidth,y*gridheight)
            return self.grids
        if widthheight and qtdxy:
            gridwidth = widthheight[0]
            gridheight = widthheight[1]
            qtdx = qtdxy[0]
            qtdy = qtdxy[1]
            for x in range(qtdx):
                for y in range(qtdy):
                    self.createGrid(gridwidth,gridheight,self.screen,x*gridwidth,y*gridheight)
            return self.grids
        return self.grids

    def dectecClickOnGrid(self,pos,event):
        for grid in self.grids:
            grid.isClicked(pos,event)
        return