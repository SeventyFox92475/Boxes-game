# Importing Modules
##### CHANGE IP TO HOST IP #####
import pygame
import socket
from threading import Thread
from multiprocessing import Process

# Constant Variables
screenHeight = 400
screenWidth = 400
gridSnapVal = ((screenHeight+screenWidth)/2)/10

# Flexible Variables
coordsLst = []
grid = []
lines = []
clickedCoords = []
current_x = 0
current_y = 0
mouse_down = False
something = 0
player1X = ''
player1Y = ''
player1Width = ''
player1Height = ''
msg = ''
wait = False

# Socket Stuff
port = 10000
host = '192.168.245.1'
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = host, port
socket.connect(server)
socketMsg = b''

# Creates the window with dimensions of 410x410
wn = pygame.display.set_mode((screenWidth + 10, screenHeight + 10))

# Class for making a line
class Line:

    # Initial action to start up class
    def __init__(self, x, y, color, surface, width, height):

        # Assigns the function variables to class variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Creats a pygame object
        self.PyGameObject = pygame.draw.rect(surface, color, (x, y, width, height))

# Algorithm to fill screen
for i in range(int((screenHeight*screenWidth)/gridSnapVal**2)):
    # Adds the location of lines to grid list
    grid.append(Line(current_x, current_y, (105, 105, 105), wn, 40, 10))
    grid.append(Line(current_x, current_y, (105, 105, 105), wn, 10, 40))
    current_x += 40
    coordsLst.append((current_x, current_y))
    if current_x == screenWidth:
        grid.append(Line(current_x, current_y, (105, 105, 105), wn, 10, 40))
        current_x = 0
        current_y += 40
        coordsLst.append((current_x, current_y))
    if current_y == screenHeight:
        for i in range(11):
            grid.append(Line(current_x, current_y, (105, 105, 105), wn, 40, 10))
            current_x += 40
            coordsLst.append((current_x, current_y))

# Function to redraw the Pygame window
def redrawWin():
    # Adds the lines to the screen from the grid list
    for gridObject in grid:
        gridObject
    # Updates the screen
    pygame.display.flip()

# Gets pygame events
def get_events():
    global pos, mouse_down, something
    pygame.event.pump()
    if something != 1:
        events = pygame.event.get()
    for event in events:
        # Quits
        if event.type == pygame.QUIT:
            pygame.quit()
        # Gets clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mouseDown()
            mouse_down = True
        else:
            mouse_down = False

def mouseDown():
    global pos, wait, msg, mouse_down, socketMsg, something, player1X, player1Y, player1Width, player1Height
    for coords in coordsLst:
        if not wait:
            if (pos[0], pos[1], 50, 10) not in clickedCoords:
                if ((coords[0] + 30 > pos[0] and coords[0] + 10 < pos[0]) and (coords[1] + 10 > pos[1] and coords[1] < pos[1])):
                    lines.append(Line(coords[0], coords[1], (255, 0, 0), wn, 50, 10))
                    clickedCoords.append((coords[0], coords[1], 50, 10))
                    redrawWin()
                    fullStr = str(coords[0]) + ' ' + str(coords[1]) + ' ' + '50' + ' ' + '10' + ' '
                    socket.send(bytes(fullStr, encoding='utf8'))  
                    wait = True
            if (pos[0], pos[1], 10, 50) not in clickedCoords:   
                if ((coords[1] + 40 > pos[1] and coords[1] + 10 < pos[1]) and (coords[0] + 10 > pos[0] and coords[0] < pos[0])):
                    lines.append(Line(coords[0], coords[1], (255, 0, 0), wn, 10, 50))
                    clickedCoords.append((coords[0], coords[1], 10, 50))
                    redrawWin()
                    fullStr = str(coords[0]) + ' ' + str(coords[1]) + ' ' + '10' + ' ' + '50' + ' '
                    socket.send(bytes(fullStr, encoding='utf8'))
                    wait = True

# TODO TODO TODO Get all sides to work, include length and width, not just the position, that isn't enough
def getWin():
    global clickedCoords
    for coords in clickedCoords:
        winCounter = 0
        for coords2 in clickedCoords:
            if (coords[0] + 40, coords[1]) == (coords2[0], coords2[1]):
                winCounter += 1
        for coords2 in clickedCoords:
            if (coords[0], coords[1] + 40) == (coords2[0], coords2[1]):
                winCounter += 1
        for coords2 in clickedCoords:
            if (coords[0] + 40, coords[1] + 40) == (coords2[0], coords2[1]):
                winCounter += 1
        if winCounter == 3:
            print('Win!')


def getRecv():
    global wait
    while True:
        msg = (socket.recv(1024)).decode(encoding='utf8')
        wait = False
        index = 0
        player1X = ''
        player1Y = ''
        player1Width = ''
        player1Height = ''
        while msg[index] != ' ':
            player1X += str(msg[index])
            index += 1
        index += 1
        while msg[index] != ' ':
            player1Y += str(msg[index])
            index += 1
        index += 1
        while msg[index] != ' ':
            player1Width += str(msg[index])
            index += 1
        index += 1
        while msg[index] != ' ':
            player1Height += str(msg[index])
            index += 1
        lines.append(Line(int(player1X), int(player1Y), (0, 0, 255), wn, int(player1Width), int(player1Height)))
        redrawWin()
thread = Thread(target=getRecv)
thread.start()
# Main Game loop
while True:
    # Calls Functions
    getWin()
    redrawWin()
    get_events()
