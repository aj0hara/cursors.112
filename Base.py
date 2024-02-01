##########################################################
#BASE FILE FOR CURSORS.112
##########################################################

from cmu_112_graphics import *
from MazeGen import *

##########################################################
#APP OBJECT INITATION (MODEL)
##########################################################

def appStarted(app):
    app.start = None
    createFreshMaze(app, 10, 10, 0, 0)
    app.startWid = app.width
    app.startHei = app.height
    x1,y1,x2,y2 = app.start.findMazeCell(0,0,app.width,app.height)
    app.cx = x1 + (x2-x1)/2
    app.cy = y1 + (y2-y1)/2
    app.rad = 5
    app.edge = app.start.margin*2
    app.solution = False
    app.play = False
    app.lose = False
    app.cellRow = 0
    app.cellCol = 0
    app.bestTime = 0
    app.resetTimer = int(generateTimer(app))
    app.tim = app.resetTimer - (app.resetTimer%10)
    app.timer = app.resetTimer - (app.resetTimer%10)
    app.timerKeeper = app.timer*1000
    app.win = False
    app.cnt = 0
    app.begin = 'start'
    app.notSol = []
    app.squeeze = False
    # print(app.order)

##########################################################
#CONTROLLER FUNCTIONS 
##########################################################

def sizeChanged(app): 
    if app.play == False: resetCursor(app)
    elif findCellBound(app, app.cellRow, app.cellCol) != True:
        resetCursor(app)

def resetCursor(app):
    x1,y1,x2,y2 = app.start.findMazeCell(0,0,app.width,app.height)
    app.cx = x1 + (x2-x1)/2
    app.cy = y1 + (y2-y1)/2
    app.cellRow, app.cellCol = (0,0)
    for row in range(app.start.rows):
        for col in range(app.start.cols):
            app.start.modMaze(row, col, 5, False)

def restartGame(app):
    app.play = False
    createFreshMaze(app, 10, 10, 0, 0)
    resetCursor(app)
    app.highScore = 0
    app.resetTimer = int(generateTimer(app))
    app.tim = app.resetTimer - (app.resetTimer%10)
    app.timer = app.resetTimer - (app.resetTimer%10)
    app.timerKeeper = app.timer*1000
    app.lose = False
    app.win = False
    app.cnt = 0
    app.solution = False
    app.squeeze = False

def resetBestTime(app):
    app.bestTime = 0

def keyPressed(app, event):
    if event.key == 'x': 
        print(app.start.order)
    elif event.key == 's': 
        app.solution = not app.solution
    elif event.key == 'l':
        print(app.start.wrong)
    elif event.key == 'r':
        restartGame(app)
        resetBestTime(app)
        app.begin = 'start'
    elif event.key == 'p':
        if app.begin == 'start': 
            app.begin = 'ins'
        elif app.begin == 'ins':
            app.begin = 'play'
        else: restartGame(app)
    elif event.key == 'i':
        app.begin = 'ins'
    elif event.key == 'z' and app.begin == 'play' and app.win == False:
        app.lose = True
    elif event.key == 'c':
        app.timer = 1
    elif event.key == 'w' and app.begin == 'play' and app.lose == False:
        app.win = True
        app.bestTime = app.tim-app.timer

def wrongSol(app, row, col):
    track = []
    currRow = row
    currCol = col
    while (currRow, currCol) not in app.start.order: 
        track.append(app.start.wrong[(currRow, currCol)])
        currRow, currCol = app.start.wrong[(currRow, currCol)]
    return reversed(track)

def timerFired(app):
    if app.lose == False and app.win == False: 
        if app.cnt > 0: 
            app.timerKeeper -= 1
            if app.timerKeeper%10 == 0:
                app.timer -= 1
        if app.play == True: 
            x1,y1,x2,y2 = app.start.findMazeCell(app.cellRow, app.cellCol,
            app.width,app.height)
            print(x2-x1-2*app.rad, y2-y1-2*app.rad)
            if x2-x1-2*app.rad<=0 or y2-y1-2*app.rad <= 0:
                app.lose = True
                app.squeeze = True
            else: 
                app.start.grow()
                app.start.updateMaze()
    if app.timer <= 0 and app.win == False: 
        app.lose = True

def mouseDragged(app, event):
    if app.begin == 'play':
        app.cnt += 1
        if app.win == False and app.lose == False: 
            app.cx, app.cy = event.x, event.y
            app.play = True
            app.cellRow, app.cellCol = findCell(app, event.x, event.y)
            if (app.cellRow, app.cellCol) in app.start.order: 
                   for i in range(0, app.start.order.index((app.cellRow,
                    app.cellCol))): 
                        row, col = app.start.order[i]
                        if app.start.modMaze(row, col, 5, -1) != True:
                           resetCursor(app)
                        else: 
                            if ((app.cellRow, app.cellCol) == 
                            (app.start.endRow, app.start.endCol)
                            and app.timer > 0): 
                                app.win = True
                                if 100-app.timer < 100-app.bestTime: 
                                    app.bestTime = app.tim-app.timer
            else: 
                wrong = wrongSol(app, app.cellRow, app.cellCol)
                for i in wrong: 
                        row, col = i
                        if app.start.modMaze(row, col, 5, -1) != True:
                           resetCursor(app)
            # print('cool', app.win)
            if findCellBound(app, app.cellRow, app.cellCol) != True:
                app.play = False
                resetCursor(app)
            else: 
                app.start.modMaze(app.cellRow, app.cellCol, 5, True) 

def mouseReleased(app, event):
    app.play = False

##########################################################
#NOTES
#create dictionary that maps beginning of path to the path from block in 
# order list
#store as list with 3 indexes: row, col, visited 
#if cursor not in order (else statement), then look for it in dict, 
# index into list value and make sure that for every cell cursor is in, every cell
#before it in list has been visited 
##########################################################

def findCell(app, x, y):
    row, col = 0, 0
    for c in range(app.start.cols):
        if (x > (app.width-2*app.start.margin)/app.start.cols*c+app.start.margin 
        and x < (app.width-2*app.start.margin)/app.start.cols*(c+1)
        +app.start.margin):
            col = c
    for r in range(app.start.rows):
        if (y > ((app.height-2*app.start.margin-app.start.offset)/
        app.start.cols*r+app.start.margin+app.start.offset)
        and y < ((app.height-2*app.start.margin-app.start.offset)/
        app.start.cols*(r+1)+app.start.margin+app.start.offset)):
            row = r
    #print(row, col)
    return row, col    

def findCellBound(app, row, col):
    x1, y1, x2, y2 = app.start.findMazeCell(row, col,
    app.width, app.height)
    bounds = app.start.cursorBounds(row, col)
    # print (bounds)
    # print (x1,y1,x2,y2)
    if bounds[0] != 0:
        x2 = x2 - app.rad
    if bounds[1] != 0:
        y2 = y2 - app.rad
    if bounds[2] != 0:
        y1 = y1 + app.rad
    if bounds[3] != 0:
        x1 = x1 + app.rad
    # print ('second', x1,y1,x2,y2)
        #right, down, up, left
    edges = app.start.fillCellEdge(row, col, x1,y1,x2,y2)
    if edges != None:
        for i in edges:
            (a, b, c, d) = i
            if (app.cx >= a - app.rad  and app.cy >= b-app.rad and 
            app.cx <= c+app.rad and app.cy <= d+app.rad):
                return False
    if (app.cx >= x1 and app.cy >= y1 and app.cx <= x2 and app.cy <= y2):
      return True  
    # print(False)
    return False

def generateTimer(app): 
    length = len(app.start.order)
    return length/app.start.rows*10

##########################################################
#DRAW ENTIRE APP (VIEW)
##########################################################

def drawStartScreen(app, canvas): 
    if app.begin == 'start': 
        canvas.create_rectangle(0, 0, app.width, app.height, fill = '#415a77')
        canvas.create_text(app.width/2, app.height*2/5, font = "default 50 bold ",
         text = f'CURSORS.112', fill = 'white')
        canvas.create_text(app.width/2, app.height*3/5, font = "default 20 bold ",
         text = f'PRESS "p" TO PLAY', fill = 'white')
        
def drawInstructions(app, canvas): 
    if app.begin == 'ins': 
        canvas.create_rectangle(0, 0, app.width, app.height, fill = '#415a77')
        canvas.create_text(app.width/2, app.height/2, font = 'default 11 bold', fill = 'white',
        text = """
        INSTRUCTIONS:\n 
        Get the dot to the end of the maze (dark square) before the timer runs out!\n
        To move the dot, click on the dot and drag your cursor - the timer won't start 
        until you make the first move.\n
        But be careful! A little birdy told me that these walls like to move ( ͡¬ ͜ʖ ͡¬).\n
        If you drag the dot into the walls, you'll have to restart the maze.\n
        When you're ready, press "p" to play!\n\n




        *For debugging:
        Press "s" to show maze solution
        Press "r" to reset entire game
        Press "p" in game to reset maze and timer 
        Press "z" to lose
        Press "w" to win
        Press "c" to make timer 1 sec
        """)
        
def drawWinMode(app, canvas): 
    if app.win: 
        canvas.create_rectangle(0, app.height/3, app.width, 2*app.height/3, 
        fill = '#ccd5ae', width = 0)
        canvas.create_text(app.width/2, app.height/2, font = "default 15 bold ",
        text = f' You win!', fill = '#283618')
        canvas.create_text(app.width/2, app.height*4/7, font = "default 13 bold ",
        text = f'(Press "p" for new maze or "r" to reset entire game)', 
        fill = '#283618')

def drawLoseMode(app, canvas):
    if app.lose: 
        canvas.create_rectangle(0, app.height/3, app.width, 2*app.height/3, 
        fill = '#723d46', width = 0)
        canvas.create_text(app.width/2, app.height/2, font = "default 15 bold ",
        text = f' You lose!', fill = 'white')
        canvas.create_text(app.width/2, app.height*4/7, font = "default 13 bold ",
        text = f'(Press "p" for new maze or "r" to reset entire game)', fill = 'white')
        if app.squeeze == True: 
            canvas.create_text(app.width/2, app.height*3/7, font = "default 15 bold ",
            text = f' You got crushed by the walls!', fill = 'white')
        elif app.timer <= 0:
            canvas.create_text(app.width/2, app.height*3/7, font = "default 15 bold ",
            text = f' The timer ran out!', fill = 'white')


def drawScore(app, canvas):
    canvas.create_text(app.width/7*6-app.start.margin/2, app.start.offset/2+app.start.margin,
    font = "default 13 bold ", text = f'High Score: {app.bestTime} sec', fill = 'white')

def drawTimer(app, canvas): 
    if app.cnt > 1 and app.win == False and app.lose == False: color = '#0d1b2a'
    else: color = 'white'
    canvas.create_text(app.width/2, app.start.offset/2+app.start.margin, 
    font = "default 13 bold ",text = f'Time Left: {app.timer} sec', fill = color)

def drawInsGame(app, canvas): 
    canvas.create_text(app.edge*2, app.start.offset/2+app.start.margin/2, 
    font = "default 13 bold ",text = '''
             Press "i" for 
             instructions''', fill = 'white')

def drawCircle(app, canvas):
    canvas.create_oval(app.cx-app.rad, app.cy-app.rad, app.cx+app.rad, 
    app.cy+app.rad,  width = 0, fill = '#0d1b2a')

def redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawCircle(app, canvas)
    drawScore(app, canvas)
    drawTimer(app, canvas)
    drawInsGame(app, canvas)
    drawWinMode(app, canvas)
    drawLoseMode(app, canvas)
    drawStartScreen(app, canvas)
    drawInstructions(app, canvas)


runApp(width = 600, height = 600)
