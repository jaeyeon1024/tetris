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

        print(self.option)

        self.p1_board = QLabel(self)
        self.p1_board.setGeometry(0, 0, int(self.width()*0.4), self.height())
        self.p1_board.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_next = QLabel(self)
        self.p1_next.setGeometry(int(self.width()*0.42), int(self.height()//8 * 2), int(self.width()*0.1), self.height()//8)
        self.p1_next.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_pocket = QLabel(self)
        self.p1_pocket.setGeometry(int(self.width()*0.42), int(self.height()//8 * 4), int(self.width()*0.1), self.height()//8)

        self.p2_board = QLabel(self)
        self.p2_board.setGeometry(int(self.width()*0.6), 0, int(self.width()*0.4), self.height())
        self.p2_board.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.board_resize()

        self.p2_next = QLabel(self)
        self.p2_next.setGeometry(int(self.width()*0.46), int(self.height()//8 * 2), int(self.width()*0.1), self.height()//8)
        self.p2_next.setStyleSheet("background-color: rgb(255, 255, 255);")

        MainWindow.center(self,False)

        self.game = Tetirs(self.p1_board,self.p1_next,self.height()) # 수정 해야 하는 부분
        
        if option != 1:
            self.game2 = Tetirs(self.p2_board,self.p2_next,self.height()) # 수정 해야 하는 부분

    def board_resize(self):
        self.p1_board.setGeometry(0, 0, (self.p1_board.width()//10)*10, self.height())
        self.p2_board.setGeometry(int(self.width()*0.6), 0, (self.p2_board.width()//10)*10, self.height())

        self.p1_next.setGeometry(int(self.width()*0.4), int(self.height()//8 * 2), (self.p1_next.width()//4)*4, self.height()//8)
        self.p2_next.setGeometry(int(self.width()*0.5), int(self.height()//8 * 2), (self.p2_next.width()//4)*4, self.height()//8)

        

    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_A and not self.game.finish_down_line:
            
            # self.move(self.curX - 1, self.curY)
            
            if self.game.check_put_block(self.game.cur_shape.curx - 1, self.game.cur_shape.cury, self.game.cur_shape.get_cur_shape()):
                self.game.move(1,-1,0)
                self.game.cur_shape.curx -= 1

        elif key == Qt.Key_D:
            # self.move(self.curX + 1, self.curY)
            if self.game.check_put_block(self.game.cur_shape.curx + 1, self.game.cur_shape.cury, self.game.cur_shape.get_cur_shape()):
                self.game.move(1,1,0)
                self.game.cur_shape.curx += 1

            # self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_S:
            # self.move(self.curX, self.curY+1)
            if self.game.check_put_block(self.game.cur_shape.curx, self.game.cur_shape.cury +1, self.game.cur_shape.get_cur_shape()):
                self.game.move(1,0,1)
                self.game.cur_shape.cury += 1
            # self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_W:
            # self.tryMove(self.curPiece, self.curC, self.curR - 1)
            if self.game.check_put_block(self.game.cur_shape.curx, self.game.cur_shape.cury, self.game.cur_shape.rotated()):
                for i in range(self.game.cur_shape.get_cur_max_y(self.game.cur_shape.get_cur_shape())+1):
                    for j in range(self.game.cur_shape.get_cur_max_x(self.game.cur_shape.get_cur_shape())+1):
                        if self.game.cur_shape.get_cur_shape()[i][j] != -1:
                            self.game.list_board[i+self.game.cur_shape.cury][self.game.cur_shape.curx + j] = -1

                self.game.cur_shape.set_cur_shape(self.game.cur_shape.rotated())
                self.game.update()


        elif key == Qt.Key_Left:
            if self.game2.check_put_block(self.game2.cur_shape.curx - 1, self.game2.cur_shape.cury, self.game2.cur_shape.get_cur_shape()):
                self.game2.move(1,-1,0)
                self.game2.cur_shape.curx -= 1
            
        elif key == Qt.Key_Right:
            if self.game2.check_put_block(self.game2.cur_shape.curx + 1, self.game2.cur_shape.cury, self.game2.cur_shape.get_cur_shape()):
                self.game2.move(1,1,0)
                self.game2.cur_shape.curx += 1
            
        elif key == Qt.Key_Down:
            if self.game2.check_put_block(self.game2.cur_shape.curx, self.game2.cur_shape.cury +1, self.game2.cur_shape.get_cur_shape()):
                self.game2.move(1,0,1)
                self.game2.cur_shape.cury += 1
        elif key == Qt.Key_Up:
            if self.game2.check_put_block(self.game2.cur_shape.curx, self.game2.cur_shape.cury, self.game2.cur_shape.rotated()):
                for i in range(self.game2.cur_shape.get_cur_max_y(self.game2.cur_shape.get_cur_shape())+1):
                    for j in range(self.game2.cur_shape.get_cur_max_x(self.game2.cur_shape.get_cur_shape())+1):
                        if self.game2.cur_shape.get_cur_shape()[i][j] != -1:
                            self.game2.list_board[i+self.game2.cur_shape.cury][self.game2.cur_shape.curx + j] = -1
                self.game2.cur_shape.set_cur_shape(self.game2.cur_shape.rotated())
                self.game2.update()


class Tetirs(QWidget):
    def __init__(self,board:QLabel,next_lb:QLabel,height:int):
        super().__init__()
        self.initUI(board,next_lb,height)

    def initUI(self,board:QLabel,next_lb:QLabel,height:int):
        self.board = board
        self.c_height = height
        self.next_lb = next_lb

        self.finish_down_line = True # 한줄이 다 내려왔는지 확인하는 변수 

        self.timer = QBasicTimer()

        self.game_width = 10
        self.game_height = 20

        self.list_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20

        self.put_filed = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20

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

        self.cur_shape = Shape()
        self.update()
        
        self.timer.start(300, self)
        

    def update(self) -> None:
        
        painter = QPainter(self.pixmap)

        next_painter = QPainter(self.next_pixmap)    
        
        self.draw_board(self.list_board,painter)

        self.draw_board(self.cur_shape.get_next_shape(),next_painter,4,4,8)

        self.board.setPixmap(self.pixmap)
        self.next_lb.setPixmap(self.next_pixmap)
        


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
                self.new_block()
            else:
                self.one_line_down()
                pass

        else:
            super(Board, self).timerEvent(event)
    
    

    def new_block(self):
        
        self.cur_shape.get_next_inx()
        
        if not self.check_put_block(5-(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())//2) - 1,0, self.cur_shape.get_cur_shape()):
            print("game over")
            self.timer.stop()
            self.game_over()
            return
        
        for i in range(self.cur_shape.get_cur_max_y(self.cur_shape.get_cur_shape())+1):
            for j in range(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())+1):
                if self.cur_shape.get_cur_shape()[i][j] != -1:
                    self.list_board[i][5-(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())//2) - 1 + j] = self.cur_shape.get_cur_inx()
        self.cur_shape.curx = 5-(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape())//2) - 1
        self.cur_shape.cury = 0
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

    def move(self,flag,dx=0,dy=0):
        for i in range(self.cur_shape.get_cur_max_y(self.cur_shape.get_cur_shape()),-1,-1):
                for j in range(self.cur_shape.get_cur_max_x(self.cur_shape.get_cur_shape()),-1,-1):
                    if self.cur_shape.get_cur_shape()[i][j] != -1:
                        if flag == 1:
                            self.list_board[i+self.cur_shape.cury+dy][self.cur_shape.curx +dx +j] = self.cur_shape.get_cur_inx()
                            self.list_board[i+self.cur_shape.cury][ self.cur_shape.curx + j] = -1
                        if flag == 2:
                            self.list_board[i+self.cur_shape.cury][self.cur_shape.curx + j] = self.cur_shape.get_cur_inx() 
                            self.put_filed[i+self.cur_shape.cury][self.cur_shape.curx + j] = self.cur_shape.get_cur_inx()

                            

    def one_line_down(self):
        if not self.check_put_block(self.cur_shape.curx, self.cur_shape.cury+1, self.cur_shape.get_cur_shape()):
            self.move(2)

            self.finish_down_line = True
            self.delete_line()
            return
        

        self.move(1,0,1)
        self.cur_shape.cury += 1
        self.update()

    def game_over(self):
        self.timer.stop()
        pass

    def delete_line(self):
        self.attack_line_cnt = 0
        attack_dmg = [0,0,1,2,4]
        for i in self.list_board:
            if -1 not in i:
                self.list_board.remove(i)
                self.put_filed.remove(i)
                self.list_board.insert(0,[-1 for i in range(10)])
                self.put_filed.insert(0,[-1 for i in range(10)])
                self.attack_line_cnt += 1
            
        #self.attack(attack_dmg[self.attack_line_cnt]) 공격을 한다면

        self.update()

    # def up_board(self):
        
    #     self.list_board.append([-2 for i in range(10) if i is not random.randint(0,9)])
    #     self.put_filed.append([-2 for i in range(10) if i is not random.randint(0,9)])


        
    #     pass
    



class Tetrominoe:
    def __init__(self):
        self.tetrominoe = [ # i, o, t, j, L,s,z
            [[-1,-1,0,-1],
             [-1,-1,0,-1],
             [-1,-1,0,-1],
             [-1,-1,0,-1]],
             
             [[-1,-1,-1,-1],
             [-1,1,1,-1],
             [-1,1,1,-1],
             [-1,-1,-1,-1]],

             [[-1,-1,-1,-1],
             [-1,2,-1,-1],
             [2,2,2,-1],
             [-1,-1,-1,-1]],

             [[-1,-1,3,-1],
             [-1,-1,3,-1],
             [-1,3,3,-1],
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
        self.curx = 0
        self.cury = 0
        self.blocks = []
        self.get_random_tetro()

    def rotated(self):
        n = 4 # 행 길이
        m = 4 # 열 길이 
        result = [[0] * n for _ in range(m)] # 회전한 결과를 표시하는 배열

        for i in range(n):
            for j in range(m):
                result[j][n-i-1] = self.cur_shape[i][j]
        return result
    
    def get_cur_inx(self):
        return self.cur_inx
    
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
        self.cur_inx = self.next_inx
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
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
