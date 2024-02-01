##########################################################
#MAZE GENERATION FILE FOR CURSORS.112

# For the maze generation/solving function, I used the DFS algorithm and 
# referenced the psuedocode from these sources: 

# https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap.html
# https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# https://www.cs.cmu.edu/~112/notes/student-tp-guides/Mazes.pdf
# https://en.wikipedia.org/wiki/Depth-first_search

##########################################################

from cmu_112_graphics import *
import random 
import copy

##########################################################
#MAZE CLASS
##########################################################

class maze: 

    moves = [(0, 1), (1, 0), (-1, 0), (0, -1)] #right, down, up, left

    def __init__(self, rows, cols, offset):
        self.rows = rows
        self.cols = cols
        self.list = [([0] * self.cols) for row in range(self.rows)]
        self.margin = 10
        self.order = [(0, 0)]
        self.endCol = self.cols-1
        self.endRow = self.rows-1
        self.checkFirstMove = True
        self.offset = offset
        self.loop = False
        self.wrong = dict()

    def modMaze(self, row, col, dim, val):
        if val == -1: return self.list[row][col][dim]
        elif dim == -1: 
            if col == -1: self.list[row] = val
            else: self.list[row][col] = val
        else: self.list[row][col][dim] = val
    
    def initMaze(self):
        for row in range(self.rows):
            for col in range(self.cols): 
                self.modMaze(row, col, -1, self.createCell())
        self.modMaze(0,0,0,1)
        #print(self.list)

    def createCell(self): 
        return [0, self.margin, self.margin, self.margin, self.margin, False]

    def grow(self):
        self.margin += .05

    def moveMaze(self, move, row, col): #move is a tuple 
        drow, dcol = move
        newR, newC = (row + drow), (col + dcol)
        return newR, newC
    
    def testMove(self, move, row, col):
        drow, dcol = move
        newR, newC = (row + drow), (col + dcol)
        if ((newR < 0) or (newC < 0) or (newR >= self.rows) or 
        (newC >= self.cols) or self.modMaze(newR, newC, 0, -1) != 0):
            return False
        return True
    
    def checkSides(self, startRow, startCol):
        for move in self.moves:
            if self.testMove(move, startRow, startCol):
                return True
        return False
    
    def generateMaze(self, startRow, startCol, num):
        if (startRow == 0) and (startCol == 0) and self.checkFirstMove == False:
            return self.list
        else: 
            self.checkFirstMove = False
            while self.checkSides(startRow, startCol):
                openMoves = []
                for move in self.moves:
                    if self.testMove(move, startRow, startCol):
                        openMoves.append(move)
                nextMove = random.choice(openMoves)
                #print('nextmove', nextMove)
                currRow, currCol = self.moveMaze(nextMove, startRow, startCol)
                self.modMaze(currRow, currCol, 0, num)
                #print(app.maze)
                self.order.append((currRow, currCol))
                self.carveMaze(startRow, startCol, currRow, currCol, nextMove)
                result = self.generateMaze(currRow, currCol, num+1)
                if result != None:
                    return result
                else: 
                    #print('openmoves', openMoves)
                    #print('next:', nextMove)
                    openMoves.pop(openMoves.index(nextMove))
                    if (currRow, currCol) == (self.endRow, self.endCol):
                        self.loop = True
                    elif self.loop == False:
                        while self.order[-1] != (startRow, startCol):
                            self.wrong[self.order.pop()] = (startRow, startCol)
                    elif self.loop == True:
                        while self.order[-1] != (self.endRow, self.endCol):
                            self.wrong[self.order.pop()] = (startRow, startCol)
                    #print('openmoves2', openMoves)
            return None 
    
#########################################################
#NOTES
#if its already in dictioanry, put items to another key and delete dictionary key
#if not in dictionary, map value to key
# square:square before 
# if its not in the order list, go to dict and get square before check if the square before is in the dictionary
# if its not in dictionary, then its an end piece 
# once it gets to a square that is in the order 
# then thats the path 
# same idea as current
# while cell not in order ist 
# check if its in the dictionary 
#############################################################

    def carveMaze(self, startRow, startCol, currRow, currCol, nextMove):
        if nextMove == self.moves[0]: #right
            self.modMaze(startRow, startCol, 1, 0)
            self.modMaze(currRow, currCol, 4, 0)
        elif nextMove == self.moves[1]: #down
            self.modMaze(startRow, startCol, 2, 0)
            self.modMaze(currRow, currCol, 3, 0)
        elif nextMove == self.moves[2]: #up
            self.modMaze(startRow, startCol, 3, 0)
            self.modMaze(currRow, currCol, 2, 0)
        elif nextMove == self.moves[3]: #left 
            self.modMaze(startRow, startCol, 4, 0)
            self.modMaze(currRow, currCol, 1, 0)
    
    def updateMaze(self):
        for row in range(self.rows):
            for col in range(self.cols):
                for i in range(1, 5):
                    if self.modMaze(row, col, i, -1) != 0:
                        self.modMaze(row, col, i, self.margin)

    def findMazeCell(self, row, col, width, height): 
        width = width - (2*self.margin)
        height = height - (2*self.margin)
        return (col*width/self.cols+self.modMaze(row, col, 4, -1)+self.margin, 
        row*(height-self.offset)/self.rows+self.modMaze(row, col, 3, -1)+
        self.offset+self.margin,((col+1)*width/self.cols)-
        self.modMaze(row, col, 1, -1)+self.margin, 
        (row+1)*(height-self.offset)/self.rows-self.modMaze(row, col, 2, -1)
        +self.offset+self.margin)

    def cursorBounds(self, row, col): 
        bounds = []
        for i in range(1, 5): 
            bounds.append(self.modMaze(row, col, i, -1))
        return bounds 

#########################################################
#NOTES
# clockwise, start top left 
# 1: 4, 3
# 2: 3, 1
# 3: 1, 2
# 4: 4, 2

# 1, 2, 3, 4
#right, down, up, left

# -make cell bound
# -draw cell bound
# -check cell bound with event 
#########################################################

    def fillCellEdge(self, row, col, x1, y1, x2, y2): 
        edges = []
        #1
        if (self.modMaze(row, col, 4, -1), self.modMaze(row, col, 3, -1)) == (0,0):
            edges.append((x1, y1, x1+self.margin, y1+self.margin))
        #2
        if (self.modMaze(row, col, 3, -1), self.modMaze(row, col, 1, -1)) == (0,0):
            edges.append((x2-self.margin, y1, x2, y1+self.margin))
        #3
        if (self.modMaze(row, col, 1, -1), self.modMaze(row, col, 2, -1)) == (0,0):
            edges.append((x2-self.margin, y2-self.margin, x2, y2))
        #4
        if (self.modMaze(row, col, 4, -1), self.modMaze(row, col, 2, -1)) == (0,0):
            edges.append((x1, y2-self.margin, x1+self.margin, y2))
        if len(edges) != None: 
            return edges
        return None    

##########################################################
#GENERATE MAZE
##########################################################

def createFreshMaze(app, rows, cols, startRow, startCol):
    app.start = maze(rows, cols, .1*app.height)
    app.start.initMaze()
    app.start.generateMaze(startRow,startCol,2)

##########################################################
#DRAW MAZE (VIEW)
##########################################################
    
def drawEnd(app, canvas):
    x1, y1, x2, y2 = app.start.findMazeCell(app.start.endRow, app.start.endCol,
    app.width, app.height)
    canvas.create_rectangle(x1, y1, x2, y2, fill = '#0d1b2a', width = 0)
    edges = app.start.fillCellEdge(app.start.endRow, app.start.endCol, x1,y1,x2,y2)
    if edges != None:
        for i in edges:
            (a, b, c, d) = i
            canvas.create_rectangle(a, b, c, d, fill = '#415a77', width = 0)
    
def drawStart(app, canvas):
    x1, y1, x2, y2 = app.start.findMazeCell(0, 0, app.width, app.height)
    canvas.create_rectangle(x1, y1, x2, y2, fill = '#ccd5ae', width = 0)

def drawGrid(app, canvas): 
    for row in range(app.start.rows):
        for col in range(app.start.cols): 
            drawCell(app, canvas, row, col)

def drawCell(app, canvas, row, col):
    color = 'white'
    if app.start.modMaze(row,col,5,-1) == True:
        color = "#ccd5ae"
    if (row, col) in app.start.order and app.solution == True:
        color = "#ccd5ae"
    x1, y1, x2, y2 = app.start.findMazeCell(row, col, app.width, app.height)
    canvas.create_rectangle(x1, y1, x2, y2, fill = color,  width = 0)
    edges = app.start.fillCellEdge(row, col, x1,y1,x2,y2)
    if edges != None:
        for i in edges:
            (a, b, c, d) = i
            canvas.create_rectangle(a, b, c, d, fill = '#415a77', width = 0)


def drawMaze(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = '#415a77')
    drawGrid(app, canvas)
    drawEnd(app, canvas)
    drawStart(app, canvas)
    









