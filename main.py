import random
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
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

        

        self.p1_board = QLabel(self)
        self.p1_board.setGeometry(0, 0, int(self.width()*0.4), self.height())
        self.p1_board.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_next = QLabel(self)
        self.p1_next.setGeometry(int(self.width()*0.42), int(self.height()//8 * 2), int(self.width()*0.1), self.height()//8)
        self.p1_next.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_pocket = QLabel(self)
        self.p1_pocket.setGeometry(int(self.width()*0.4), int(self.height()//8 * 4), int(self.width()*0.1), self.height()//8)
        self.p1_pocket.setStyleSheet("background-color: rgb(255, 255, 255);")


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

        self.game = Tetirs(self.p1_board,self.p1_next,self.p1_pocket,self.height(), observer,option) # 수정 해야 하는 부분
        
        if option != 1:
            self.game2 = Tetirs(self.p2_board,self.p2_next,self.p2_pocket,self.height(), observer,option) # 수정 해야 하는 부분

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
            
            if self.game.check_put_block(self.game.cur_shape.curx - 1, self.game.cur_shape.cury, self.game.cur_shape.get_cur_shape()):
                self.game.left()
                self.game.draw_falling()
                

        elif key == Qt.Key_D:
            # self.move(self.curX + 1, self.curY)
            if self.game.check_put_block(self.game.cur_shape.curx + 1, self.game.cur_shape.cury, self.game.cur_shape.get_cur_shape()):
                self.game.right()
                self.game.draw_falling()
                

            # self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_S:
            # self.move(self.curX, self.curY+1)
            if self.game.check_put_block(self.game.cur_shape.curx, self.game.cur_shape.cury +1, self.game.cur_shape.get_cur_shape()):
                self.game.down()
                self.game.draw_falling()
                
            # self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_W:


            self.game.rotate()
            self.game.update()


        elif key == Qt.Key_C and not self.game.use_pocket:
            tmp = self.game.cur_shape.get_pocket()
            tmp2 = self.game.cur_shape.get_pocket_inx()
            
            self.game.cur_shape.set_pocket(self.game.cur_shape.get_cur_shape())
            self.game.cur_shape.set_pocket_inx(self.game.cur_shape.get_cur_inx())
            if not self.game.cur_shape.is_pocket:
                print("pocket is None")

                self.game.finish_down_line = True
                self.game.cur_shape.is_pocket = True    
                
            else:
                self.game.cur_shape.set_cur_shape(tmp)
                self.game.cur_shape.set_cur_inx(tmp2)
                self.game.cur_shape.cury = 0
                self.game.use_pocket = True
                
        elif key == Qt.Key_V:
            self.game.dropDown()
            self.game.update()


        elif key == Qt.Key_Left and self.option != 1 and self.option != 4:
            if self.game2.check_put_block(self.game2.cur_shape.curx - 1, self.game2.cur_shape.cury, self.game2.cur_shape.get_cur_shape()):
                self.game2.left()
                self.game2.draw_falling()
            
        elif key == Qt.Key_Right and self.option != 1 and self.option != 4:
            if self.game2.check_put_block(self.game2.cur_shape.curx + 1, self.game2.cur_shape.cury, self.game2.cur_shape.get_cur_shape()):
                self.game2.right()
                self.game2.draw_falling()
            
        elif key == Qt.Key_Down and self.option != 1 and self.option != 4:
            if self.game2.check_put_block(self.game2.cur_shape.curx, self.game2.cur_shape.cury +1, self.game2.cur_shape.get_cur_shape()):
                self.game2.down()
                self.game2.draw_falling()
                
        elif key == Qt.Key_Up and self.option != 1 and self.option != 4:
                self.game2.rotate()
                self.game2.update()
        
        elif key == Qt.Key_N and not self.game2.use_pocket:
            tmp = self.game2.cur_shape.get_pocket()
            tmp2 = self.game2.cur_shape.get_pocket_inx()
            
            self.game2.cur_shape.set_pocket(self.game2.cur_shape.get_cur_shape())
            self.game2.cur_shape.set_pocket_inx(self.game2.cur_shape.get_cur_inx())
            if not self.game.cur_shape.is_pocket:
                print("pocket is None")

                self.game2.finish_down_line = True
                self.game2.cur_shape.is_pocket = True    
                
            else:
                self.game2.cur_shape.set_cur_shape(tmp)
                self.game2.cur_shape.set_cur_inx(tmp2)
                self.game2.cur_shape.cury = 0
                self.game2.use_pocket = True

        elif key == Qt.Key_M:
            self.game2.dropDown()
            self.game2.update()

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


class Tetirs(QWidget):
    def __init__(self,board:QLabel,next_lb:QLabel,pocket_lb:QLabel,height:int, observer:AttackObserver,option):
        super().__init__()
        self.option = option
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
        attack_dmg = [0,0,2,3,4]
        for i in self.put_filed:
            if -1 not in i:
                self.put_filed.remove(i)
                self.put_filed.insert(0,[-1 for i in range(10)])
                self.attack_line_cnt += 1
            
        self.attack(attack_dmg[self.attack_line_cnt]) 

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
        if self.option == 3:
            self.observer.notify_attack(self,attack_dmg)
    
    def left(self):
        self.cur_shape.curx -= 1
    def right(self):
        self.cur_shape.curx += 1
    def down(self):
        self.cur_shape.cury += 1
    def rotate(self):
        if self.check_put_block(self.cur_shape.curx, self.cur_shape.cury, self.cur_shape.rotated()):
            self.cur_shape.set_cur_shape(self.cur_shape.rotated())
    
    def dropDown(self):
        
        dy = self.cur_shape.cury

        while self.check_put_block(self.cur_shape.curx, dy+1, self.cur_shape.get_cur_shape()):
            dy += 1

        self.cur_shape.cury = dy
        self.draw_falling()


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

    def rotated(self):
        n = max(self.get_cur_max_y(self.cur_shape),self.get_cur_max_x(self.cur_shape))+1 # 행 길이
        m = n # 열 길이 
        result = [[0] * m for _ in range(n)] # 회전한 결과를 표시하는 배열
        
        for i in range(n):
            for j in range(m):
                result[j][n-i-1] = self.cur_shape[i][j]
        
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

드롭 만들기

좌 우 드롭 포켓 교체 메소드 만들기

랜덤으로 내리는거 테스트

새로운 레이어 만들어서 그 위에 그리기
for문 로테이트
    for문으로 0부터 끝까지 다 돌면서 
    각 위치의 가중치값 구하기
가장 높았던 위치의 가중치값을 기준으로
이동



'''