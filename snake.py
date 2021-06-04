#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Porting of http://zetcode.com/javascript/snake/

This is a simple Snake game
clone.

Author: Sinbrive
Last edited: May 2021
"""

import sys
import random
# from PIL import Image, ImageTk
from PyQt5.QtWidgets import QDialog, QApplication, QLabel
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt

class Cons:
        
    BOARD_WIDTH = 400
    BOARD_HEIGHT = 400
    DELAY = 150
    DOT_SIZE = 10
    MAX_RAND_POS = 27

class Snake(QDialog):

    def __init__(self):
        super().__init__()
                
        self.setWindowTitle('Snake')
        self.setStyleSheet("background-color:black")
        self.setFixedWidth(Cons.BOARD_WIDTH)
        self.setFixedHeight(Cons.BOARD_HEIGHT)
        self.init_game()

    def init_game(self):
        """initializes game"""

        self.inGame = True
        self.score = 0
        
        # starting apple coordinates
        self.appleX = 100
        self.appleY = 190

        self.dots = 3
        self.x=[]     
        self.y=[] 
        
        self.x.append(Cons.DOT_SIZE)
        self.x.append(Cons.DOT_SIZE)
        self.x.append(Cons.DOT_SIZE)

        self.y.append(3*Cons.DOT_SIZE)
        self.y.append(2*Cons.DOT_SIZE)
        self.y.append(Cons.DOT_SIZE)

        self.leftDirection = False
        self.rightDirection = False
        self.upDirection = False
        self.downDirection = False
        
        self.load_images()

        self.create_objects()
        self.locate_apple()
 
        timer = QTimer(self)
        timer.timeout.connect(self.on_timer)
        timer.start(Cons.DELAY)

    def load_images(self):
        """loads images from the disk"""
        
        try:

            self.l_iapple = QLabel(self)
            self.iapple = QPixmap('apple.png')
            self.l_iapple.setPixmap(self.iapple)


        except IOError as e:
            
            print(e)
            sys.exit(1)
        
    def create_objects(self):
        self.l_score = QLabel(self)
        self.l_score.setStyleSheet("color:white")
        st = "Score: "+str(self.score)
        self.l_score.setText(st)
        self.l_score.move(Cons.BOARD_WIDTH-100, 10)
               
    def check_apple_collision(self):
        #checks if the head of snake collides with apple
        if (self.x[0] == self.appleX) and (self.y[0] == self.appleY):
            self.dots+=1 
            self.x.append(-Cons.BOARD_WIDTH)
            self.y.append(-Cons.BOARD_HEIGHT)
            self.score += 1
            self.locate_apple()
        
    def move_snake(self):
        """moves the Snake object"""
        for z in range (self.dots-1, 0, -1):
            self.x[z] = self.x[(z - 1)]
            self.y[z] = self.y[(z - 1)]

        if self.leftDirection:
            self.x[0] -= Cons.DOT_SIZE

        if self.rightDirection:
            self.x[0] += Cons.DOT_SIZE;

        if self.upDirection:
            self.y[0] -= Cons.DOT_SIZE

        if self.downDirection:
            self.y[0] += Cons.DOT_SIZE


        # out of the baord
        if self.x[0] >= Cons.BOARD_WIDTH:
            self.x[0] =  0

        if self.x[0] < 0:
            self.x[0] = Cons.BOARD_WIDTH

        if self.y[0] >= Cons.BOARD_HEIGHT:
            self.y[0] =  0

        if self.y[0] < 0:
            self.y[0] = Cons.BOARD_HEIGHT

 
    def doDrawing(self):
        self.update()   # pqintEvent

    def paintEvent(self, event):         
        painter = QPainter(self)
        if self.inGame: 
            for i in range(0, self.dots):
                if i==0:
                    painter.setPen(Qt.red)
                    painter.setBrush(Qt.red)
                else:
                    painter.setPen(Qt.white)
                    painter.setBrush(Qt.white)
                painter.drawRect(self.x[i], self.y[i], Cons.DOT_SIZE, Cons.DOT_SIZE)
        else:
            self.gameOver();      

    def check_gameEnd(self):
        """checks for collisions"""
        for z in range(self.dots-1, 0, -1):

            if z > 4 and self.x[0] == self.x[z] and self.y[0] == self.y[z]:
                inGame = False;
            

    def locate_apple(self):
        """places the apple object on Canvas"""
    
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleX = r * Cons.DOT_SIZE
        r = random.randint(0, Cons.MAX_RAND_POS)
        self.appleY = r * Cons.DOT_SIZE
        
        self.l_iapple.move(self.appleX, self.appleY)

    def keyPressEvent(self, e):
        """controls direction variables with cursor keys"""
    
        key = e.key()

        if key == Qt.Key_Left and (not self.rightDirection):
    
            self.leftDirection = True
            self.upDirection = False
            self.downDirection = False

        if key == Qt.Key_Right and (not self.leftDirection):
            
            self.rightDirection = True
            self.upDirection = False
            self.downDirection = False

        if key == Qt.Key_Up and (not self.downDirection):
            
            self.upDirection = True
            self.rightDirection = False
            self.leftDirection = False


        if key == Qt.Key_Down and (not self.upDirection):
            
            self.downDirection = True
            self.rightDirection = False
            self.leftDirection = False


    def on_timer(self):
        """creates a game cycle each timer event"""
        self.draw_score()
        self.check_gameEnd()

        if self.inGame:
            self.check_apple_collision()
            if self.upDirection or self.downDirection or self.leftDirection or self.rightDirection:
                self.move_snake()
            self.doDrawing();
        else:
            self.game_over()

    def draw_score(self):
        """draws score"""
        st = "Score:"+str(self.score)
        self.l_score.setText(st)
 #
    def game_over(self):
        """deletes all objects and draws game over message"""
        self.l_gameOver = QLabel('Game Over', self)
        self.l_gameOver.setStyleSheet("font_type: 'serif'; align:center; color:white")
        self.l_gameOver.move(Cons.BOARD_WIDTH/2, Cons.BOARD_HEIGHT/2)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    snake = Snake()
    snake.show()
    sys.exit(app.exec_())
