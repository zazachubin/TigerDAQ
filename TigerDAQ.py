from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QMessageBox, QPushButton, QAction, QVBoxLayout,
                             QHBoxLayout, QDockWidget, QFileDialog, QTabWidget,
                             QGridLayout, QGroupBox, QLineEdit, QLabel, QComboBox)
from PyQt5.QtGui import QIcon, QPalette, QColor, QDoubleValidator
from PyQt5.QtCore import Qt, QDir, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import numpy as np
import binascii
import random
import copy
import os

# Global data buffer
DATA = {}
# Global control of threads (run & stop)
_Run  = False
# Control debugging
debug = False

# ~~~~~~~~~~~~~~~~~~~~~~~~ Plot 2D Histogram ~~~~~~~~~~~~~~~~~~~~~~~~~~
class Plot2DHistogram(FigureCanvasQTAgg):
# +++++++++++++++++++++++++++++ __init__ ++++++++++++++++++++++++++++++
    def __init__(self, title="title", Xlabel="X", Ylabel="Y", parent=None):
        self.title = title
        self.Xlabel = Xlabel
        self.Ylabel = Ylabel

        self.X = []
        self.Y = []

        self.fig, self.ax = plt.subplots(tight_layout=True)
        FigureCanvasQTAgg.__init__(self, self.fig)
        ########## Statistical information font style #################
        self.Afont ={'family': 'serif',
                     'color':  'Red',
                     'weight': 'normal',
                     'size': 9,
                    }
        ######### Statistical information on the graph ################
        statistics_text = AnchoredText( s='Entries: --\nMinX: --\nMinY: --\nMaxX: --\nMaxY: --\nMeanX: --\nMeanY: --\nSd_X: --\nSd_Y: --',
                                        loc=1, frameon=False, prop=self.Afont)
        self.ax.add_artist(statistics_text)
        ##################### 2D histogram ############################
        self.hist, self.xbins, self.ybins, self.im = self.ax.hist2d(self.X, self.Y, cmap = 'plasma')
        ############### 2D histogram color bar ########################
        self.cbar = self.fig.colorbar(self.im, ax=self.ax)
        self.cbar.set_label('Counts')
        self.cbar.minorticks_on()
        ################# 2D histogram labels #########################
        self.ax.set(xlabel=self.Xlabel, ylabel=self.Ylabel, title=self.title)
        ################ 2D histogram axis mode #######################
        self.ax.autoscale_view()
        self.ax.minorticks_on()
        self.ax.grid()
# +++++++++++++++++++++++++++ update2Hist +++++++++++++++++++++++++++++
    def update2dHist(self, data):
        ############### Clear 2D histogram data #######################
        self.ax.clear()
        ################### 2D histogram data #########################
        self.X = data[0]
        self.Y = data[1]
        try:
            ############## Calculate X maximum ########################
            x_max = np.max(self.X)
            Data_Entries = np.size(self.Y)
            ############# Calculate X statistics ######################
            Data_min_X = round(np.min(self.X),2)
            Data_max_X = round(np.max(self.X),2)
            Data_mean_X = round(np.mean(self.X),2)
            Data_std_X = round(np.std(self.X),2)
            ############# Calculate Y statistics ######################
            Data_min_Y = round(np.min(self.Y),2)
            Data_max_Y = round(np.max(self.Y),2)
            Data_mean_Y = round(np.mean(self.Y),2)
            Data_std_Y = round(np.std(self.Y),2)
            ##### Statistical information on the graph ################
            statistics_text = AnchoredText( s='Entries: {}\nMinX: {}\nMinY: {}\nMaxX: {}\nMaxY: {}\nMeanX: {}\nMeanY: {}\nSd_X: {}\nSd_Y: {}'.format(Data_Entries,
                                                                                                                                                     Data_min_X,
                                                                                                                                                     Data_min_Y,
                                                                                                                                                     Data_max_X,
                                                                                                                                                     Data_max_Y,
                                                                                                                                                     Data_mean_X,
                                                                                                                                                     Data_mean_Y,
                                                                                                                                                     Data_std_X,
                                                                                                                                                     Data_std_Y),
                                            loc=1, frameon=False, prop=self.Afont)
            self.ax.add_artist(statistics_text)
            ########### Update 2D histogram data ######################
            self.hist, self.xbins, self.ybins, self.im = self.ax.hist2d(self.X, self.Y, cmap = 'plasma', bins=x_max)
            ######## Update 2D histogram color bar ####################
            self.cbar.update_normal(self.im)
            self.cbar.minorticks_on()
        except ValueError:
            pass
        ############# Update 2D histogram labels ######################
        self.ax.set(xlabel=self.Xlabel, ylabel=self.Ylabel, title=self.title)
        ############ Update 2D histogram axis mode ####################
        self.ax.autoscale_view()
        self.ax.minorticks_on()
        self.ax.grid()
        ################## Draw 2D histogram ##########################
        self.draw()
# ++++++++++++++++++++++++++++ setXlabel ++++++++++++++++++++++++++++++
    def setXlabel(self, Xlabel):
        self.Xlabel = Xlabel
# ++++++++++++++++++++++++++++ setYlabel ++++++++++++++++++++++++++++++
    def setYlabel(self, Ylabel):
        self.Ylabel = Ylabel

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Plot Histogram ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlotHistogram(FigureCanvasQTAgg):
# +++++++++++++++++++++++++++++ __init__ ++++++++++++++++++++++++++++++
    def __init__(self,title,Xlabel="X",Ylabel="Y",parent=None):
        self.title = title
        self.Xlabel = Xlabel
        self.Ylabel = Ylabel

        fig, self.ax = plt.subplots(tight_layout=True)
        FigureCanvasQTAgg.__init__(self, fig)
        ########## Statistical information font style #################
        self.Afont ={'family': 'serif',
                     'color':  'red',
                     'weight': 'normal',
                     'size': 9,
                    }
        ############### Initialization histogram ######################
        self.ax.hist([], color = 'green', edgecolor = 'black')
        ######### Statistical information on the graph ################
        statistics_text = AnchoredText( s='Entries: --\nMin: --\nMax: --\nMean: --\nMedian: --\nSd: --',
                                        loc=1, frameon=False, prop=self.Afont)
        self.ax.add_artist(statistics_text)
        ################## Histogram labels ##########################
        self.ax.set(xlabel=self.Xlabel, ylabel=self.Ylabel, title=self.title)
        ################# Histogram axis mode ########################
        self.ax.autoscale_view()
        self.ax.grid()
# ++++++++++++++++++++++++++++ updateHist +++++++++++++++++++++++++++++
    def updateHist(self, data):
        ############### Clear 2D histogram data #######################
        self.ax.clear()
        ################# Calculate statistics ########################
        Data_Entries = np.size(data)
        Data_min = round(np.min(data),2)
        Data_max = round(np.max(data),2)
        Data_mean = round(np.mean(data),2)
        Data_median = round(np.median(data),2)
        Data_std = round(np.std(data),2)
        ######### Statistical information on the graph ################
        statistics_text = AnchoredText( s='Entries: {}\nMin: {}\nMax: {}\nMean: {}\nMedian: {}\nSd: {}'.format(Data_Entries, Data_min, Data_max, Data_mean, Data_median, Data_std),
                                        loc=1, frameon=False, prop=self.Afont)
        self.ax.add_artist(statistics_text)
        ################# Update Histogram data #######################
        try:
            bins = np.linspace(min(data), max(data))
            self.ax.hist(data, color = 'green', bins=bins, edgecolor = 'black')
        except ValueError:
            self.ax.hist(data, color = 'green', edgecolor = 'black')
        ################ Update Histogram labels ######################
        self.ax.set(xlabel=self.Xlabel, ylabel=self.Ylabel, title=self.title)
        ############## Update Histogram axis mode #####################
        self.ax.autoscale_view()
        self.ax.grid()
        #################### Draw Histogram ###########################
        self.draw()
# ++++++++++++++++++++++++++++ setXlabel ++++++++++++++++++++++++++++++
    def setXlabel(self, Xlabel):
        self.Xlabel = Xlabel
# ++++++++++++++++++++++++++++ setYlabel ++++++++++++++++++++++++++++++
    def setYlabel(self, Ylabel):
        self.Ylabel = Ylabel

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Read Data Thread ~~~~~~~~~~~~~~~~~~~~~~~~~~
class ReadDataThread(QThread):
# +++++++++++++++++++++++++++++__init__ +++++++++++++++++++++++++++++++
    def __init__(self, path, delay, parent=None):
        super(ReadDataThread, self).__init__()
        self.path = path
        ################### Set delay time ############################
        try:
            self.delay = int(float(delay)*1000)
        except ValueError:
            self.delay = int(float(delay.replace(",", "."))*1000)
# +++++++++++++++++++++++++++++++ run +++++++++++++++++++++++++++++++++
    def run(self):
        while _Run:
        ###################### Read data ##############################
            self.datFileReading()
        #################### Simulate data ############################
            #self.simulateData()
            #QThread.msleep(self.delay)
# ++++++++++++++++++++++++ DAT file reading +++++++++++++++++++++++++++
    def datFileReading(self, outputFileName="path.datout.txt"):
        ################ get info about file ##########################
        statinfo = os.stat(self.path)
        outputFileName = self.path.split('.dat')[0] + '.datout.txt'

        ############## Create output text file ########################
        f = open(outputFileName, 'w')
        f.close()

        self.thr_scan_matrix = np.zeros((8, 64))  # Tiger, Channel

        ################ Read dat file data ###########################
        with open(self.path, 'rb') as f:
            for i in range(0, int(statinfo.st_size / 8)):
        ################## Thread breaker #############################
                if _Run == False:
                    break
        ##################### Read data ###############################
                data = f.read(8)
                hexdata = binascii.hexlify(data)
                string= "{:064b}".format(int(hexdata,16))
                raw_raw="{} \n".format(string)
                inverted=[]
                for i in range (8,0,-1):
                    inverted.append(string[(i-1)*8:i*8])
                string_inv="".join(inverted)
                int_x = int(string_inv,2)
                raw = "{:064b}  ".format(int_x)
        ###### Decoding raw data and create text format ###############
                if (((int_x & 0xFF00000000000000) >> 59) == 0x04):  # It's a frameword
                    s = 'TIGER: ' + '%01X ' % ((int_x >> 56) & 0x7) + 'HB: ' + 'Framecount: %08X ' % (
                            (int_x >> 15) & 0xFFFF) + 'SEUcount: %08X\n' % (int_x & 0x7FFF)

                if (((int_x & 0xFF00000000000000) >> 59) == 0x08):
                    s = 'TIGER: ' + '%01X ' % ((int_x >> 56) & 0x7) + 'CW: ' + 'ChID: %02X ' % (
                            (int_x >> 24) & 0x3F) + ' CounterWord: %016X\n' % (int_x & 0x00FFFFFF)

                if (((int_x & 0xFF00000000000000) >> 59) == 0x00):
                    s = 'TIGER: ' + '%01X ' % ((int_x >> 56) & 0x7) + 'EW: ' + 'ChID: %02X ' % (
                            (int_x >> 48) & 0x3F) + 'tacID: %01X ' % ((int_x >> 46) & 0x3) + 'Tcoarse: %04X ' % (
                                (int_x >> 30) & 0xFFFF) + 'Ecoarse: %03X ' % (
                                (int_x >> 20) & 0x3FF) + 'Tfine: %03X ' % ((int_x >> 10) & 0x3FF) + 'Efine: %03X \n' % (
                                int_x & 0x3FF)
                    self.thr_scan_matrix[(int_x >> 56) & 0x7, int(int_x >> 48) & 0x3F] = self.thr_scan_matrix[(int_x >> 56) & 0x7, int(int_x >> 48) & 0x3F] + 1
        ############ Decoding raw and separation ######################
                tigerId = ((int_x >> 56) & 0x7)
                ch = ((int_x >> 48) & 0x3F)
                tacId = ((int_x >> 46) & 0x3)
                tcoarse = ((int_x >> 30) & 0xFFFF)
                ecoarse = ((int_x >> 20) & 0x3FF)
                tfine = ((int_x >> 10) & 0x3FF)
                efine = (int_x & 0x3FF)
        ######### from 16bit Tcourse data take 10bit ##################
                #tcoarse = int(string_inv[24:][:10],2)
        ########## Correct reverse logic efine value ##################
                efine = 1023 - efine
        ######## Transfer parameters to global buffer #################
                if "TIGER:{}".format(tigerId) in DATA.keys():
                    DATA["TIGER:{}".format(tigerId)]['ch'].append(ch)
                    DATA["TIGER:{}".format(tigerId)]['tacId'].append(tacId)
                    DATA["TIGER:{}".format(tigerId)]['tcoarse'].append(tcoarse)
                    DATA["TIGER:{}".format(tigerId)]['ecoarse'].append(ecoarse)
                    DATA["TIGER:{}".format(tigerId)]['tfine'].append(tfine)
                    DATA["TIGER:{}".format(tigerId)]['efine'].append(efine)
                    DATA["TIGER:{}".format(tigerId)]['ToT'].append(abs(ecoarse-tcoarse))
                else:
                    DATA["TIGER:{}".format(tigerId)] = {'ch'      : [],
                                                        'tacId'   : [],
                                                        'tcoarse' : [],
                                                        'ecoarse' : [],
                                                        'tfine'   : [],
                                                        'efine'   : [],
                                                        'ToT'     : []}

                    DATA["TIGER:{}".format(tigerId)]['ch'].append(ch)
                    DATA["TIGER:{}".format(tigerId)]['tacId'].append(tacId)
                    DATA["TIGER:{}".format(tigerId)]['tcoarse'].append(tcoarse)
                    DATA["TIGER:{}".format(tigerId)]['ecoarse'].append(ecoarse)
                    DATA["TIGER:{}".format(tigerId)]['tfine'].append(tfine)
                    DATA["TIGER:{}".format(tigerId)]['efine'].append(efine)

                    DATA["TIGER:{}".format(tigerId)]['ToT'].append(abs(ecoarse-tcoarse))
        ############# Debugging of data reading #######################
                if debug:
                    print('******************')
                    print('TIGER: {}'.format(tigerId))
                    print('ChID: {}'.format(ch))
                    print('tacId: {}'.format(tacId))
                    print('Tcoarse: {}'.format(tcoarse))
                    print('Ecoarse: {}'.format(ecoarse))
                    print('Tfine: {}'.format(tfine))
                    print('Efine: {}'.format(efine))
        ############### Calculate current time ########################
                # Time= Framecount*204,8ns + Tcoarse*6,25ns
                if ((int_x >> 30) & 0xFFFF) < 2^15:
                    Time = ((int_x >> 15) & 0xFFFF) * 204800 + ((int_x >> 30) & 0xFFFF) * 6.25
                
                if ((int_x >> 30) & 0xFFFF) > 2^15:
                    Time= ((int_x >> 15) & 0xFFFF) * 204800 + (((int_x >> 30) & 0xFFFF)-2^15) * 6.25
        ############### Write data to log file ########################
                with open(outputFileName, 'a') as ff:
                    #ff.write("{}     {}".format(raw, s))
                    ff.write("{}".format(s))
        #################### Thread delay #############################
                QThread.msleep(self.delay)
# +++++++++++++++++++++++++++ Simulation ++++++++++++++++++++++++++++++
    def simulateData(self):
        ################ Generate random data #########################
        self.tigerId = random.randint(0,2)
        self.ch = random.randint(0,63)
        self.tacId = random.randint(0,3)
        self.tcoarse = random.randint(0,1023)
        self.ecoarse = random.randint(0,1023)
        self.tfine = random.randint(0,1023)
        self.efine = random.randint(0,1023)
        ######## Transfer parameters to global buffer #################
        if "TIGER:{}".format(self.tigerId) in DATA.keys():
            DATA["TIGER:{}".format(self.tigerId)]['ch'].append(self.ch)
            DATA["TIGER:{}".format(self.tigerId)]['tacId'].append(self.tacId)
            DATA["TIGER:{}".format(self.tigerId)]['tcoarse'].append(self.tcoarse)
            DATA["TIGER:{}".format(self.tigerId)]['ecoarse'].append(self.ecoarse)
            DATA["TIGER:{}".format(self.tigerId)]['tfine'].append(self.tfine)
            DATA["TIGER:{}".format(self.tigerId)]['efine'].append(self.efine)
            DATA["TIGER:{}".format(self.tigerId)]['ToT'].append(abs(self.ecoarse-self.tcoarse))
        else:
            DATA["TIGER:{}".format(self.tigerId)] = {'ch'      : [],
                                                     'tacId'   : [],
                                                     'tcoarse' : [],
                                                     'ecoarse' : [],
                                                     'tfine'   : [],
                                                     'efine'   : [],
                                                     'ToT'     : []}

            DATA["TIGER:{}".format(self.tigerId)]['ch'].append(self.ch)
            DATA["TIGER:{}".format(self.tigerId)]['tacId'].append(self.tacId)
            DATA["TIGER:{}".format(self.tigerId)]['tcoarse'].append(self.tcoarse)
            DATA["TIGER:{}".format(self.tigerId)]['ecoarse'].append(self.ecoarse)
            DATA["TIGER:{}".format(self.tigerId)]['tfine'].append(self.tfine)
            DATA["TIGER:{}".format(self.tigerId)]['efine'].append(self.efine)
            DATA["TIGER:{}".format(self.tigerId)]['ToT'].append(abs(self.ecoarse-self.tcoarse))
        ############# debugging of data reading #######################
        if debug:
            print('******************')
            print('TIGER: {}'.format(self.tigerId))
            print('ChID: {}'.format(self.ch))
            print('tacId: {}'.format(self.tacId))
            print('Tcoarse: {}'.format(self.tcoarse))
            print('Ecoarse: {}'.format(self.ecoarse))
            print('Tfine: {}'.format(self.tfine))
            print('Efine: {}'.format(self.efine))
# ++++++++++++++++++++++++ Set refresh time +++++++++++++++++++++++++++
    def setRefreshTime(self, delay):
        try:
            self.delay = int(float(delay)*1000)
        except ValueError:
            try:
                self.delay = int(float(delay.replace(",", "."))*1000)
            except ValueError:
                pass

# ~~~~~~~~~~~~~~~~~~~~~~~~ Monitoring Thread ~~~~~~~~~~~~~~~~~~~~~~~~~~
class MonitoringThread(QThread):
    change_value = pyqtSignal()
# +++++++++++++++++++++++++++++__init__ +++++++++++++++++++++++++++++++
    def __init__(self, delay, parent=None):
        super(MonitoringThread, self).__init__()
        try:
            self.delay = int(float(delay)*1000)
        except ValueError:
            self.delay = int(float(delay.replace(",", "."))*1000)
# +++++++++++++++++++++++++++++++ run +++++++++++++++++++++++++++++++++
    def run(self):
        while _Run:
            QThread.msleep(self.delay)
            self.change_value.emit()
# ++++++++++++++++++++++++ Set refresh time +++++++++++++++++++++++++++
    def setRefreshTime(self, delay):
        try:
            self.delay = int(float(delay)*1000)
        except ValueError:
            try:
                self.delay = int(float(delay.replace(",", "."))*1000)
            except ValueError:
                pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ App ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(QMainWindow):
# +++++++++++++++++++++++++++++__init__ +++++++++++++++++++++++++++++++
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('img/DAQ.svg'))
        self.setWindowTitle('DAQ')
        self.setGeometry(0, 0, 1500, 800)
        self.statuseMessage("")

        self.selectedPar = 'tcoarse'
        self.OpenfilePath = ''

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
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        ######################## open #################################
        openAct = QAction(QIcon('img/open.svg'),'Open files', self)
        openAct.setShortcut("Ctrl+O")
        openAct.triggered.connect(self.openFile)
        ######################## Play #################################
        PlayAct = QAction(QIcon('img/play.svg'),'Play', self)
        PlayAct.triggered.connect(self.start)
        ######################## Stop #################################
        StopAct = QAction(QIcon('img/stop.svg'), 'Stop', self)
        StopAct.triggered.connect(self.stop)
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

        viewWidgetsPage1_VLayout = QVBoxLayout()
        viewWidgetsPage2_GridLayout = QGridLayout()

        # "ToT" Time over Threshold
        self.HistPlot = PlotHistogram(title="Hist",Xlabel=self.selectedPar,Ylabel="Counts")
        viewWidgetsPage1_VLayout.addWidget(self.HistPlot)

        #HistPlot_toolbar = NavigationToolbar2QT(self.HistPlot, self)
        #viewWidgetsPage1_VLayout.addWidget(HistPlot_toolbar)
        self.viewWidgetsPage1.setLayout(viewWidgetsPage1_VLayout)


        self.TwoDHistPlot = Plot2DHistogram(title="2D hist",Xlabel="Channels",Ylabel=self.selectedPar)
        viewWidgetsPage1_VLayout.addWidget(self.TwoDHistPlot)

        TwoDHistPlot_toolbar = NavigationToolbar2QT(self.TwoDHistPlot, self)
        viewWidgetsPage1_VLayout.addWidget(TwoDHistPlot_toolbar)
        self.viewWidgetsPage1.setLayout(viewWidgetsPage1_VLayout)

        ##############################
        self.TwoDHistPlot1 = Plot2DHistogram(title="2D hist",Xlabel="Channels",Ylabel="Tcourse")
        self.TwoDHistPlot2 = Plot2DHistogram(title="2D hist",Xlabel="Channels",Ylabel="Ecoarse")
        self.TwoDHistPlot3 = Plot2DHistogram(title="2D hist",Xlabel="Channels",Ylabel="Tfine")
        self.TwoDHistPlot4 = Plot2DHistogram(title="2D hist",Xlabel="Channels",Ylabel="Efine")


        viewWidgetsPage2_GridLayout.addWidget(self.TwoDHistPlot1,0,0)
        viewWidgetsPage2_GridLayout.addWidget(self.TwoDHistPlot2,0,1)
        viewWidgetsPage2_GridLayout.addWidget(self.TwoDHistPlot3,1,0)
        viewWidgetsPage2_GridLayout.addWidget(self.TwoDHistPlot4,1,1)

        self.viewWidgetsPage2.setLayout(viewWidgetsPage2_GridLayout)
        ##############################

        self.tabs.addTab(self.viewWidgetsPage1, "All in one")
        self.tabs.addTab(self.viewWidgetsPage2, "Additional")
        self.setCentralWidget(self.tabs)

        viewWidgetsVlayout = QVBoxLayout()

        self.tabs.setLayout(viewWidgetsVlayout)
        self.controlDockWidget = QDockWidget('Monitoring')
        self.controlDockWidget.setWidget(self.tabs)
        self.addDockWidget(Qt.RightDockWidgetArea, self.controlDockWidget)
################# Set control widgets on dockedWidget #################
        self.controlWidgets = QWidget()
        controlWidgetsVlayout = QVBoxLayout()

        DAQ_setupGroupbox = QGroupBox("DAQ setup")

        DAQ_VLayout = QVBoxLayout()
        ################ Dat file path label ##########################
        datFilepathLabel = QLabel("Current DAT file path")
        ################ Current path field ###########################
        self.selectedPath = QLineEdit()
        self.selectedPath.setAlignment(Qt.AlignCenter)
        self.selectedPath.setReadOnly(True)
        self.selectedPath.setToolTip("<h5>Current path")
        ############### DAT file path Layout ##########################
        datFilepathVLayout = QVBoxLayout()
        datFilepathVLayout.addWidget(datFilepathLabel)
        datFilepathVLayout.addWidget(self.selectedPath)
        #################### Delay label ##############################
        delayLabel = QLabel("Delay [s]")
        #################### Delay Layout #############################
        delayHLayout = QHBoxLayout()
        ################# Refresh time field ##########################
        validator = QDoubleValidator()
        validator.setRange(1.0, 60.0, 1)
        self.delay = QLineEdit()
        self.delay.textChanged.connect(self.setRefreshTime)
        self.delay.setAlignment(Qt.AlignCenter)
        self.delay.setValidator(validator)
        self.delay.setText('5')
        ############## Parameter selector Layout ######################
        parameterSelectorHLayout = QHBoxLayout()
        #################### Delay label ##############################
        parameterSelectorLabel = QLabel("Parameter selector")
        ############ Set widgets on delay layouts #####################
        delayHLayout.addWidget(self.delay)
        delayHLayout.addWidget(delayLabel)
        ###############################################################
        # Create combobox and add items.
        self.parameterSelector = QComboBox()
        self.parameterSelector.addItems(['tcoarse','ecoarse','tfine','efine','ToT'])
        self.parameterSelector.currentIndexChanged.connect(self.chooseParameter)
        ####### Set widgets on parameter Selector layouts #############
        parameterSelectorHLayout.addWidget(self.parameterSelector)
        parameterSelectorHLayout.addWidget(parameterSelectorLabel)
        ###############################################################
        DAQ_VLayout.addLayout(datFilepathVLayout)
        DAQ_VLayout.addLayout(delayHLayout)
        DAQ_VLayout.addLayout(parameterSelectorHLayout)
        DAQ_setupGroupbox.setLayout(DAQ_VLayout)

        Trigger_setupGroupbox = QGroupBox("Triger setup")
        Trigger_setupGroupbox.setCheckable(True)
        Trigger_setupGroupbox.setChecked(False)

        controlWidgetsVlayout.addWidget(DAQ_setupGroupbox)
        controlWidgetsVlayout.addWidget(Trigger_setupGroupbox)

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
        path, _ = QFileDialog.getOpenFileName(self, 'Select DAT file', QDir.currentPath(), "DAT Files(*.dat)")
        if path != '':
            self.OpenfilePath = path
            self.selectedPath.setText(self.OpenfilePath)
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
# ++++++++++++++++++++++++ Status Messages ++++++++++++++++++++++++++++
    def statuseMessage(self, message):
        self.statusBar().showMessage(message)
# ++++++++++++++++++++++++++++++ Start ++++++++++++++++++++++++++++++++
    def start(self):
        global _Run
        if self.OpenfilePath != '':
            if _Run == False:
                _Run = True
        ############### Clear global data buffer ######################
                try:
                    DATA.clear()
                    self.statuseMessage("Stop")
                except AttributeError:
                    pass
        ################# Data reading thread #########################
                self.thread1 = ReadDataThread(path=self.OpenfilePath, delay="0.001")
        ################## Monitoring thread ##########################
                self.thread2 = MonitoringThread(self.delay.text())
                self.thread2.change_value.connect(self.presentData)
        #################### Start threads ############################
                self.thread1.start()
                self.thread2.start()

                self.statuseMessage("Running")
# ++++++++++++++++++++++++++++++ Stop +++++++++++++++++++++++++++++++++
    def stop(self):
        global _Run
        _Run = False
        self.statuseMessage("Stop")
# ++++++++++++++++++++++++ Set refresh time +++++++++++++++++++++++++++
    def setRefreshTime(self):
        try:
            self.thread2.setRefreshTime(self.delay.text())
        except AttributeError:
            pass
# ++++++++++++++++++++++++ Choose parameter +++++++++++++++++++++++++++
    def chooseParameter(self):
        self.selectedPar = self.parameterSelector.currentText()
        self.HistPlot.setXlabel(self.selectedPar)
        self.TwoDHistPlot.setYlabel(self.selectedPar)
# ++++++++++++++++++++++++++++ View data ++++++++++++++++++++++++++++++
    def presentData(self):
        ######### Check global buffer if contains data ################
        if len(DATA.keys()) != 0:
        ####### Get all TIGER ID keys from global buffer ##############
            keys = []
            for key in sorted(DATA.keys()):
                keys.append(key)
        ##### Take selected parameter from global buffer ##############
            try:
                X = DATA[keys[0]]['ch']
                Y = DATA[keys[0]][self.selectedPar]
        ############## Take first TIGER parameters ####################
                tcoarse = copy.copy(DATA[keys[0]]['tcoarse'])
                ecoarse = copy.copy(DATA[keys[0]]['ecoarse'])
                tfine = copy.copy(DATA[keys[0]]['tfine'])
                efine = copy.copy(DATA[keys[0]]['efine'])

                channels = 63
                i = 1
        ########### Concatenate all TIGERs parameters #################
                for key in keys[1:]:
                    X += [x + channels*i for x in DATA[key]['ch']]
                    Y += DATA[key][self.selectedPar]
                    
                    tcoarse += DATA[key]['tcoarse']
                    ecoarse += DATA[key]['ecoarse']
                    tfine += DATA[key]['tfine']
                    efine += DATA[key]['efine']
                    i +=1
        ################# Update active page ##########################
                ############### Page 1 ################################
                if self.tabs.currentIndex() == 0:
                    self.HistPlot.updateHist(Y)
                    self.TwoDHistPlot.update2dHist([X,Y])
                ############### Page 2 ################################
                elif self.tabs.currentIndex() == 1:
                    x = copy.copy(X)
                    self.TwoDHistPlot1.update2dHist([x, tcoarse])
                    self.TwoDHistPlot2.update2dHist([x, ecoarse])
                    self.TwoDHistPlot3.update2dHist([x, tfine])
                    self.TwoDHistPlot4.update2dHist([x, efine])
            except IndexError:
                pass
        ############### Clear global data buffer ######################
            DATA.clear()
# +++++++++++++++++++++++++++ Test button +++++++++++++++++++++++++++++
    def test(self):
        print("test")

#######################################################################
#######################################################################
if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    ex = App()
    app.exec_()