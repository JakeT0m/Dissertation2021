import pygame
from pygame.locals import *
import sys
import random

#importing the dissertation necessary functions
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from potobj import *
#from accelobj import *
from bluezero import microbit
from time import sleep
from time import time
from datetime import datetime

class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.blue = pygame.image.load("assets/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        
        #DISS CODE
        
        #code for the potentiometer:
        #instantiating the potentiometer as part of the doodle jump object
        self.i2c = busio.I2C(board.SCL, board.SDA)

        #Creating theADC object using i2C bus
        self.ads = ADS.ADS1015(self.i2c)
        
        #the game now has instatiated the potentiometer
        self.pot0 = Potentiometer(0,self.ads)
        
        #Code for the Microbits:
        self.ubit1 = microbit.Microbit(adapter_addr='DC:A6:32:7C:35:D2',
                         device_addr='D6:CA:A9:57:F7:72')
        self.ubit2 = microbit.Microbit(adapter_addr='DC:A6:32:7C:35:D2',
                         device_addr='E4:E1:14:75:E1:E5')
        
        try:
            self.ubit1.connect()
            print("Microbit 1 Connected!")
        except:
            print("Could not connect to Microbit 1")

        print("Attempting to connect to Microbit 2...")
        try:
            self.ubit2.connect()
            print("Microbit 2 Connected!")
        except:
            print("Could not connect to Microbit 2")
        
        #creating both microbit devices
        #self.mbit1 = accel(1)
        #self.mbit2 = accel(2)
        #self.quitstatus = False    #this is the quit status of the game
        
        #opening the necesary file
        time = datetime.__str__(datetime.today())
        self.name = "Accelerometer data: " + time
        bad = ' '
        good = '_'
        self.name = self.name.replace(bad,good)
        bad = ':'
        good = '_'
        self.name = self.name.replace(bad,good)
        file = open(self.name, "w")
        file.close()
        self.writeto = []
        
        
    def updatePlayer(self):
        #x1, y1, z1 = self.ubit1.accelerometer
        #time = datetime.__str__(datetime.utcnow())
        #x2, y2, z2 = self.ubit2.accelerometer
        #file.write('time: ' + time + '        x1: ' + str(x1) + '    y1: '+ str(y1) + '    z1: ' + str(z1) +'\n')
        #file.write('time: ' + time + '        x2: ' + str(x2) + '    y2: '+ str(y2) + '    z2: ' + str(z2) +'\n')
        
        direction = self.pot0.returndirection()  #this gathers the direction of the pot at the begining of each 
        #ubit1button = [self.ubit1.button_a, self.ubit1.button_b]        #gets the status of the microbit1 buttons
        #if ubit1button[0] >= 1 and ubit1button[1] >= 1:   #checks if both butons have been pressed to act as the quitting method
            #QUITS
        #    self.mbit1.disconnectmicrobit()
        #    self.mbit2.disconnectmicrobit()
        #    pygame.quit()
        #    sys.exit("User Terminated Via Microbit")
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        #key = pygame.key.get_pressed()
        
        #if key[K_RIGHT]:
        ##this is the part of the game that decides where the player moves to
        if direction == 1:     #checks to see if the potentiometer is pointing right
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        #elif key[K_LEFT]:
        elif direction == 3:    #checks to see if the potentiometer is pointing left
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))
    
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))
    
    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255,255,255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.playery - self.cameray > 700:
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
                #this is when the character dies. Once this occurs the file is saved

                
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip() 


DoodleJump().run()
