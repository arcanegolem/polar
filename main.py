import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from picbutton import PicButton

import os
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        try:
            os.mkdir("Results")
        except Exception:
            pass

        self.folderPaths = {}

        # Window size
        self.WIDTH = 900
        self.HEIGHT = 540
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)
        self.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet(
            '''
            background: rgb(245, 245, 245);
            border-top-left-radius:15px;
            border-bottom-left-radius:15px;
            border-top-right-radius:15px;
            border-bottom-right-radius:15px;
            '''
        )

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        # Background
        # self.bg = QLabel(self.centralwidget)
        # self.bg.setPixmap(QPixmap("assets/iceberg_background.jpg"))
        # self.bg.resize(600, 600)
        # self.bg.setGeometry(QRect(0, 0, 600, 600))
        self.bg_2d = QLabel(self.centralwidget)
        self.bg_2d.setStyleSheet('''
            background: rgb(220, 220, 220);
            
        ''')
        self.bg_2d.setGeometry(QRect(40, 70, 420, 420))

        # Top left icon
        self.iconMascot = QLabel(self.centralwidget)
        self.iconMascot.setPixmap(QPixmap("assets/icon_xs.png"))
        self.iconMascot.resize(50, 50)
        self.iconMascot.setGeometry(QRect(10, 10, 50, 50))
        self.iconMascot.setStyleSheet('''
            background: transparent;
        ''')

        # Top left name
        font_id = QFontDatabase.addApplicationFont("assets/PlayfairDisplay-VariableFont_wght.ttf")
        font = QFont("Playfair Display")

        self.message = QLabel(self.centralwidget)
        self.message.setText("Полярник")
        self.message.setFont(font)
        self.message.setGeometry(60, 10, 381, 50)
        self.message.setStyleSheet('''
            font-weight: bold;
            font: 30px;
        ''')

        # Exit button
        self.exitButton = PicButton(pixmap=QPixmap("assets/exitbutton.png"), pixmap_hover=QPixmap("assets/exitbutton_hover.png"), pixmap_pressed=QPixmap("assets/exitbutton_hover.png"), parent=self.centralwidget)
        self.exitButton.setGeometry(QRect(870, 10, 20, 20))

        # Close button
        self.closeButton = PicButton(pixmap=QPixmap("assets/closebutton.png"), pixmap_hover=QPixmap("assets/closebutton_hover.png"), pixmap_pressed=QPixmap("assets/closebutton_pressed.png"), parent=self.centralwidget)
        self.closeButton.setGeometry(QRect(845, 10, 20, 20))

        # Add file button
        self.addFileButton = QPushButton(self.centralwidget)
        self.addFileButton.setText("Добавить")
        self.addFileButton.setFont(QFont("Arial"))
        self.addFileButton.setGeometry(500, 500, 80, 20)
        self.addFileButton.setStyleSheet('''
            QPushButton {background: rgb(204, 204, 204);
            border-radius: 5px;
            border-bottom: 3px solid rgb(153, 153, 153);
            border-right: 3px solid rgb(153, 153,153);}
            QPushButton:hover {background: grey;}
            QPushButton:pressed {color: white;}
        ''')

        self.removeFileButton = QPushButton(self.centralwidget)
        self.removeFileButton.setText("Удалить")
        self.removeFileButton.setFont(QFont("Arial"))
        self.removeFileButton.setGeometry(590, 500, 80, 20)
        self.removeFileButton.setStyleSheet('''
            QPushButton {background: rgb(204, 204, 204);
            border-radius: 5px;
            border-bottom: 3px solid rgb(153, 153, 153);
            border-right: 3px solid rgb(153, 153,153);}
            QPushButton:hover {background: grey;}
            QPushButton:pressed {color: white;}
        ''')

        # Process button
        self.processButton = QPushButton(self.centralwidget)
        self.processButton.setText("Начать поиск")
        self.processButton.setGeometry(50, 500, 80, 20)
        self.processButton.setStyleSheet('''
            QPushButton {background: rgb(204, 204, 204);
            border-radius: 5px;
            border-bottom: 3px solid rgb(153, 153, 153);
            border-right: 3px solid rgb(153, 153,153);}
            QPushButton:hover {background: grey;}
            QPushButton:pressed {color: white;}
        ''')

        self.openResultFolderButton = QPushButton(self.centralwidget)
        self.openResultFolderButton.setText("Открыть папку с результатами")
        self.openResultFolderButton.setGeometry(140, 500, 190, 20)
        self.openResultFolderButton.setStyleSheet('''
            QPushButton {background: rgb(204, 204, 204);
            border-radius: 5px;
            border-bottom: 3px solid rgb(153, 153, 153);
            border-right: 3px solid rgb(153, 153,153);}
            QPushButton:hover {background: grey;}
            QPushButton:pressed {color: white;}
        ''')

        # File list label
        self.fileListLabel = QLabel(self.centralwidget)
        self.fileListLabel.setText("Открытые папки:")
        self.fileListLabel.setGeometry(QRect(500, 55, 200, 25))
        self.fileListLabel.setFont(QFont("Arial"))
        self.fileListLabel.setStyleSheet('''
            font:15px;
            background: transparent;
        ''')

        _translate = QCoreApplication.translate
        radius = 15
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QRect(50, 80, 400, 375))
        self.textBrowser.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                       "font: 12pt \"Consolas\" white;\n"
                                       "border-top-left-radius:{0}px;\n"
                                       "border-bottom-left-radius:{0}px;\n"
                                       "border-top-right-radius:{0}px;\n"
                                       "border-bottom-right-radius:{0}px;\n"
                                       "padding: 10px".format(radius)
                                       )
        self.textBrowser.append("< span style = \" color:#ffffff;\" > Output Terminal: < / span >")

        # Progress bar
        self.processProgress = QProgressBar(self.centralwidget)
        self.processProgress.setGeometry(50, 465, 400, 15)
        self.processProgress.setStyleSheet('''
            QProgressBar {background: rgb(250, 250, 250);
                border-bottom: 3px solid rgb(230, 230, 230);
                border-right: 3px solid rgb(230, 230, 230);
                border-radius: 5px;}
            QProgressBar::chunk {
                background-color: rgb(36, 154, 255);
            }
            
        ''')
        self.processProgress.setTextVisible(False)
        self.processProgress.setValue(0)
        #self.processProgress.setVisible(False)


        # File list view
        self.fileList = QListWidget(self.centralwidget)
        self.fileList.setGeometry(QRect(500, 80, 350, 400))
        self.fileList.setStyleSheet('''
            QListWidget {background: rgb(204, 204, 204);
                padding: 10px;
                font: 15px;
                border-bottom: 3px solid rgb(153, 153, 153);
                border-right: 3px solid rgb(153, 153,153);}
            QListWidget:item {border-radius: 10px;
                background: rgb(220, 220, 220);
                border-bottom: 3px solid rgb(153, 153, 153);
                border-right: 3px solid rgb(153, 153,153);}
        ''')

        self.fileList.itemDoubleClicked.connect(self.openFolder)

        '''Test items'''
        # self.testItem = QListWidgetItem()
        # self.testItem.setIcon(QIcon("assets/folder.png"))
        # self.testItem.setText("Batch folder")
        # self.testItem.setFont(QFont("Arial"))
        # self.fileList.addItem(self.testItem)
        #
        # self.testItem2 = QListWidgetItem()
        # self.testItem2.setIcon(QIcon("assets/picture.png"))
        # self.testItem2.setText("Batch folder")
        # self.testItem2.setFont(QFont("Arial"))
        # self.fileList.addItem(self.testItem2)


        # # Search button
        # self.searchButton = PicButton(pixmap=QPixmap("assets/search.png"), pixmap_hover=QPixmap("assets/search_hover.png"), pixmap_pressed=QPixmap("assets/search_pressed.png"), parent=self.centralwidget)
        # self.searchButton.setGeometry(QRect(10, 540, 50, 50))
        #
        # self.uploadButton = PicButton(pixmap=QPixmap("assets/upload.png"), pixmap_hover=QPixmap("assets/upload_hover.png"), pixmap_pressed=QPixmap("assets/upload_pressed.png"), parent=self.centralwidget)
        # self.uploadButton.setGeometry(QRect(70, 540, 50, 50))


        self.load_functionality()

    def load_functionality(self):
        self.exitButton.clicked.connect(sys.exit)
        self.closeButton.clicked.connect(self.showMinimized)
        self.addFileButton.clicked.connect(self.addFolder)
        self.removeFileButton.clicked.connect(self.removeFolder)
        self.processButton.clicked.connect(self.startProcessing)
        self.openResultFolderButton.clicked.connect(self.openResultFolder)

    def openFolder(self, item):
        path = str(self.folderPaths[item.text()])
        path = path.replace("/", "\\")
        subprocess.Popen(["explorer", path])

    def startProcessing(self):
        model = "vadislav_train1260_640px.pt"
        folder_count = 0
        folder_amount = len(self.folderPaths.keys())
        self.processProgress.setValue(0)

        for folder in self.folderPaths:
            folder_count += 1
            value = int((folder_count / folder_amount) * 100)
            #print(self.folderPaths[folder])
            os.system("python detect.py --weights {model_name} --img-size 640 --conf 0.22 --source {folder_path}".format(model_name=model, folder_path=self.folderPaths[folder]))

            self.processProgress.setValue(value)

    def openResultFolder(self):
        path = os.path.abspath("Results")
        subprocess.Popen(["explorer", path])


    def addFolder(self):
        text = QFileDialog.getExistingDirectory(self, 'Select Folder')
        item = QListWidgetItem()
        item.setText(text.split("/")[-1])
        item.setIcon(QIcon("assets/folder.png"))
        text.replace("/", "\\")

        if len(item.text()) > 0 and item.text() not in self.folderPaths.keys():
            self.fileList.addItem(item)
            self.folderPaths[text.split("/")[-1]] = text

    def removeFolder(self):
        selected = self.fileList.selectedItems()

        if not selected:
            return

        for item in selected:
            self.fileList.takeItem(self.fileList.row(item))
            del self.folderPaths[item.text()]

    # def show_start_in_status_menu(self, file_name):
    #     current_time = str(datetime.now().time())
    #     current_time = current_time[:current_time.find('.')]
    #     answer = """< body style = " font-family:'Consolas'; font-size:10pt; font-weight:400; font-style:normal;" >
    #     < p style = " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;" >
    #     < span style = " color:#ffffff;" >[{}]Детекция медведей в папке - {}...< / span >< / p >< / body >""".format(
    #         current_time, file_name)
    #     self.textBrowser.append(answer)

    # def show_data_in_status_menu(self, counter):
    #     current_time = str(datetime.now().time())
    #     current_time = current_time[:current_time.find('.')]
    #     answer = """< body style = " font-family:'Consolas'; font-size:10pt; font-weight:400; font-style:normal;" >
    #     < p style = " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;" >
    #     < span style = " color:#ffffff;" >[{}]Найдено: {} < / span >< / p >< / body >""".format(current_time, counter)
    #     self.textBrowser.append(answer)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton and self.moveFlag:
                self.move(event.globalPos() - self.movePosition)
                self.setCursor(QCursor(Qt.ClosedHandCursor))
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        self.moveFlag = False
        self.setCursor(Qt.ArrowCursor)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())