from PySide.QtCore import *
from PySide.QtGui import *
import libs.settingsDialog as settingsDialog
import testTread as libthread 
import libs.libserial as libserial
import time
import os
import re
import datetime




icons_folder = "resources/icons/"
nickname = "Guest"
default_save_folder = os.path.expanduser('~')
serial_port = None
intervaltime = 6





class MainWindow(QMainWindow):

    def __init__(self):
        super(self.__class__,self).__init__()
        self.nickname = nickname
        self.default_save_folder = default_save_folder
        self.serial_port = serial_port
        self.intervaltime = intervaltime
        self.counter = 0
        self.iswaitingData = False
        self.receive = None
        self.send = None


        
        self.menuBar = QMenuBar()
        self.Menusettings = self.menuBar.addMenu('Settings')
        self.actionOpenSettings = QAction("Open Settings",self)
        self.actionOpenSettings.triggered.connect(self.openSettings)
        self.Menusettings.addAction(self.actionOpenSettings)
        self.MenuSendFile = self.menuBar.addMenu('Send File')
        self.actionSendFile = QAction("Choose File to Send",self)
        #add trigger 
        self.MenuSendFile.addAction(self.actionSendFile)
        self.MenuHelp = self.menuBar.addMenu('Help')
        self.actionOpenHelp = QAction("Manual",self)
        self.actionOpenAbout = QAction("About",self)
        self.MenuHelp.addAction(self.actionOpenHelp)
        self.MenuHelp.addAction(self.actionOpenAbout)

        self.setMenuBar(self.menuBar)

        
        
        self.layoutCentralWidget = QVBoxLayout()

        self.listWidget = QListWidget()
        self.inputText = QTextEdit()
        self.sendButton = QPushButton("Send")
        self.sendButton.clicked.connect(self.sendMsg)

        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearSendingArea)

        self.horizontalButtonLayout = QHBoxLayout()
        self.horizontalButtonLayout.addWidget(self.sendButton)
        self.horizontalButtonLayout.addWidget(self.clearButton)

        self.layoutCentralWidget.addWidget(self.listWidget)
        self.layoutCentralWidget.addWidget(self.inputText)
        self.layoutCentralWidget.addLayout(self.horizontalButtonLayout)

        self.progressBar = QProgressBar()

        self.downDockWidget = QDockWidget()
        self.downDockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.downDockWidget.setWidget(self.progressBar)
        self.addDockWidget(Qt.BottomDockWidgetArea,self.downDockWidget)

        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Started!!!")
        self.setStatusBar(self.statusBar)

        win = QWidget()
        win.setLayout(self.layoutCentralWidget)
        self.setCentralWidget(win)

        self.setGeometry(200,200,500,500)
        self.setWindowTitle("SerialChat Application")
        self.setWindowIcon(QIcon(icons_folder+'chat.ico'))
        self.show()


    def startThreads(self):
        if self.receive == None:
            print("Starting Threads...")
            self.send = libthread.Send(self)
            self.receive = libthread.Receive(self.serial_port)

            self.receive.startRCV.connect(self.startRCV)
            self.receive.endRCV.connect(self.endRCV)
            self.receive.catchESF.connect(self.catchESF)
            self.receive.catchEOP.connect(self.catchEOP)

            self.receive.start()



    def openSettings(self):
        settingsDialog.SettingsWindow(self)

    def sendFile(self):
        pass

    def openAbout(self):
        pass

    def checkIfsettingsROK(self):
        
        if self.receive == None:
            msgBox = QMessageBox(icon=QMessageBox.Warning,text="Check your Settings...")
            msgBox.setWindowTitle('Warning')
            msgBox.exec_()
            self.inputText.clear()
            return False
        return True

    def sendMsg(self):
        
        if not self.iswaitingData and self.checkIfsettingsROK():

            self.send.text = self.inputText.toPlainText()
            find = re.search("^\s*$",self.send.text)
            if not find:
                tt = "[ "+self.nickname+" (me) @ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ]: "+self.send.text
                tmp = QListWidgetItem(tt)
                tmp.setForeground(QColor('blue'))
                self.listWidget.addItem(tmp)
                self.listWidget.scrollToBottom()
                self.send.start()
                self.inputText.clear()
        elif self.iswaitingData:
            print("Cannot send yet... im receiving data...")

    def clearSendingArea(self):
        self.inputText.clear()

    @Slot()
    def startRCV(self,x):
        self.iswaitingData = True
        print("Start Receiving...")
        
    def reassembleData(self,rdata):

        end_text = ''
        count = 0
        print self.receive.pieces
        print self.receive.remain
        print self.receive.nickname
        if self.receive.pieces > 0 :
            for chunk in range(0,self.receive.pieces):
                print(rdata['data_'+str(chunk)])
                end_text += rdata['data_'+str(chunk)]
        if self.receive.remain > 0:
            print("remain") 
            print(rdata['data_remain'])
            end_text += rdata['data_remain']
        return end_text

                

    @Slot()
    def endRCV(self):
        self.iswaitingData = False
        self.counter = 0
        print("Ended receiving the data...")
        print(self.receive.data)
        tt = "[ "+self.receive.nickname+" @ "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" ]: "+self.reassembleData(self.receive.data)
        self.receive.clear_vars()
        tmp = QListWidgetItem(tt)
        tmp.setForeground(QColor('green'))
        self.listWidget.addItem(tmp)
        self.listWidget.scrollToBottom()

    @Slot()
    def catchESF(self,specs):
        print("Found Spec of Files...")
        print(specs)

    @Slot()
    def catchEOP(self,len_of_data):
        print("Catch %i"%int(len_of_data))
        self.counter += int(len_of_data)
        print(self.counter)



    













##########################end class Main Window#############################

app = QApplication([])
window = MainWindow()
app.exec_()
