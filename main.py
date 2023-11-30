import sys
import math
import time
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.new_window = None
    
    def initUI(self):
        self.setWindowTitle("Tetris")
        self.setGeometry(100, 100, 500, 400)
        self.center()

        widget = QWidget(self)
        grid = QGridLayout(widget)
        

        self.label = QLabel("테트리스 게임", self)
        #self.label.setGeometry(0, 0, self.width(), 50)
        
        self.setfont()
        
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.p1_btn = QPushButton("1인용", self)
        self.p1_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.p1_btn.clicked.connect(lambda : self.open_new_window(1))

        self.p2_btn = QPushButton("2인용", self)
        self.p2_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.p2_btn.clicked.connect(lambda : self.open_new_window(2))

        self.vs2_btn = QPushButton("2인 대전", self)
        self.vs2_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vs2_btn.clicked.connect(lambda : self.open_new_window(3))

        self.com_btn = QPushButton("컴퓨터 대전", self)
        self.com_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)    
        self.com_btn.clicked.connect(lambda : self.open_new_window(4))

        self.setting_btn = QPushButton("설정", self)
        self.setting_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setting_btn.clicked.connect(self.open_new_window)
        
        self.exit_btn = QPushButton(" 나가기", self)
        self.exit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.exit_btn.clicked.connect(QCoreApplication.instance().quit)
        
        
        grid.addWidget(self.label,0,0,1,3)
        grid.addWidget(self.p1_btn,1,0)
        grid.addWidget(self.p2_btn,1,1)
        grid.addWidget(self.vs2_btn,1,2)
        grid.addWidget(self.com_btn,2,0)
        grid.addWidget(self.setting_btn,2,1)
        grid.addWidget(self.exit_btn,2,2)
        self.setLayout(grid)
        self.setCentralWidget(widget)

        

    def center(self,flag=True):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        dp = QPoint(200, 0)
        if flag:
            dp  = -QPoint(600, 0)
        self.move(qr.topLeft()+dp)
        
    def setfont(self):
        font = self.label.font()
        font.setPointSize(30)
        font.setBold(True)
        font.setFamily("나눔고딕")

        self.label.setFont(font)

    def open_new_window(self,option):
        if not self.new_window is None:
            self.new_window.close()
        self.new_window = Board(option)
        
        self.new_window.show()

    

class Board(QWidget):
    def __init__(self,option):
        super().__init__()
        self.initUI(option)
    def initUI(self,option):
        self.setWindowTitle("Tetris")
        self.setGeometry(100, 100, 1000, 700)

        self.option = option

        self.next_block_text = QLabel(self)
        self.next_block_text.setGeometry(int(self.width()*0.47), int(self.height()//8 * 1.2), int(self.width()*0.1), self.height()//8)
        self.next_block_text.setText("다음 블럭")

        self.pocket_block_text = QLabel(self)
        self.pocket_block_text.setGeometry(int(self.width()*0.47), int(self.height()//8 * 3.2), int(self.width()*0.1), self.height()//8)
        self.pocket_block_text.setText("포켓 블럭")

        

        self.p1_board = QLabel(self)
        self.p1_board.setGeometry(0, 0, int(self.width()*0.4), self.height())
        self.p1_board.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_next = QLabel(self)
        self.p1_next.setGeometry(int(self.width()*0.42), int(self.height()//8 * 2), int(self.width()*0.1), self.height()//8)
        self.p1_next.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_pocket = QLabel(self)
        self.p1_pocket.setGeometry(int(self.width()*0.4), int(self.height()//8 * 4), int(self.width()*0.1), self.height()//8)
        self.p1_pocket.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_score = QLabel(self)
        self.p1_score.setGeometry(int(self.width()*0.42), int(self.height()//8 * 0.5), int(self.width()*0.1), self.height()//8)
        self.p1_score.setText(f"점수: {0}")



        self.p2_board = QLabel(self)
        self.p2_board.setGeometry(int(self.width()*0.6), 0, int(self.width()*0.4), self.height())
        self.p2_board.setStyleSheet("background-color: rgb(255, 255, 255);")
        

        self.p2_next = QLabel(self)
        self.p2_next.setGeometry(int(self.width()*0.46), int(self.height()//8 * 2), int(self.width()*0.1), self.height()//8)
        self.p2_next.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p2_pocket = QLabel(self)
        self.p2_pocket.setGeometry(int(self.width()*0.5), int(self.height()//8 * 4), int(self.width()*0.1), self.height()//8)
        self.p2_pocket.setStyleSheet("background-color: rgb(255, 255, 255);")

        

        self.board_resize()

        MainWindow.center(self,False)

        observer = AttackObserver()
        if self.option == 4:
            self.game = Tetirs(self.p1_board,self.p1_next,self.p1_pocket,self.height(), observer,self.option-1) # 수정 해야 하는 부분
        else:
            self.game = Tetirs(self.p1_board,self.p1_next,self.p1_pocket,self.height(), observer,self.option)
        self.game.user_signal.connect(self.show_p1_score)

        if option != 1:
            self.p2_score = QLabel(self)
            self.p2_score.setGeometry(int(self.width()*0.5), int(self.height()//8 * 0.5), int(self.width()*0.1), self.height()//8)
            self.p2_score.setText(f"점수: {0}")

            self.game2 = Tetirs(self.p2_board,self.p2_next,self.p2_pocket,self.height(), observer,self.option) # 수정 해야 하는 부분
            self.game2.user_signal.connect(self.show_p2_score)

    def board_resize(self):
        self.p1_board.setGeometry(0, 0, (self.p1_board.width()//10)*10, self.height())
        self.p2_board.setGeometry(int(self.width()*0.6), 0, (self.p2_board.width()//10)*10, self.height())

        self.p1_next.setGeometry(int(self.width()*0.4), int(self.height()//8 * 2), (self.p1_next.width()//4)*4, self.height()//8)
        self.p2_next.setGeometry(int(self.width()*0.5), int(self.height()//8 * 2), (self.p2_next.width()//4)*4, self.height()//8)

        self.p1_pocket.setGeometry(int(self.width()*0.4), int(self.height()//8 * 4), (self.p1_pocket.width()//4)*4, self.height()//8)
        self.p2_pocket.setGeometry(int(self.width()*0.5), int(self.height()//8 * 4), (self.p2_pocket.width()//4)*4, self.height()//8)
        

    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_A and not self.game.finish_down_line:
            
            # self.move(self.curX - 1, self.curY)
            
            self.game.left_move()
                

        elif key == Qt.Key_D:
            # self.move(self.curX + 1, self.curY)
            self.game.right_move()

            # self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_S:
            # self.move(self.curX, self.curY+1)
            self.game.down_move()
                
            # self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_W:
            self.game.rotate_move()


        elif key == Qt.Key_C and not self.game.use_pocket:
            self.game.pocket_move()
                
        elif key == Qt.Key_V:
            self.game.dropDown()


        elif key == Qt.Key_Left and self.option != 1 and self.option != 4:
            self.game2.left_move()
            
        elif key == Qt.Key_Right and self.option != 1 and self.option != 4:
            self.game2.right_move()
            
        elif key == Qt.Key_Down and self.option != 1 and self.option != 4:
            self.game2.down_move()
                
        elif key == Qt.Key_Up and self.option != 1 and self.option != 4:
            self.game2.rotate_move()
        
        elif key == Qt.Key_N and not self.game2.use_pocket:
            self.game2.pocket_move()

        elif key == Qt.Key_M:
            self.game2.dropDown()
    
    @pyqtSlot(int)
    def show_p1_score(self,score):
        self.p1_score.setText(f"점수: {score}")

    @pyqtSlot(int)
    def show_p2_score(self,score):
        self.p2_score.setText(f"점수: {score}")

    def closeEvent(self, event):
        if self.option == 1:
            self.game.timer.stop()
        else:
            self.game.timer.stop()
            self.game2.timer.stop()

    
class AttackObserver:
    def __init__(self) -> None:
        self.game_list = []
    
    def add_game(self,game):
        self.game_list.append(game)
    
    def notify_attack(self, attak_game, attack_dmg):
        shffled_list = self.game_list[:]
        random.shuffle(shffled_list)

        for game in shffled_list:
            if game != attak_game:
                game.attacked(attack_dmg)
                
'''

가중치

높이 + 전체 빈칸 + 지울 수 있는 줄의 개수 +  벽과 인접한 면의 개수 +바닥과 인접한 면의 개수+ 블록과 인접한 면의 개수 


'''
class Ai_Move:
    def __init__(self):
        self.game_width = 10
        self.game_height = 20
        

    def instruct_direction(self,game,put_board,cur_shape ):
        self.game = game
        self.put_board = put_board
        self.falling_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20
        self.back_board = [list([-1 for i in range(10)]) for j in range(20)]
        
        self.cur_shape = cur_shape
        self.dy = 0
        self.continueflag = False

        self.shape = self.cur_shape.get_cur_shape()
        
        
        self.weight_board = [-math.inf,0,0,0] # 가중치, x, 회전 횟수 , pocket 사용 여부

        for k in range(2):
            if not self.cur_shape.is_pocket and k == 1:
                self.shape = self.cur_shape.get_next_shape()
                
            elif self.cur_shape.is_pocket and k == 1:
                self.shape = self.cur_shape.get_pocket()
            
            for i in range(4):
                
                for j in range(20 - self.cur_shape.get_cur_max_x(self.shape)-1):
                
                    self.weight_board_rotated = []
                    
                    self.dropDown(j)
                    
                    if self.continueflag:
                        self.continueflag = False
                        continue
                    self.draw_falling(j,self.dy)
                    
                    self.add_board()

                    self.height = self.get_height()
                    self.blank = self.get_blank(j)
                    self.under_blank = self.get_under_blank(j)  
                    
                    self.del_line = self.get_del_line()
                    self.wall = self.get_wall()
                    self.floor = self.get_floor()
                    self.around_block = self.get_around_block()
                    
                    
                    score = -3*self.height - 1*self.blank - 15*self.under_blank + self.del_score() + self.wall*6 + self.floor*10  + self.around_block*6
                    
                    
                    
                    '''
                    높이 : 0~20

                    빈칸 : 0~200

                    지울 수 있는 줄의 개수 : 0~4

                    밑에 빈칸 : 0~40

                    벽과 인접한 면의 개수 : 0~20

                    바닥과 인접한 면의 개수 : 0~10

                    블록과 인접한 면의 개수 : 0~80
                    
                    '''
                    
                    
                    if(score >= self.weight_board[0]):
                        #print("k : ",k," i : ",i," j : ",j)
                        #print("height : ",self.height," blank : ",self.blank," under_blank : ",self.under_blank," del_line : ",self.del_line," wall : ",self.wall," floor : ",self.floor," around_block : ",self.around_block," score : ",score)
                        self.weight_board[0] = score
                        self.weight_board[1] = j
                        self.weight_board[2] = i
                        
                        if k == 1:
                            self.weight_board[3] = 1
                
                self.shape = self.cur_shape.rotated(self.shape)
                #print(self.shape)

        #print("===================================")

        sleep_time = 0.01

        if self.weight_board[3] == 1:
            self.game.pocket_move()
            time.sleep(sleep_time)
        
        
            

        for i in range(self.weight_board[2]):
            self.game.rotate_move()
            time.sleep(sleep_time)
            

        if self.weight_board[1] < self.cur_shape.curx:
            for i in range(self.cur_shape.curx - self.weight_board[1]):
                self.game.left_move()
                time.sleep(sleep_time)

        elif self.weight_board[1] > self.cur_shape.curx:
            for i in range(self.weight_board[1] - self.cur_shape.curx):
                self.game.right_move()
                time.sleep(sleep_time)

        self.game.dropDown()
        
    def del_score(self):
        if self.del_line == 1:
            return 30
        elif self.del_line == 2:
            return 300
        elif self.del_line == 3:
            return 500
        elif self.del_line == 4:
            return 800
        else:
            return 0

    def get_around_block(self):
        around_block_cnt = 0
        for i in range(self.game_height):
            for j in range(self.game_width):
                if self.falling_board[i][j] != -1:
                    if i-1 >= 0 and self.put_board[i-1][j] != -1:
                        around_block_cnt += 1
                    if i+1 < self.game_height and self.put_board[i+1][j] != -1:
                        around_block_cnt += 1
                    if j-1 >= 0 and self.put_board[i][j-1] != -1:
                        around_block_cnt += 1
                    if j+1 < self.game_width and self.put_board[i][j+1] != -1:
                        around_block_cnt += 1
                    
        return around_block_cnt
    
    def get_wall(self):
        wall_cnt = 0
        for i in range(self.game_height):
            if self.back_board[i][0] != -1:
                wall_cnt += 1
            if self.back_board[i][self.game_width-1] != -1:
                wall_cnt += 1
                    
        return wall_cnt
    
    def get_floor(self):
        floor_cnt = 0
        for i in range(self.game_width):
            if self.back_board[-1][i] != -1:
                floor_cnt += 1
        return floor_cnt


            
    def get_del_line(self):
        del_line_cnt = 0
        for i in range(self.game_height):
            if -1 not in self.back_board[i]:
                del_line_cnt += 1
        return del_line_cnt

    def add_board(self):
        self.back_board = [list([-1 for i in range(10)]) for j in range(20)]
        for i in range(self.game_height):
            for j in range(self.game_width):
                if self.put_board[i][j] != -1:
                    self.back_board[i][j] = self.put_board[i][j]
                elif self.falling_board[i][j] != -1:
                    self.back_board[i][j] = self.falling_board[i][j]
                else:
                    self.back_board[i][j] = -1


    def get_height(self):
        for i ,val in enumerate(self.back_board):
            if sum(val) != -10:
                return self.game_height - i
        return 0
            
    def get_blank(self,x):
        blank_cnt = 0
        for i in range(self.game_height-1,self.game_height-1-self.height,-1):
            for j in range(self.game_width):
                if self.back_board[i][j] == -1:
                    blank_cnt += 1
        return blank_cnt

    def get_under_blank(self,x):
        blank_cnt = 0
        for i in range(self.game_height-1,self.dy-1,-1):
            for j in range(x,x+self.cur_shape.get_cur_max_x(self.shape)+1):
                if self.back_board[i][j] == -1:
                    blank_cnt += 1
        
        return blank_cnt

    def dropDown(self,x):
        
        self.dy = self.cur_shape.cury

        while self.game.check_put_block(x,self.dy+1, self.shape):
            self.dy += 1
        if self.dy == self.cur_shape.cury:
            self.continueflag = True
            
        

    def draw_falling(self,x,y):
        flag = False
        self.falling_board = [list([-1 for i in range(10)]) for j in range(20)]
        for i in range(self.cur_shape.get_cur_max_y(self.shape)+1):
            for j in range(self.cur_shape.get_cur_max_x(self.shape)+1):
                if self.shape[i][j] != -1:                    
                    self.falling_board[i+y][x + j] = self.cur_shape.get_cur_inx()
        

    def check_put_block(self,x,y,shape):
        
        if x+self.cur_shape.get_cur_min_x(shape) < 0 or x+self.cur_shape.get_cur_max_x(shape)>= self.game_width:
            return False
        if y+self.cur_shape.get_cur_min_y(shape) < 0:
            print("game over")
            return False
        if y+self.cur_shape.get_cur_max_y(shape) >= self.game_height:            
            return False
        
        for i in range(self.cur_shape.get_cur_max_y(shape)-1,-1,-1):
            for j in range(self.cur_shape.get_cur_max_x(shape)-1,-1,-1):
                if shape[i][j] != -1:
                    if self.put_filed[i+y][j+x] != -1:
                        return False

        

class Tetirs(QWidget):
    user_signal = pyqtSignal(int)
    def __init__(self,board:QLabel,next_lb:QLabel,pocket_lb:QLabel,height:int, observer:AttackObserver,option):
        super().__init__()
        self.option = option
        
        self.ai_move = Ai_Move()

        
    
        self.score = 0

        self.initUI(board,next_lb,height,pocket_lb)
        
        self.observer = observer
        self.attack_flag = False
        observer.add_game(self)
        self.attack_dmg = 0

        

    def initUI(self,board:QLabel,next_lb:QLabel,height:int,pocket_lb:QLabel):
        self.board = board
        self.c_height = height
        self.next_lb = next_lb
        self.pocket_lb = pocket_lb
        
        self.use_pocket = False

        self.finish_down_line = True # 한줄이 다 내려왔는지 확인하는 변수 

        self.timer = QBasicTimer()

        self.game_width = 10
        self.game_height = 20

        self.back_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20

        self.put_filed = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20

        self.falling_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20

        self.start()
        #여기서 start를 쓰레드로 호출

        

    # def get_space_size(self,n=20):
    #     return self.c_height//n

    def start(self): 

        self.pixmap = QPixmap(int(self.width()), self.c_height)
        self.pixmap.fill(Qt.white)
        self.board.setPixmap(self.pixmap)

        self.next_pixmap = QPixmap(self.next_lb.width(), self.next_lb.height())
        self.next_pixmap.fill(Qt.white)
        self.next_lb.setPixmap(self.next_pixmap)

        self.pocket_pixmap = QPixmap(self.pocket_lb.width(), self.pocket_lb.height())
        self.pocket_pixmap.fill(Qt.white)
        self.pocket_lb.setPixmap(self.pocket_pixmap)
        
        self.cur_shape = Shape()

        self.update()
        
        self.timer.start(500, self)

    
    def add_board(self):
        self.back_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20
        for i in range(self.game_height):
            for j in range(self.game_width):
                if self.put_filed[i][j] != -1:
                    self.back_board[i][j] = self.put_filed[i][j]
                elif self.falling_board[i][j] != -1:
                    self.back_board[i][j] = self.falling_board[i][j]
                else:
                    self.back_board[i][j] = -1

    def update(self) -> None:
        
        painter = QPainter(self.pixmap)

        next_painter = QPainter(self.next_pixmap)    
        
        pocket_painter = QPainter(self.pocket_pixmap)
        
        self.add_board()
        
        self.draw_board(self.back_board,painter)

        self.draw_board(self.cur_shape.get_next_shape(),next_painter,4,4,8)

        self.draw_board(self.cur_shape.get_pocket(),pocket_painter,4,4,8)

        self.board.setPixmap(self.pixmap)
        self.next_lb.setPixmap(self.next_pixmap)
        self.pocket_lb.setPixmap(self.pocket_pixmap)


    def draw_board(self,p_board,painter:QPainter,height=20,width=10,n = 1):
        
        colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.cyan, Qt.magenta, Qt.gray, Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkYellow, Qt.darkCyan, Qt.darkMagenta, Qt.darkGray, Qt.lightGray]
        
        

        for i in range(height):
            
            for j in range(width):
                if p_board[i][j] != -1:
                    painter.setBrush((colors[p_board[i][j]]))
                else:
                    painter.setBrush(Qt.white)
                painter.drawRect(j*((self.c_height//n)//height), i*((self.c_height//n)//height), ((self.c_height//n)//height), ((self.c_height//n)//height))

        painter.end()
    
    
        

    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            
            if self.finish_down_line:
                self.finish_down_line = False
                self.use_pocket = False
                
                self.up_board(self.attack_dmg)
                self.attack_dmg = 0

                self.new_block()
                if self.option == 4:
                    self.ai_move.instruct_direction(self,self.put_filed,self.cur_shape)

            else:
                self.one_line_down()
                pass

        else:
            super(Board, self).timerEvent(event)
    
    def attacked(self,atk_dmg=0):
        self.attack_dmg = atk_dmg
        

    def draw_falling(self):
        self.falling_board_clear()
        for i in range(self.cur_shape.get_cur_max_y(self.cur_shape.get_cur_shape())+1):
            for j in range(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())+1):
                if self.cur_shape.get_cur_shape()[i][j] != -1:
                    self.falling_board[i+self.cur_shape.cury][self.cur_shape.curx + j] = self.cur_shape.get_cur_inx()

    def falling_board_clear(self):
        for i in range(self.game_height):
            for j in range(self.game_width):
                self.falling_board[i][j] = -1

    def new_block(self):
        
        self.cur_shape.get_next_inx()
        
        

        if not self.check_put_block(5-(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())//2) - 1,0, self.cur_shape.get_cur_shape()):
            print("game over")
            self.timer.stop()
            self.game_over()
            return
        

        self.cur_shape.curx = 5-(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())//2) - 1
        self.cur_shape.cury = 0

        ## 이 부분에서 ai로 값 전달
        

        self.draw_falling()
        self.update()

    def check_put_block(self,x,y,shape):
        
        if x+self.cur_shape.get_cur_min_x(shape) < 0 or x+self.cur_shape.get_cur_max_x(shape)>= self.game_width:
            return False
        if y+self.cur_shape.get_cur_min_y(shape) < 0:
            print("game over")
            return False
        if y+self.cur_shape.get_cur_max_y(shape) >= self.game_height:            
            return False
        
        for i in range(self.cur_shape.get_cur_max_y(shape),-1,-1):
            for j in range(self.cur_shape.get_cur_max_x(shape),-1,-1):
                if shape[i][j] != -1:
                    if self.put_filed[i+y][j+x] != -1:
                        return False


        return True

    def put_block(self,flag,dx=0,dy=0):
        for i in range(self.cur_shape.get_cur_max_y(self.cur_shape.get_cur_shape()),-1,-1):
                for j in range(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape()),-1,-1):
                    if self.cur_shape.get_cur_shape()[i][j] != -1:
                        self.put_filed[i+self.cur_shape.cury][self.cur_shape.curx + j] = self.cur_shape.get_cur_inx()

                            

    def one_line_down(self):
        if not self.check_put_block(self.cur_shape.curx, self.cur_shape.cury+1, self.cur_shape.get_cur_shape()):
            self.put_block(2)

            self.finish_down_line = True
            self.delete_line()
            return
        
        self.down()
        self.draw_falling()
        self.update()

    def game_over(self):
        self.timer.stop()
        pass

    def delete_line(self):
        self.attack_line_cnt = 0
        attack_dmg = [0,0,2,3,4,10]
        for i,val in enumerate(self.put_filed):
            if -1 not in val:
                self.put_filed.remove(val)
                del self.falling_board[i]
                self.falling_board.insert(0,[-1 for i in range(10)])
                self.put_filed.insert(0,[-1 for i in range(10)])
                self.attack_line_cnt += 1

        self.score += 100*(attack_dmg[self.attack_line_cnt+1])
        self.user_signal.emit(self.score)
        self.attack(attack_dmg[self.attack_line_cnt]) 
        self.attack_line_cnt = 0
        self.update()

    def up_board(self,attack_dmg):
        
        for i in range(attack_dmg):
            
            if -1 not in self.put_filed[i]:
                self.game_over()

    
            del self.put_filed[i]

            r_int = random.randint(0,9)
            
            self.put_filed.append([-2 if i is not r_int else -1 for i in range(10) ])

        self.update()

        
    def attack(self,attack_dmg):
        if self.option == 3 or self.option == 4:
            self.observer.notify_attack(self,attack_dmg)
    
    def left(self):
        self.cur_shape.curx -= 1
    def right(self):
        self.cur_shape.curx += 1
    def down(self):
        self.cur_shape.cury += 1
    def rotate(self):
        if self.check_put_block(self.cur_shape.curx, self.cur_shape.cury, self.cur_shape.rotated(self.cur_shape.get_cur_shape())):
            self.cur_shape.set_cur_shape(self.cur_shape.rotated(self.cur_shape.get_cur_shape()))
    
    def dropDown(self):
        
        dy = self.cur_shape.cury

        while self.check_put_block(self.cur_shape.curx, dy+1, self.cur_shape.get_cur_shape()):
            dy += 1

        self.cur_shape.cury = dy
        self.draw_falling()

    def left_move(self):
        if self.check_put_block(self.cur_shape.curx - 1, self.cur_shape.cury, self.cur_shape.get_cur_shape()):
            self.left()
            
            self.draw_falling()
    
    def right_move(self):
        if self.check_put_block(self.cur_shape.curx + 1, self.cur_shape.cury, self.cur_shape.get_cur_shape()):
            self.right()
            self.draw_falling()
    
    def down_move(self):
        if self.check_put_block(self.cur_shape.curx, self.cur_shape.cury +1, self.cur_shape.get_cur_shape()):
            self.down()
            self.draw_falling()

    def rotate_move(self):
        self.rotate()
        self.update()

    def pocket_move(self):
        tmp = self.cur_shape.get_pocket()
        tmp2 = self.cur_shape.get_pocket_inx()
            
        self.cur_shape.set_pocket(self.cur_shape.get_cur_shape())
        self.cur_shape.set_pocket_inx(self.cur_shape.get_cur_inx())
        if not self.cur_shape.is_pocket:

            self.finish_down_line = True
            self.cur_shape.is_pocket = True    
                
        else:
            self.cur_shape.set_cur_shape(tmp)
            self.cur_shape.set_cur_inx(tmp2)
            self.cur_shape.cury = 0
            self.use_pocket = True





class Tetrominoe:
    def __init__(self):
        self.tetrominoe = [ # i, o, t, j, L,s,z
            [[0,-1,-1,-1],
             [0,-1,-1,-1],
             [0,-1,-1,-1],
             [0,-1,-1,-1]],
             
             [[1,1,-1,-1],
             [1,1,-1,-1],
             [-1,-1,-1,-1],
             [-1,-1,-1,-1]],

             [[-1,2,-1,-1],
             [2,2,2,-1],
             [-1,-1,-1,-1],
             [-1,-1,-1,-1]],

             [[-1,3,-1,-1],
             [-1,3,-1,-1],
             [3,3,-1,-1],
             [-1,-1,-1,-1]],

             [[4,-1,-1,-1],
             [4,-1,-1,-1],
             [4,4,-1,-1],
             [-1,-1,-1,-1]],

             [[-1,5,5,-1],
             [5,5,-1,-1],
             [-1,-1,-1,-1],
             [-1,-1,-1,-1]],

             [[6,6,-1,-1],
             [-1,6,6,-1],
             [-1,-1,-1,-1],
             [-1,-1,-1,-1]]
        ]
    def get_tetro_len(self):
        return len(self.tetrominoe)

class Shape:

    def __init__(self): 
        self.tetro = Tetrominoe()
        self.cur_inx = 0
        self.cur_shape = self.tetro.tetrominoe[self.cur_inx]
        self.next_inx = 0
        self.pocket_inx = -1
        self.curx = 0
        self.cury = 0
        self.blocks = []
        self.get_random_tetro()
        
        self.pocket_shpae = [list([-1 for i in range(4)]) for j in range(4)]  # 4*4
        self.is_pocket = False

    def rotated(self,shape):
        n = max(self.get_cur_max_y(shape),self.get_cur_max_x(shape))+1 # 행 길이
        m = n # 열 길이 
        result = [[0] * m for _ in range(n)] # 회전한 결과를 표시하는 배열
        
        for i in range(n):
            for j in range(m):
                result[j][n-i-1] = shape[i][j]
        
        for i in range(4-m):
            result.append([-1 for i in range(n)])
        
        for i in range(4):
            for j in range(4-n):
                result[i].append(-1)
        
        return result
    
    def get_cur_inx(self):
        return self.cur_inx
    
    def set_cur_inx(self,inx):
        self.cur_inx = inx

    def get_blokcs(self):
        return self.blocks

    def get_cur_min_x(self,shape):
        for i in range(4):
            for j in range(4):
                if shape[j][i] != -1:
                    return i
        return 3

    def get_cur_max_x(self,shape):
        for i in range(3,-1,-1):
            for j in range(4):
                if shape[j][i] != -1:
                    return i
        return 0
    
    def get_cur_min_y(self,shape):
        for i in range(4):
            for j in range(4):
                if shape[i][j] != -1:
                    return i
        return 3
    
    def get_cur_max_y(self,shape):
        for i in range(3,-1,-1):
            for j in range(4):
                if shape[i][j] != -1:
                    return i
        return 0
    
    def get_cur_shape(self):
        return self.cur_shape
    
    def set_cur_shape(self,shape):
        self.cur_shape = shape

    def get_next_inx(self):        
        self.set_cur_inx(self.next_inx)
        self.cur_shape = self.tetro.tetrominoe[self.cur_inx]
        self.get_random_tetro()
        
    def get_next_shape(self):
        return self.tetro.tetrominoe[self.next_inx]

    def get_random_tetro(self):
        if (self.blocks == []):
            self.blocks = list(range(0,self.tetro.get_tetro_len()))
            
            random.shuffle(self.blocks)
            self.next_inx = self.blocks.pop()
        else:
            self.next_inx = self.blocks.pop()
    
    def set_pocket(self,shape):
        self.pocket_shpae = shape

    def get_pocket(self):
        return self.pocket_shpae

    def set_pocket_inx(self,inx):
        self.pocket_inx = inx
    
    def get_pocket_inx(self):
        return self.pocket_inx



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

'''

드롭 만들기 V

좌 우 드롭 포켓 교체 메소드 만들기 V

랜덤으로 내리는거 테스트 V

새로운 레이어 만들어서 그 위에 그리기 V
for문 로테이트
    for문으로 0부터 끝까지 다 돌면서 
    각 위치의 가중치값 구하기
가장 높았던 위치의 가중치값을 기준으로
이동

종료 했을 때 잘 종료 되게 하기 V

점수 추가 V

설정 

'''