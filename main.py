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
        self.p1_btn.clicked.connect(self.open_new_window)

        self.p2_btn = QPushButton("2인용", self)
        self.p2_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.p2_btn.clicked.connect(self.open_new_window)

        self.vs2_btn = QPushButton("2인 대전", self)
        self.vs2_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vs2_btn.clicked.connect(self.open_new_window)

        self.com_btn = QPushButton("컴퓨터 대전", self)
        self.com_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)    
        self.com_btn.clicked.connect(self.open_new_window)

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

    def open_new_window(self):
        self.new_window = Board()
        self.new_window.start()
        self.new_window.show()


class Board(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.finish_down_line = True

        self.timer = QBasicTimer()

        self.game_width = 10
        self.game_height = 20

        self.setWindowTitle("Tetris")
        self.setGeometry(100, 100, 1000, 700)

        self.p1_board = QLabel(self)
        self.p1_board.setGeometry(0, 0, int(self.width()*0.4), self.height())
        self.p1_board.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p2_board = QLabel(self)
        self.p2_board.setGeometry(int(self.width()*0.6), 0, int(self.width()*0.4), self.height())
        self.p2_board.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.p1_list_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20
        self.p2_list_board = [list([-1 for i in range(10)]) for j in range(20)]  # 10*20

        self.board_resize()



        MainWindow.center(self,False)
        
    def board_resize(self):
        self.p1_board.setGeometry(0, 0, (self.width()//10)*10, self.height())
        self.p2_board.setGeometry(int(self.width()*0.6), 0, (self.width()//10)*10, self.height())

    def set_space_x_size(self):
        self.space_size = self.p1_board.width()//10

    def get_space_x_size(self):
        return self.space_size
    
    def set_space_y_size(self):
        self.space_size = self.p1_board.height()//20

    def get_space_y_size(self):
        return self.space_size

    def start(self):

        self.cur_blocks_list = []

        self.set_space_x_size()
        self.set_space_y_size()

        self.p1_pixmap = QPixmap(int(self.width()*0.4), self.height())
        self.p1_pixmap.fill(Qt.white)
        self.p1_board.setPixmap(self.p1_pixmap)
        
        self.p2_pixmap = QPixmap(int(self.width()*0.4), self.height())
        self.p2_pixmap.fill(Qt.white)
        self.p2_board.setPixmap(self.p2_pixmap)
        
        next_block = self.next_block()

        self.update()

        self.timer.start(200, self)

    def update(self):
        
        p1_painter = QPainter(self.p1_pixmap)
        p2_painter = QPainter(self.p2_pixmap)

    
        self.draw_board(self.p1_list_board,p1_painter)
        self.draw_board(self.p2_list_board,p2_painter)



        self.p1_board.setPixmap(self.p1_pixmap)
        self.p2_board.setPixmap(self.p2_pixmap)

        

    def draw_board(self,p_board,painter:QPainter):
        
        colors = [Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.cyan, Qt.magenta, Qt.gray, Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkYellow, Qt.darkCyan, Qt.darkMagenta, Qt.darkGray, Qt.lightGray]

        

        for i in range(self.game_height):
            for j in range(self.game_width):
                if p_board[i][j] != -1:
                    painter.setBrush((colors[p_board[i][j]]))
                else:
                    painter.setBrush(Qt.white)
                painter.drawRect(j*self.get_space_x_size(), i*self.get_space_y_size(), self.get_space_x_size(), self.get_space_y_size())

        painter.end()
        

    def block_size(self) -> int:
        #블록 사이즈
        pass

    def put_block(self):
        pass

    def one_line_down(self):
        
        #한줄 내리기
        pass

    def line_down(self):
        #라인 내리기
        pass
    
    def new_block(self):
        self.cur_block = self.next_pices
        self.curx = self.game_width // 2 + 1
        self.cury = 0
        self.next_block()

    def next_block(self):
        self.shape = Shape()
        if self.cur_blocks_list == []:
            self.cur_blocks_list = self.shape.get_random_index()
            self.next_pices = self.cur_blocks_list.pop()
            return self.next_pices
        else:
            self.next_pices = self.cur_blocks_list.pop()
            return self.next_pices

    def delete_line(self):
        #라인 삭제
        pass

    def keyPressEvent(self, event):
        print(event.key())
        pass

    def paintEvent(self, event):
        #화면 그리기
        pass

    def check_game_over(self):
        #게임 오버 체크
        pass

    def check_line(self):
        #라인 체크
        pass


    def timerEvent(self, event):

        if event.timerId() == self.timer.timerId():
            
            if self.finish_down_line:
                self.finish_down_line = False
                self.new_block()
            else:
                self.one_line_down()

        else:
            super(Board, self).timerEvent(event)
    
    


        self.show()

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
             [3,3,3,-1],
             [-1,-1,-1,-1]],

             [[4,-1,-1,-1],
             [4,-1,-1,-1],
             [4,4,-1,-1],
             [-1,-1,-1,-1]],

             [[-1,-1,-1,-1],
             [-1,5,5,-1],
             [5,5,-1,-1],
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
        self.tetrominoe = Tetrominoe()

    def rotated(array_2d):
        n = len(array_2d) # 행 길이
        m = len(array_2d[0]) # 열 길이 
        result = [[0] * n for _ in range(m)] # 회전한 결과를 표시하는 배열

        for i in range(n):
            for j in range(m):
                result[j][n-i-1] = array_2d[i][j]
        return result

    def get_random_index(self) -> list:
        arr = list(range(self.tetrominoe.get_tetro_len()))
        random.shuffle(arr)
        return arr


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
