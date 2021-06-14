from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, 
                             QMessageBox, QPushButton, QAction, QVBoxLayout, 
                             QHBoxLayout, QDockWidget, QFileDialog, QTabWidget)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QDir

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ App ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(QMainWindow):
# +++++++++++++++++++++++++++++__init__ +++++++++++++++++++++++++++++++
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('img/DAQ.svg'))
        self.setWindowTitle('DAQ')
        self.setGeometry(0, 0, 1500, 600)

        self.initUI()
# +++++++++++++++++++++++++++++ initUI ++++++++++++++++++++++++++++++++
    def initUI(self):
        self.darkTheme()
        self.setStyleSheet("""QDockWidget::title {text-align: center;}""")
        self.center()
################################ Menu #################################
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')
########################## Control Buttons ############################
        ######################## Exit #################################
        exitButton = QAction(QIcon('img/close.svg'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        ######################## open #################################
        openAct = QAction(QIcon('img/open.svg'),'Open files', self)
        openAct.setShortcut("Ctrl+O")
        openAct.triggered.connect(self.openFile)
        ######################## Play #################################
        PlayAct = QAction(QIcon('img/play.svg'),'Play', self)
        #PlayAct.triggered.connect(self.start)
        ######################## Stop #################################
        StopAct = QAction(QIcon('img/stop.svg'), 'Stop', self)
        #StopAct.triggered.connect(self.stop)
        ####################### About #################################
        aboutButton = QAction(QIcon('img/info.svg'), 'About', self)
        aboutButton.triggered.connect(self.aboutDialog)
        helpMenu.addAction(aboutButton)
        # ------------------------------ Test ---------------------------------
        testAct = QAction(QIcon('img/test.png'), 'Test', self)
        testAct.triggered.connect(self.test)
####################### Add buttons on toolbar ########################
        toolbar = self.addToolBar('Tools')
        toolbar.addAction(exitButton)
        toolbar.addSeparator()
        toolbar.addAction(openAct)
        toolbar.addSeparator()
        toolbar.addAction(PlayAct)
        toolbar.addAction(StopAct)
        toolbar.addSeparator()
        toolbar.addAction(aboutButton)
        toolbar.addSeparator()
        toolbar.addAction(testAct)
################## Set view widgets on dockedWidget ###################
        ##################### Create tabs #############################
        self.tabs = QTabWidget()
        self.viewWidgetsPage1 = QWidget()
        self.viewWidgetsPage2 = QWidget()

        self.tabs.addTab(self.viewWidgetsPage1, "Page 1")
        self.tabs.addTab(self.viewWidgetsPage2, "Page 2")
        self.setCentralWidget(self.tabs)

        viewWidgetsVlayout = QVBoxLayout()
        self.tabs.setLayout(viewWidgetsVlayout)
        self.controlDockWidget = QDockWidget('Monitoring')
        self.controlDockWidget.setWidget(self.tabs)
        self.addDockWidget(Qt.RightDockWidgetArea, self.controlDockWidget)
################# Set control widgets on dockedWidget #################
        self.controlWidgets = QWidget()
        controlWidgetsVlayout = QVBoxLayout()
        self.controlWidgets.setLayout(controlWidgetsVlayout)
        self.controlDockWidget = QDockWidget('Control')
        self.controlDockWidget.setWidget(self.controlWidgets)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.controlDockWidget)

        self.show()
# +++++++++++++++++++++++++++++ Center ++++++++++++++++++++++++++++++++
    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
# ++++++++++++++++++++++++++ About dialog +++++++++++++++++++++++++++++
    def aboutDialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("About")
        msg.setText("DAQ")
        msg.setInformativeText("This is test DAQ program")
        msg.exec_()
# ++++++++++++++++++++++++++++ openFile +++++++++++++++++++++++++++++++
    def openFile(self):
        OpenfilePath, _ = QFileDialog.getOpenFileName(self, 'Select file', QDir.currentPath(), "DAT Files(*.dat)")
        if OpenfilePath != '':
            print("Path is good!")
            print(OpenfilePath)
        else:
            print("Path is bad!")
# +++++++++++++++++++++++++++ Dark theme ++++++++++++++++++++++++++++++
    def darkTheme(self): 
        pal = QApplication.palette()
        pal.setColor(QPalette.Window, QColor(53, 53, 53))
        pal.setColor(QPalette.WindowText, Qt.white)
        pal.setColor(QPalette.Base, QColor(25, 25, 25))
        pal.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        pal.setColor(QPalette.ToolTipBase, Qt.white)
        pal.setColor(QPalette.ToolTipText, Qt.white)
        pal.setColor(QPalette.Text, Qt.white)
        pal.setColor(QPalette.Button, QColor(53, 53, 53))
        pal.setColor(QPalette.ButtonText, Qt.white)
        pal.setColor(QPalette.BrightText, Qt.red)
        pal.setColor(QPalette.Link, QColor(42, 130, 218))
        pal.setColor(QPalette.Highlight, QColor(42, 130, 218))
        pal.setColor(QPalette.HighlightedText, Qt.black)        
        QApplication.setPalette(pal)
# ++++++++++++++++++++++++++ test button ++++++++++++++++++++++++++++++
    def test(self): 
        print("test")
#######################################################################
#######################################################################
if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    ex = App()
    app.exec_()