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
        
        self.new_window.show()


class Board(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle("Tetris")
        self.setGeometry(100, 100, 1000, 700)
        MainWindow.center(self,False)

        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0))
        painter.setBrush(QColor(255, 0, 0))
        painter.drawRect(QRect(80, 20, 10, 60))


    def drawRect(self, qp):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(50, 50, 100, 100)


    def one_line_down(self):
        #한줄 내리기
        pass

    def line_down(self):
        #라인 내리기
        pass

    def new_block(self):
        #새로운 블록 생성
        pass

    def delete_line(self):
        #라인 삭제
        pass

    def keyPressEvent(self, event):
        #키보드 이벤트
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

    


        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
