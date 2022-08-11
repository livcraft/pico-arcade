from machine import Pin, Timer
import time
from ssd1306 import SSD1306_I2C
import random

i2c = machine.I2C(0, sda=Pin(0), scl=Pin(1), freq=40000)
oled = SSD1306_I2C(128,64,i2c)

redLed = Pin(12, Pin.OUT)
redButton = Pin(20, machine.Pin.IN) ## Also being used as Down Button
redDebounce = 0

yellowLed = Pin(10, Pin.OUT)
yellowButton = Pin(18, machine.Pin.IN) ## Also being used as Up Button
yellowDebounce = 0

greenLed = Pin(11, Pin.OUT)
greenButton = Pin(19, machine.Pin.IN)
greenDebounce = 0

blueLed = Pin(13, Pin.OUT)
blueButton = Pin(21, machine.Pin.IN)
blueDebounce = 0

def turnOnScreen():
    
    for i in range(0,62,3):
        oled.fill(0)
        oled.text("Pico Arcade",20,i)
        oled.show()

    homescreen()

def writeHomescreen(index):
    oled.fill(0)
    oled.text("simon says",10,0)
    oled.text("ping pong",10,20)
    
    if index == 0:
        oled.text("-",0,2)
    else:
        oled.text("-",0,18)
    
    oled.show()
    return

def playGame(index):
    blueLed.value(0)
    greenLed.value(0)
        
    if index == 0:
        simonsays()
    else:
        pingpong(0,0)

def homescreen():
    onHomescreen = 1
    activeIndex = 0
    
    while onHomescreen == 1:
        redLed.value(0)
        yellowLed.value(0)
        blueLed.value(0)
        greenLed.value(0)
        
        redDebounce = 0
        yellowDebounce = 0
        blueDebounce = 0
        greenDebounce = 0
        
        writeHomescreen(activeIndex)
        
        if redButton.value() == 0 and redDebounce == 0:
            redLed.value(1)
            activeIndex = activeIndex + 1
            if activeIndex == 2: # CHANGE BASED ON NUMBER OF GAMES
                activeIndex = 0
            writeHomescreen(activeIndex)
            redDebounce = 1

        if yellowButton.value() == 0 and yellowDebounce == 0:
            yellowLed.value(1)
            activeIndex = activeIndex - 1
            if activeIndex == -1:
                activeIndex = 1 # CHANGE BASED ON NUMBER OF GAMES
            writeHomescreen(activeIndex)
            yellowDebounce = 1
            
        if blueButton.value() == 0 and blueDebounce == 0:
            blueLed.value(1)
            writeHomescreen(activeIndex)
            blueDebounce = 1
            
            playGame(activeIndex)
            
        if greenButton.value() == 0 and greenDebounce == 0:
            greenLed.value(1)
            writeHomescreen(activeIndex)
            greenDebounce = 1
            
            playGame(activeIndex)
       
# GAME OVER SCREEN
def gameOver():
    oled.fill(0)
    oled.text("Game Over",20,10)
    oled.text(":(", 40, 20)
    oled.show()
    
    time.sleep(3)
    
    homescreen()
            
# SIMON SAYS LED SHOW
def ledShow(valList):
    for val in valList:
        if val == "Red":
            redLed.value(1)
            time.sleep(0.25)
            redLed.value(0)
            time.sleep(0.25)
            
        if val == "Yellow":
            yellowLed.value(1)
            time.sleep(0.25)
            yellowLed.value(0)
            time.sleep(0.25)
            
        if val == "Green":
            greenLed.value(1)
            time.sleep(0.25)
            greenLed.value(0)
            time.sleep(0.25)
            
        if val == "Blue":
            blueLed.value(1)
            time.sleep(0.25)
            blueLed.value(0)
            time.sleep(0.25)
            
# SIMON SAYS GAME
def simonsays():
    oled.fill(0)
    oled.text("simon says",20,0)
    oled.show()
    
    valList = []
    optionsList = ["Red", "Yellow", "Green", "Blue"]
    playing = True
    
    while playing:
        curVal = optionsList[random.randint(0,3)]
        valList.append(curVal)
        
        oled.fill(0)
        oled.text("simon says",20,0)
        oled.text(curVal,20,20)
        oled.show()
        
        ledShow(valList)
        
        for val in valList:
            redDebounce = 0
            yellowDebounce = 0
            blueDebounce = 0
            greenDebounce = 0

            timer1 = 0
            notPressed = True
            
            while notPressed:
                timer1 += 1
                
                if val == "Red":
                    if redButton.value() == 0 and redDebounce == 0:
                        redLed.value(1)
                        time.sleep(0.25)
                        redLed.value(0)
                        notPressed = False
                        redDebounce = 1
                    if yellowButton.value() == 0 or greenButton.value() == 0 or blueButton.value() == 0:
                        gameOver()
                    
                if val == "Yellow":
                    if yellowButton.value() == 0 and yellowDebounce == 0:
                        yellowLed.value(1)
                        time.sleep(0.25)
                        yellowLed.value(0)
                        notPressed = False
                        yellowDebounce = 1
                    if redButton.value() == 0 or greenButton.value() == 0 or blueButton.value() == 0:
                        gameOver()
                    
                if val == "Green":
                    if greenButton.value() == 0 and greenDebounce == 0:
                        greenLed.value(1)
                        time.sleep(0.25)
                        greenLed.value(0)
                        notPressed = False
                        greenDebounce = 1
                    if yellowButton.value() == 0 or redButton.value() == 0 or blueButton.value() == 0:
                        gameOver()
                    
                if val == "Blue":
                    if blueButton.value() == 0 and blueDebounce == 0:
                        blueLed.value(1)
                        time.sleep(0.25)
                        blueLed.value(0)
                        notPressed = False
                        blueDebounce = 1
                    if yellowButton.value() == 0 or greenButton.value() == 0 or redButton.value() == 0:
                        gameOver() 
                    
                if timer1 > 75000:
                    gameOver()
                    
    gameOver()
    
# MOVE BALL FOR PING PONG
def moveBall(currentDirection, ballPos):
    steps = 4
    if currentDirection == 0:
        ballPos[0] -= steps
        ballPos[1] -= steps
        if ballPos[1] < 0:
            currentDirection = 2
            
        return currentDirection, ballPos
        
    if currentDirection == 1:
        ballPos[0] += steps
        ballPos[1] -= steps
        if ballPos[1] < 0:
            currentDirection = 3
            
        return currentDirection, ballPos
        
    if currentDirection == 2:
        ballPos[0] -= steps
        ballPos[1] += steps
        if ballPos[1] > 63:
            currentDirection = 0
            
        return currentDirection, ballPos
        
    if currentDirection == 3:
        ballPos[0] += steps
        ballPos[1] += steps
        if ballPos[1] > 63:
            currentDirection = 1
            
        return currentDirection, ballPos
   
# DISPLAY SCORE FOR PING PONG
def displayScores(player1score, player2score):
    oled.fill(0)
    
    curScores = "P1: " + str(player1score) + "     P2: " + str(player2score)
    oled.text(curScores,5,0)
    oled.show()
    
    time.sleep(3)
    oled.fill(0)
    pingpong(player1score, player2score)
    
# PING PONG GAME
def pingpong(player1score, player2score):
    if player1score == 3:
        oled.text("P1 wins",25,10)
        oled.show()
        
        time.sleep(2)
        gameOver()
    if player2score == 3:
        oled.text("P2 wins",25,10)
        oled.show()
        
        time.sleep(2)
        gameOver()
        
    oled.fill(0)
    oled.show()
    winner = False
    
    p1pos = [0,20,5,15]
    p2pos = [122,20,5,15]
    
    ballPos = [60,22]
    currentDirection = random.randint(0,3)
    
    oled.rect(p1pos[0], p1pos[1], p1pos[2], p1pos[3], 1)
    oled.rect(p2pos[0], p2pos[1], p2pos[2], p2pos[3], 1)
    
    oled.pixel(ballPos[0],ballPos[1],1)
    oled.show()
    
    while not winner:
        redDebounce = 0
        yellowDebounce = 0
        blueDebounce = 0
        greenDebounce = 0
        
        if redButton.value() == 0 and redDebounce == 0:
            oled.rect(p1pos[0], p1pos[1], p1pos[2], p1pos[3], 0)
            
            p1pos = [0,p1pos[1] + 8,5,p1pos[3]]
            oled.rect(p1pos[0], p1pos[1], p1pos[2], p1pos[3], 1)
            oled.show()
            redDebounce = 1
            
        if yellowButton.value() == 0 and yellowDebounce == 0:
            oled.rect(p1pos[0], p1pos[1], p1pos[2], p1pos[3], 0)
            
            p1pos = [0,p1pos[1] - 8,5,p1pos[3]]
            oled.rect(p1pos[0], p1pos[1], p1pos[2], p1pos[3], 1)
            oled.show()
            yellowDebounce = 1
            
        if greenButton.value() == 0 and greenDebounce == 0:
            oled.rect(p2pos[0], p2pos[1], p2pos[2], p2pos[3], 0)
            
            p2pos = [122,p2pos[1] - 8,5,p2pos[3]]
            oled.rect(p2pos[0], p2pos[1], p2pos[2], p2pos[3], 1)
            oled.show()
            greenDebounce = 1
            
        if blueButton.value() == 0 and blueDebounce == 0:
            oled.rect(p2pos[0], p2pos[1], p2pos[2], p2pos[3], 0)
            
            p2pos = [122,p2pos[1] + 8,5,p2pos[3]]
            oled.rect(p2pos[0], p2pos[1], p2pos[2], p2pos[3], 1)
            oled.show()
            blueDebounce = 1
            
        oled.pixel(ballPos[0],ballPos[1],0)
        currentDirection, ballPos = moveBall(currentDirection, ballPos)
        oled.pixel(ballPos[0],ballPos[1],1)
        oled.show()
        
        if ballPos[0] <=5:
            if (p1pos[1] <= ballPos[1] and ballPos[1] <= p1pos[1] + p1pos[3]):
                if currentDirection == 0:
                    currentDirection = 1
                else:
                    currentDirection = 3
                    
                oled.pixel(ballPos[0],ballPos[1],0)
                currentDirection, ballPos = moveBall(currentDirection, ballPos)
                oled.pixel(ballPos[0],ballPos[1],1)
                oled.show()
            else:
                player2score += 1
                displayScores(player1score, player2score)
                
        if ballPos[0] >= 122:
            if (p2pos[1] <= ballPos[1] and ballPos[1] <= p2pos[1] + p2pos[3]):
                if currentDirection == 1:
                    currentDirection = 0
                else:
                    currentDirection = 2
                    
                oled.pixel(ballPos[0],ballPos[1],0)
                currentDirection, ballPos = moveBall(currentDirection, ballPos)
                oled.pixel(ballPos[0],ballPos[1],1)
                oled.show()
            else:
                player1score += 1
                displayScores(player1score, player2score)
        
    gameOver()

turnOnScreen()