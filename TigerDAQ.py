from re import T
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QMessageBox, QAction, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QGridLayout,
                             QGroupBox, QLineEdit, QLabel, QComboBox,
                             QCheckBox, QRadioButton)
from PyQt5.QtGui import QIcon, QPalette, QColor, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal, QTimer
import pyqtgraph as pg
import numpy as np
import binascii
import socket
import os

mapping = { 'Chip1_Ch0' : 111,
            'Chip1_Ch1' : 61,
            'Chip1_Ch2' : 109,
            'Chip1_Ch3' : 37,
            'Chip1_Ch4' : 67,
            'Chip1_Ch5' : 31,
            'Chip1_Ch6' : 65,
            'Chip1_Ch7' : 36,
            'Chip1_Ch8' : 72,
            'Chip1_Ch9' : 33,
            'Chip1_Ch10': 69,
            'Chip1_Ch11': 49,
            'Chip1_Ch12': 66,
            'Chip1_Ch13': 35,
            'Chip1_Ch14': 117,
            'Chip1_Ch15': 57,
            'Chip1_Ch16': 113,
            'Chip1_Ch17': 47,
            'Chip1_Ch18': 114,
            'Chip1_Ch19': 56,
            'Chip1_Ch20': 106,
            'Chip1_Ch21': 71,
            'Chip1_Ch22': 108,
            'Chip1_Ch23': 68,
            'Chip1_Ch24': 107,
            'Chip1_Ch25': 53,
            'Chip1_Ch26': 104,
            'Chip1_Ch27': 51,
            'Chip1_Ch28': 105,
            'Chip1_Ch29': 60,
            'Chip1_Ch30': 116,
            'Chip1_Ch31': 59,
            'Chip1_Ch32': 38,
            'Chip1_Ch33': 64,
            'Chip1_Ch34': 39,
            'Chip1_Ch35': 62,
            'Chip1_Ch36': 112,
            'Chip1_Ch37': 48,
            'Chip1_Ch38': 115,
            'Chip1_Ch39': 55,
            'Chip1_Ch40': 120,
            'Chip1_Ch41': 63,
            'Chip1_Ch42': 32,
            'Chip1_Ch43': 43,
            'Chip1_Ch44': 41,
            'Chip1_Ch45': 123,
            'Chip1_Ch46': 40,
            'Chip1_Ch47': 70,
            'Chip1_Ch48': 110,
            'Chip1_Ch49': 34,
            'Chip1_Ch50': 122,
            'Chip1_Ch51': 50,
            'Chip1_Ch52': 121,
            'Chip1_Ch53': 46,
            'Chip1_Ch54': 45,
            'Chip1_Ch55': 54,
            'Chip1_Ch56': 42,
            'Chip1_Ch57': 124,
            'Chip1_Ch58': 34,
            'Chip1_Ch59': 44,
            'Chip1_Ch60': 52,
            'Chip1_Ch61': 119,

            'Chip2_Ch0' : 83,
            'Chip2_Ch1' : 14,
            'Chip2_Ch2' : 21,
            'Chip2_Ch3' : 73,
            'Chip2_Ch4' : 76,
            'Chip2_Ch5' : 26,
            'Chip2_Ch6' : 9,
            'Chip2_Ch7' : 13,
            'Chip2_Ch8' : 24,
            'Chip2_Ch9' : 10,
            'Chip2_Ch10': 25,
            'Chip2_Ch11': 74,
            'Chip2_Ch12': 77,
            'Chip2_Ch13': 16,
            'Chip2_Ch14': 81,
            'Chip2_Ch15': 80,
            'Chip2_Ch16': 89,
            'Chip2_Ch17': 22,
            'Chip2_Ch18': 28,
            'Chip2_Ch19': 79,
            'Chip2_Ch20': 88,
            'Chip2_Ch21': 23,
            'Chip2_Ch22': 75,
            'Chip2_Ch23': 78,
            'Chip2_Ch24': 27,
            'Chip2_Ch25': 11,
            'Chip2_Ch26': 84,
            'Chip2_Ch27': 15,
            'Chip2_Ch28': 90,
            'Chip2_Ch29': 12,
            'Chip2_Ch30': 29,
            'Chip2_Ch31': 17,
            'Chip2_Ch32': 30,
            'Chip2_Ch33': 6,
            'Chip2_Ch34': 102,
            'Chip2_Ch35': 18,
            'Chip2_Ch36': 101,
            'Chip2_Ch37': 8,
            'Chip2_Ch38': 103,
            'Chip2_Ch39': 7,
            'Chip2_Ch40': 97,
            'Chip2_Ch41': 4,
            'Chip2_Ch42': 100,
            'Chip2_Ch43': 5,
            'Chip2_Ch44': 99,
            'Chip2_Ch45': 1,
            'Chip2_Ch46': 96,
            'Chip2_Ch47': 2,
            'Chip2_Ch48': 98,
            'Chip2_Ch49': 85,
            'Chip2_Ch50': 93,
            'Chip2_Ch51': 87,
            'Chip2_Ch52': 94,
            'Chip2_Ch53': 20,
            'Chip2_Ch54': 3,
            'Chip2_Ch55': 86,
            'Chip2_Ch56': 92,
            'Chip2_Ch57': 19,
            'Chip2_Ch58': 95,
            'Chip2_Ch59': 91,
            'Chip2_Ch60': 82,
            'Chip2_Ch61': 118,

            'Chip3_Ch0' : 111,
            'Chip3_Ch1' : 61,
            'Chip3_Ch2' : 109,
            'Chip3_Ch3' : 37,
            'Chip3_Ch4' : 67,
            'Chip3_Ch5' : 31,
            'Chip3_Ch6' : 65,
            'Chip3_Ch7' : 36,
            'Chip3_Ch8' : 72,
            'Chip3_Ch9' : 33,
            'Chip3_Ch10': 69,
            'Chip3_Ch11': 49,
            'Chip3_Ch12': 66,
            'Chip3_Ch13': 35,
            'Chip3_Ch14': 117,
            'Chip3_Ch15': 57,
            'Chip3_Ch16': 113,
            'Chip3_Ch17': 47,
            'Chip3_Ch18': 114,
            'Chip3_Ch19': 56,
            'Chip3_Ch20': 106,
            'Chip3_Ch21': 71,
            'Chip3_Ch22': 108,
            'Chip3_Ch23': 68,
            'Chip3_Ch24': 107,
            'Chip3_Ch25': 53,
            'Chip3_Ch26': 104,
            'Chip3_Ch27': 51,
            'Chip3_Ch28': 105,
            'Chip3_Ch29': 60,
            'Chip3_Ch30': 116,
            'Chip3_Ch31': 59,
            'Chip3_Ch32': 38,
            'Chip3_Ch33': 64,
            'Chip3_Ch34': 39,
            'Chip3_Ch35': 62,
            'Chip3_Ch36': 112,
            'Chip3_Ch37': 48,
            'Chip3_Ch38': 115,
            'Chip3_Ch39': 55,
            'Chip3_Ch40': 120,
            'Chip3_Ch41': 63,
            'Chip3_Ch42': 32,
            'Chip3_Ch43': 43,
            'Chip3_Ch44': 41,
            'Chip3_Ch45': 123,
            'Chip3_Ch46': 40,
            'Chip3_Ch47': 70,
            'Chip3_Ch48': 110,
            'Chip3_Ch49': 34,
            'Chip3_Ch50': 122,
            'Chip3_Ch51': 50,
            'Chip3_Ch52': 121,
            'Chip3_Ch53': 46,
            'Chip3_Ch54': 45,
            'Chip3_Ch55': 54,
            'Chip3_Ch56': 42,
            'Chip3_Ch57': 124,
            'Chip3_Ch58': 34,
            'Chip3_Ch59': 44,
            'Chip3_Ch60': 52,
            'Chip3_Ch61': 119,

            'Chip4_Ch0' : 83,
            'Chip4_Ch1' : 14,
            'Chip4_Ch2' : 21,
            'Chip4_Ch3' : 73,
            'Chip4_Ch4' : 76,
            'Chip4_Ch5' : 26,
            'Chip4_Ch6' : 9,
            'Chip4_Ch7' : 13,
            'Chip4_Ch8' : 24,
            'Chip4_Ch9' : 10,
            'Chip4_Ch10': 25,
            'Chip4_Ch11': 74,
            'Chip4_Ch12': 77,
            'Chip4_Ch13': 16,
            'Chip4_Ch14': 81,
            'Chip4_Ch15': 80,
            'Chip4_Ch16': 89,
            'Chip4_Ch17': 22,
            'Chip4_Ch18': 28,
            'Chip4_Ch19': 79,
            'Chip4_Ch20': 88,
            'Chip4_Ch21': 23,
            'Chip4_Ch22': 75,
            'Chip4_Ch23': 78,
            'Chip4_Ch24': 27,
            'Chip4_Ch25': 11,
            'Chip4_Ch26': 84,
            'Chip4_Ch27': 15,
            'Chip4_Ch28': 90,
            'Chip4_Ch29': 12,
            'Chip4_Ch30': 29,
            'Chip4_Ch31': 17,
            'Chip4_Ch32': 30,
            'Chip4_Ch33': 6,
            'Chip4_Ch34': 102,
            'Chip4_Ch35': 18,
            'Chip4_Ch36': 101,
            'Chip4_Ch37': 8,
            'Chip4_Ch38': 103,
            'Chip4_Ch39': 7,
            'Chip4_Ch40': 97,
            'Chip4_Ch41': 4,
            'Chip4_Ch42': 100,
            'Chip4_Ch43': 5,
            'Chip4_Ch44': 99,
            'Chip4_Ch45': 1,
            'Chip4_Ch46': 96,
            'Chip4_Ch47': 2,
            'Chip4_Ch48': 98,
            'Chip4_Ch49': 85,
            'Chip4_Ch50': 93,
            'Chip4_Ch51': 87,
            'Chip4_Ch52': 94,
            'Chip4_Ch53': 20,
            'Chip4_Ch54': 3,
            'Chip4_Ch55': 86,
            'Chip4_Ch56': 92,
            'Chip4_Ch57': 19,
            'Chip4_Ch58': 95,
            'Chip4_Ch59': 91,
            'Chip4_Ch60': 82,
            'Chip4_Ch61': 118,

            'Chip5_Ch0' : 111,
            'Chip5_Ch1' : 61,
            'Chip5_Ch2' : 109,
            'Chip5_Ch3' : 37,
            'Chip5_Ch4' : 67,
            'Chip5_Ch5' : 31,
            'Chip5_Ch6' : 65,
            'Chip5_Ch7' : 36,
            'Chip5_Ch8' : 72,
            'Chip5_Ch9' : 33,
            'Chip5_Ch10': 69,
            'Chip5_Ch11': 49,
            'Chip5_Ch12': 66,
            'Chip5_Ch13': 35,
            'Chip5_Ch14': 117,
            'Chip5_Ch15': 57,
            'Chip5_Ch16': 113,
            'Chip5_Ch17': 47,
            'Chip5_Ch18': 114,
            'Chip5_Ch19': 56,
            'Chip5_Ch20': 106,
            'Chip5_Ch21': 71,
            'Chip5_Ch22': 108,
            'Chip5_Ch23': 68,
            'Chip5_Ch24': 107,
            'Chip5_Ch25': 53,
            'Chip5_Ch26': 104,
            'Chip5_Ch27': 51,
            'Chip5_Ch28': 105,
            'Chip5_Ch29': 60,
            'Chip5_Ch30': 116,
            'Chip5_Ch31': 59,
            'Chip5_Ch32': 38,
            'Chip5_Ch33': 64,
            'Chip5_Ch34': 39,
            'Chip5_Ch35': 62,
            'Chip5_Ch36': 112,
            'Chip5_Ch37': 48,
            'Chip5_Ch38': 115,
            'Chip5_Ch39': 55,
            'Chip5_Ch40': 120,
            'Chip5_Ch41': 63,
            'Chip5_Ch42': 32,
            'Chip5_Ch43': 43,
            'Chip5_Ch44': 41,
            'Chip5_Ch45': 123,
            'Chip5_Ch46': 40,
            'Chip5_Ch47': 70,
            'Chip5_Ch48': 110,
            'Chip5_Ch49': 34,
            'Chip5_Ch50': 122,
            'Chip5_Ch51': 50,
            'Chip5_Ch52': 121,
            'Chip5_Ch53': 46,
            'Chip5_Ch54': 45,
            'Chip5_Ch55': 54,
            'Chip5_Ch56': 42,
            'Chip5_Ch57': 124,
            'Chip5_Ch58': 34,
            'Chip5_Ch59': 44,
            'Chip5_Ch60': 52,
            'Chip5_Ch61': 119,

            'Chip6_Ch0' : 83,
            'Chip6_Ch1' : 14,
            'Chip6_Ch2' : 21,
            'Chip6_Ch3' : 73,
            'Chip6_Ch4' : 76,
            'Chip6_Ch5' : 26,
            'Chip6_Ch6' : 9,
            'Chip6_Ch7' : 13,
            'Chip6_Ch8' : 24,
            'Chip6_Ch9' : 10,
            'Chip6_Ch10': 25,
            'Chip6_Ch11': 74,
            'Chip6_Ch12': 77,
            'Chip6_Ch13': 16,
            'Chip6_Ch14': 81,
            'Chip6_Ch15': 80,
            'Chip6_Ch16': 89,
            'Chip6_Ch17': 22,
            'Chip6_Ch18': 28,
            'Chip6_Ch19': 79,
            'Chip6_Ch20': 88,
            'Chip6_Ch21': 23,
            'Chip6_Ch22': 75,
            'Chip6_Ch23': 78,
            'Chip6_Ch24': 27,
            'Chip6_Ch25': 11,
            'Chip6_Ch26': 84,
            'Chip6_Ch27': 15,
            'Chip6_Ch28': 90,
            'Chip6_Ch29': 12,
            'Chip6_Ch30': 29,
            'Chip6_Ch31': 17,
            'Chip6_Ch32': 30,
            'Chip6_Ch33': 6,
            'Chip6_Ch34': 102,
            'Chip6_Ch35': 18,
            'Chip6_Ch36': 101,
            'Chip6_Ch37': 8,
            'Chip6_Ch38': 103,
            'Chip6_Ch39': 7,
            'Chip6_Ch40': 97,
            'Chip6_Ch41': 4,
            'Chip6_Ch42': 100,
            'Chip6_Ch43': 5,
            'Chip6_Ch44': 99,
            'Chip6_Ch45': 1,
            'Chip6_Ch46': 96,
            'Chip6_Ch47': 2,
            'Chip6_Ch48': 98,
            'Chip6_Ch49': 85,
            'Chip6_Ch50': 93,
            'Chip6_Ch51': 87,
            'Chip6_Ch52': 94,
            'Chip6_Ch53': 20,
            'Chip6_Ch54': 3,
            'Chip6_Ch55': 86,
            'Chip6_Ch56': 92,
            'Chip6_Ch57': 19,
            'Chip6_Ch58': 95,
            'Chip6_Ch59': 91,
            'Chip6_Ch60': 82,
            'Chip6_Ch61': 118,

            'Chip7_Ch0' : 111,
            'Chip7_Ch1' : 61,
            'Chip7_Ch2' : 109,
            'Chip7_Ch3' : 37,
            'Chip7_Ch4' : 67,
            'Chip7_Ch5' : 31,
            'Chip7_Ch6' : 65,
            'Chip7_Ch7' : 36,
            'Chip7_Ch8' : 72,
            'Chip7_Ch9' : 33,
            'Chip7_Ch10': 69,
            'Chip7_Ch11': 49,
            'Chip7_Ch12': 66,
            'Chip7_Ch13': 35,
            'Chip7_Ch14': 117,
            'Chip7_Ch15': 57,
            'Chip7_Ch16': 113,
            'Chip7_Ch17': 47,
            'Chip7_Ch18': 114,
            'Chip7_Ch19': 56,
            'Chip7_Ch20': 106,
            'Chip7_Ch21': 71,
            'Chip7_Ch22': 108,
            'Chip7_Ch23': 68,
            'Chip7_Ch24': 107,
            'Chip7_Ch25': 53,
            'Chip7_Ch26': 104,
            'Chip7_Ch27': 51,
            'Chip7_Ch28': 105,
            'Chip7_Ch29': 60,
            'Chip7_Ch30': 116,
            'Chip7_Ch31': 59,
            'Chip7_Ch32': 38,
            'Chip7_Ch33': 64,
            'Chip7_Ch34': 39,
            'Chip7_Ch35': 62,
            'Chip7_Ch36': 112,
            'Chip7_Ch37': 48,
            'Chip7_Ch38': 115,
            'Chip7_Ch39': 55,
            'Chip7_Ch40': 120,
            'Chip7_Ch41': 63,
            'Chip7_Ch42': 32,
            'Chip7_Ch43': 43,
            'Chip7_Ch44': 41,
            'Chip7_Ch45': 123,
            'Chip7_Ch46': 40,
            'Chip7_Ch47': 70,
            'Chip7_Ch48': 110,
            'Chip7_Ch49': 34,
            'Chip7_Ch50': 122,
            'Chip7_Ch51': 50,
            'Chip7_Ch52': 121,
            'Chip7_Ch53': 46,
            'Chip7_Ch54': 45,
            'Chip7_Ch55': 54,
            'Chip7_Ch56': 42,
            'Chip7_Ch57': 124,
            'Chip7_Ch58': 34,
            'Chip7_Ch59': 44,
            'Chip7_Ch60': 52,
            'Chip7_Ch61': 119,
            
            'Chip8_Ch0' : 83,
            'Chip8_Ch1' : 14,
            'Chip8_Ch2' : 21,
            'Chip8_Ch3' : 73,
            'Chip8_Ch4' : 76,
            'Chip8_Ch5' : 26,
            'Chip8_Ch6' : 9,
            'Chip8_Ch7' : 13,
            'Chip8_Ch8' : 24,
            'Chip8_Ch9' : 10,
            'Chip8_Ch10': 25,
            'Chip8_Ch11': 74,
            'Chip8_Ch12': 77,
            'Chip8_Ch13': 16,
            'Chip8_Ch14': 81,
            'Chip8_Ch15': 80,
            'Chip8_Ch16': 89,
            'Chip8_Ch17': 22,
            'Chip8_Ch18': 28,
            'Chip8_Ch19': 79,
            'Chip8_Ch20': 88,
            'Chip8_Ch21': 23,
            'Chip8_Ch22': 75,
            'Chip8_Ch23': 78,
            'Chip8_Ch24': 27,
            'Chip8_Ch25': 11,
            'Chip8_Ch26': 84,
            'Chip8_Ch27': 15,
            'Chip8_Ch28': 90,
            'Chip8_Ch29': 12,
            'Chip8_Ch30': 29,
            'Chip8_Ch31': 17,
            'Chip8_Ch32': 30,
            'Chip8_Ch33': 6,
            'Chip8_Ch34': 102,
            'Chip8_Ch35': 18,
            'Chip8_Ch36': 101,
            'Chip8_Ch37': 8,
            'Chip8_Ch38': 103,
            'Chip8_Ch39': 7,
            'Chip8_Ch40': 97,
            'Chip8_Ch41': 4,
            'Chip8_Ch42': 100,
            'Chip8_Ch43': 5,
            'Chip8_Ch44': 99,
            'Chip8_Ch45': 1,
            'Chip8_Ch46': 96,
            'Chip8_Ch47': 2,
            'Chip8_Ch48': 98,
            'Chip8_Ch49': 85,
            'Chip8_Ch50': 93,
            'Chip8_Ch51': 87,
            'Chip8_Ch52': 94,
            'Chip8_Ch53': 20,
            'Chip8_Ch54': 3,
            'Chip8_Ch55': 86,
            'Chip8_Ch56': 92,
            'Chip8_Ch57': 19,
            'Chip8_Ch58': 95,
            'Chip8_Ch59': 91,
            'Chip8_Ch60': 82,
            'Chip8_Ch61': 118
        }

# Global data buffer
DATA = {}
# thread controll
_Run = False
# Control debugging
debug = False

# ~~~~~~~~~~~~~~~~~~~~~~~~ Plot 2D Histogram ~~~~~~~~~~~~~~~~~~~~~~~~~~
class Plot2DHistogram(QWidget):
# +++++++++++++++++++++++++++++ __init__ ++++++++++++++++++++++++++++++
    def __init__(self, Xlabel='X', Ylabel='Y', Title='Title', Xcolor='#0000ff', Ycolor='#00ff00', parent=None):
        super(Plot2DHistogram, self).__init__(parent)
        self.Xlabel = Xlabel
        self.Ylabel = Ylabel
        self.Title = Title
        self.Xcolor = Xcolor
        self.Ycolor = Ycolor
        self.initUI()
# ++++++++++++++++++++++++++++++ initUI +++++++++++++++++++++++++++++++
    def initUI(self):
        #################### Window layout ############################
        windowHLayout = QHBoxLayout()
        ##################### Create plot #############################
        self.canvas = pg.GraphicsLayoutWidget()

        self.img = pg.ImageItem()

        self.plot = self.canvas.addPlot(title=self.Title)
        self.plot.addItem(self.img)
        self.plot.setLabel("bottom", self.Xlabel, color=self.Xcolor)
        self.plot.setLabel("left", self.Ylabel, color=self.Ycolor)

        self.histogram = pg.HistogramLUTItem()
        self.histogram.setLevels(0, 50)
        self.canvas.addItem(self.histogram)
        self.histogram.gradient.loadPreset("viridis")
        #self.histogram.gradient.loadPreset("flame")
        self.histogram.setImageItem(self.img)
        ############# Graph characteristics setup #####################
        self.plot.setMenuEnabled(False)
        self.plot.setAutoVisible(y=True)
        self.plot.setDownsampling(mode='peak')
        ############ Set plot widget on main window ###################
        windowHLayout.addWidget(self.canvas)
        self.setLayout(windowHLayout)
# ++++++++++++++++++++++++++++ updateHist +++++++++++++++++++++++++++++
    def update2dHist(self, data):
        try:
            xmin = min(data[0])
            xmax = max(data[0])

            ymin = min(data[1])
            ymax = max(data[1])

            xbins = 125
            ybins = ymax

            H = np.histogram2d(data[0], data[1], bins=(xbins, ybins), range=[[0, xbins], [0, ymax]])

            self.img.setImage(H[0], autoLevels=False, autoRange=True)
            self.plot.setLimits(xMin=1, xMax=xbins, yMin=0, yMax=ymax)
        except ValueError:
            pass
# ++++++++++++++++++++++++++++ setXlabel ++++++++++++++++++++++++++++++
    def setXlabel(self, Xlabel):
        self.Xlabel = Xlabel
        self.plot.setLabel("bottom", self.Xlabel)
# ++++++++++++++++++++++++++++ setYlabel ++++++++++++++++++++++++++++++
    def setYlabel(self, Ylabel):
        self.Ylabel = Ylabel
        self.plot.setLabel("left", self.Ylabel)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ Plot Histogram ~~~~~~~~~~~~~~~~~~~~~~~~~~~
class PlotHistogram(QWidget):
# +++++++++++++++++++++++++++++ __init__ ++++++++++++++++++++++++++++++
    def __init__(self, Xlabel='X', Ylabel='Y', Title='Title', Xcolor='#0000ff', Ycolor='#ff0000', barColor='#ff0000', parent=None):
        super(PlotHistogram, self).__init__(parent)
        self.Xlabel = Xlabel
        self.Ylabel = Ylabel
        self.Title = Title
        self.Xcolor = Xcolor
        self.Ycolor = Ycolor
        self.barColor = barColor
        self.initUI()
# ++++++++++++++++++++++++++++++ initUI +++++++++++++++++++++++++++++++
    def initUI(self):
        #################### Window layout ############################
        windowVLayout = QVBoxLayout()
        ##################### Create plot #############################
        self.canvas = pg.GraphicsLayoutWidget()

        self.statistics_text = pg.LabelItem(justify='right')
        text = f"<span style='font-size: {8}pt'>Entries: --- <br> Min: --- <br> Max: --- <br> Mean: --- <br> Sd: --- <br>"
        self.statistics_text.setText(text)
        self.canvas.addItem(self.statistics_text)

        self.plot = self.canvas.addPlot(title=self.Title, row=0, col=0)

        self.bg = pg.BarGraphItem(x=[], height=[], width=0.6, brush=self.barColor)
        self.plot.addItem(self.bg)
        ###################### Axis setup #############################
        self.plot.setLabel("bottom", self.Xlabel, color=self.Xcolor)
        self.plot.setLabel("left", self.Ylabel, color=self.Ycolor)
        ############# Graph characteristics setup #####################
        self.plot.setMenuEnabled(False)
        self.plot.setAutoVisible(y=True)
        self.plot.setDownsampling(mode='peak')
        self.plot.showGrid(x=True, y=True)
        ############ Set plot widget on main window ###################
        windowVLayout.addWidget(self.canvas)
        self.setLayout(windowVLayout)
# ++++++++++++++++++++++++++++ updateHist +++++++++++++++++++++++++++++
    def updateHist(self, X, Y):
        self.bg.setOpts(x=X, height=Y)
        data = np.asarray(X)
        try:
            Data_Entries = sum(Y)
            Data_min = round(np.min(data),2)
            Data_max = round(np.max(data),2)
            Data_mean = round(np.mean(data),2)
            Data_std = round(np.std(data),2)
            text = f"<span style='font-size: {8}pt'>Entries: {Data_Entries} <br> Min: {Data_min} <br> Max: {Data_max} <br> Mean: {Data_mean} <br> Sd: {Data_std} <br>"
            self.statistics_text.setText(text)
        except ValueError:
            pass
# ++++++++++++++++++++++++++++ setXlabel ++++++++++++++++++++++++++++++
    def setXlabel(self, Xlabel):
        self.Xlabel = Xlabel
        self.plot.setLabel("bottom", self.Xlabel)
# ++++++++++++++++++++++++++++ setYlabel ++++++++++++++++++++++++++++++
    def setYlabel(self, Ylabel):
        self.Ylabel = Ylabel
        self.plot.setLabel("left", self.Ylabel)

# ~~~~~~~~~~~~~~~~~~~~~~~~~ Read Data Thread ~~~~~~~~~~~~~~~~~~~~~~~~~~
class ReadDataThread(QThread):
# +++++++++++++++++++++++++++++__init__ +++++++++++++++++++++++++++++++
    def __init__(self, GEMROC_id, IP, Port, BUFSIZE, delay, mode, exportdata=False, parent = None):
        QThread.__init__(self, parent)
        self.IP = IP
        self.Port = Port
        self.delay = delay
        self.mode = mode
        self.BUFSIZE = BUFSIZE
        self.exportdata = exportdata
        self.GEMROC_id = GEMROC_id
# +++++++++++++++++++++++++++++++ Run +++++++++++++++++++++++++++++++++
    def run(self):
        if self.exportdata:
            file = open('./data/test.dat', "w")
            file.close()

        try:
            timeout_for_sockets = None
            serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serverSock.settimeout(timeout_for_sockets)
            serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serverSock.bind((self.IP, self.Port))
        except Exception as e:
            print( "--GEMROC {}-{}".format(self.GEMROC_id, e))
            print( "Can't bind the socket")

        while _Run:
            data_pack, addr = serverSock.recvfrom(self.BUFSIZE)

            if self.exportdata:
                file = open('./data/test.dat', "ab")
                file.write(data_pack)

            for slices in range(0,len(data_pack)//8):
                data=data_pack[slices*8:slices*8+8]

                hexdata = binascii.hexlify(data)
                string= "{:064b}".format(int(hexdata,16))
                inverted=[]
                for i in range (8,0,-1):
                    inverted.append(string[(i-1)*8:i*8])
                string_inv="".join(inverted)
                int_x = int(string_inv,2)

                if (((int_x & 0xFF00000000000000) >> 59) == 0x00):
                    try:
                        tigerId = ((int_x >> 56) & 0x7)
                        ch = ((int_x >> 48) & 0x3F)
                        strip = mapping['Chip{}_Ch{}'.format(tigerId+1, ch)]
                        tacId = ((int_x >> 46) & 0x3)
                        tcoarse = ((int_x >> 30) & 0xFFFF)
                        ecoarse = ((int_x >> 20) & 0x3FF)
                        tfine = ((int_x >> 10) & 0x3FF)
                        efine = (int_x & 0x3FF)
                ########## Correct reverse logic efine value ##################
                        efine = 1023 - efine
                ######## Transfer parameters to global buffer #################

                        if "TIGER:{}".format(tigerId) in DATA.keys():
                            DATA["TIGER:{}".format(tigerId)]['strip'].append(strip)
                            DATA["TIGER:{}".format(tigerId)]['tacId'].append(tacId)
                            DATA["TIGER:{}".format(tigerId)]['tcoarse'].append(tcoarse)
                            DATA["TIGER:{}".format(tigerId)]['ecoarse'].append(ecoarse)
                            DATA["TIGER:{}".format(tigerId)]['tfine'].append(tfine)
                            DATA["TIGER:{}".format(tigerId)]['efine'].append(efine)
                        else:
                            DATA["TIGER:{}".format(tigerId)] = {'strip'   : [],
                                                                'tacId'   : [],
                                                                'tcoarse' : [],
                                                                'ecoarse' : [],
                                                                'tfine'   : [],
                                                                'efine'   : []
                                                                }

                            DATA["TIGER:{}".format(tigerId)]['strip'].append(strip)
                            DATA["TIGER:{}".format(tigerId)]['tacId'].append(tacId)
                            DATA["TIGER:{}".format(tigerId)]['tcoarse'].append(tcoarse)
                            DATA["TIGER:{}".format(tigerId)]['ecoarse'].append(ecoarse)
                            DATA["TIGER:{}".format(tigerId)]['tfine'].append(tfine)
                            DATA["TIGER:{}".format(tigerId)]['efine'].append(efine)
                ############# Debugging of data reading #######################
                        if debug:
                            print('******************')
                            print('TIGER: {}'.format(tigerId))
                            print('Strip: {}'.format(strip))
                            print('tacId: {}'.format(tacId))
                            print('Tcoarse: {}'.format(tcoarse))
                            print('Ecoarse: {}'.format(ecoarse))
                            print('Tfine: {}'.format(tfine))
                            print('Efine: {}'.format(efine))
                    except KeyError:
                        pass
        if self.exportdata:
            file.close()
        self.wait()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ App ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class App(QMainWindow):
# +++++++++++++++++++++++++++++__init__ +++++++++++++++++++++++++++++++
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('img/DAQ.svg'))
        self.setWindowTitle('DAQ_online')
        self.setGeometry(0, 0, 1500, 800)
        self.statuseMessage("")

        self.selectedPar = 'efine'
        self.selectedTiger = 'TIGER(0-1)'
        self.OpenfilePath = ''
        self.parameters = ['tcoarse','ecoarse','tfine','efine']

        self.modeSelector = 'TL'

        self.IPaddress = '127.0.0.1'
        self.GEMROC_id = 0
        self.Port = 58880 + self.GEMROC_id
        self.BUFSIZE = 32000
        
        self.selectedstrip_From = 1
        self.selectedstrip_To = 124

        self.delayMiliseconds = 1000

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.presentData)

        self.barData = np.zeros(125, dtype=int)

        pg.setConfigOptions(antialias=True)

        self.exportDataSatate = False

        self.initUI()
# +++++++++++++++++++++++++++++ initUI ++++++++++++++++++++++++++++++++
    def initUI(self):
        self.darkTheme()
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
####################### Add buttons on toolbar ########################
        toolbar = self.addToolBar('Tools')
        toolbar.addAction(exitButton)
        toolbar.addSeparator()
        toolbar.addAction(PlayAct)
        toolbar.addAction(StopAct)
        toolbar.addSeparator()
        toolbar.addAction(aboutButton)
########################## Set view widgets ###########################
        MainWidget = QWidget()
        MainHLayout = QHBoxLayout()
        ##################### Create tabs #############################
        self.tabs = QTabWidget()

        self.viewWidgetsPage1 = QWidget()
        self.viewWidgetsPage2 = QWidget()

        viewWidgetsPage1_VLayout = QVBoxLayout()
        viewWidgetsPage1_HLayout = QHBoxLayout()
        viewWidgetsPage2_GridLayout = QGridLayout()

        self.HistPlot = PlotHistogram(Xlabel="Strips", Ylabel="Counts", Title="Hist", Xcolor='#0000ff', Ycolor='#ff0000', barColor='#ff0000')
        viewWidgetsPage1_VLayout.addWidget(self.HistPlot)

        self.HistPlot2 = PlotHistogram(Xlabel=self.selectedPar, Ylabel="Counts", Title="Hist", Xcolor='#00ff00', Ycolor='#ff0000', barColor='#0000ff')
        viewWidgetsPage1_HLayout.addWidget(self.HistPlot2)

        self.TwoDHistPlot = Plot2DHistogram(Xlabel="Strips", Ylabel=self.selectedPar, Title="2D hist", Xcolor='#0000ff', Ycolor='#00ff00')
        viewWidgetsPage1_HLayout.addWidget(self.TwoDHistPlot)

        viewWidgetsPage1_VLayout.addLayout(viewWidgetsPage1_HLayout)
        self.viewWidgetsPage1.setLayout(viewWidgetsPage1_VLayout)
        
        #viewWidgetsPage2_GridLayout.addWidget(self.TwoDHistPlot,0,0)
        #viewWidgetsPage2_GridLayout.addWidget(self.histogramPlotLayout,0,1)

        self.viewWidgetsPage2.setLayout(viewWidgetsPage2_GridLayout)
        ##############################
        self.tabs.addTab(self.viewWidgetsPage1, "All in one")
        self.tabs.addTab(self.viewWidgetsPage2, "Additional")
######################## Set control widgets ##########################
        DAQ_setupGroupbox = QGroupBox("DAQ setup")
        DAQ_setupGroupbox.setAlignment(Qt.AlignCenter)

        setup_VLayout = QVBoxLayout()
        setup_HLayout = QHBoxLayout()
        #################### IP validator #############################
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"   # Part of the regular expression
        # Regulare expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self) 
        ######################### IP ##################################
        self.IP = QLineEdit()
        self.IP.setAlignment(Qt.AlignCenter)
        self.IP.setValidator(ipValidator)
        self.IP.setText(self.IPaddress)
        self.IP.setToolTip("DAQ IP comunication")
        self.IP.setFixedWidth(100)
        self.IP.editingFinished.connect(self.IpChanged)
        ######################## GEMROC_ID #################################
        self.GEMROC_ID = QLineEdit()
        self.GEMROC_ID.setAlignment(Qt.AlignCenter)
        self.onlyInt = QIntValidator()
        self.GEMROC_ID.setValidator(self.onlyInt)
        self.GEMROC_ID.setText(str(self.GEMROC_id))
        self.GEMROC_ID.setToolTip("Select GEMROC ID number")
        self.GEMROC_ID.setFixedWidth(100)
        self.GEMROC_ID.editingFinished.connect(self.gemrocIdChanged)
        #################### Mode selector ############################
        modeSelectorHLayout = QHBoxLayout()
        self.TL = QRadioButton("TL")
        self.TL.setChecked(True)
        self.TL.setToolTip("Trigger less mode")
        self.TL.toggled.connect(self.modeClicked)

        self.TM = QRadioButton("TM")
        self.TM.setToolTip("Trigger matched mode")
        modeSelectorHLayout.addWidget(self.TL)
        modeSelectorHLayout.addWidget(self.TM)
        self.TM.toggled.connect(self.modeClicked)
        ################### Tiger selector ############################
        self.tigerGroupSelector = QComboBox()
        self.tigerGroupSelector.addItems(['TIGER(0-1)','TIGER(2-3)','TIGER(4-5)','TIGER(6-7)'])
        self.tigerGroupSelector.setToolTip("Select TIGER group")
        self.tigerGroupSelector.setFixedWidth(100)
        self.tigerGroupSelector.currentIndexChanged.connect(self.chooseTigerGroup)
        ################# Parameter selector ##########################
        self.parameterSelector = QComboBox()
        self.parameterSelector.addItems(self.parameters)
        self.parameterSelector.setCurrentIndex(self.parameters.index(self.selectedPar))
        self.parameterSelector.setToolTip("Select parameter")
        self.parameterSelector.setFixedWidth(100)
        self.parameterSelector.currentIndexChanged.connect(self.chooseParameter)
        ################### Channel selector ##########################
        selectedCh_From_validator = QIntValidator()
        selectedCh_From_validator.setRange(1, 124)
        self.selectedCh_From = QLineEdit()
        self.selectedCh_From.setAlignment(Qt.AlignCenter)
        self.selectedCh_From.setValidator(selectedCh_From_validator)
        self.selectedCh_From.setText(str(self.selectedstrip_From))
        self.selectedCh_From.setToolTip("Select start strip number")
        self.selectedCh_From.setFixedWidth(45)
        self.selectedCh_From.editingFinished.connect(self.selectedStripChanged)

        selectedCh_To_validator = QIntValidator()
        selectedCh_To_validator.setRange(1, 124)
        self.selectedCh_To = QLineEdit()
        self.selectedCh_To.setAlignment(Qt.AlignCenter)
        self.selectedCh_To.setValidator(selectedCh_To_validator)
        self.selectedCh_To.setText(str(self.selectedstrip_To))
        self.selectedCh_To.setToolTip("Select stop strip number")
        self.selectedCh_To.setFixedWidth(45)
        self.selectedCh_To.editingFinished.connect(self.selectedStripChanged)
        ################ Refresh time field ###########################
        delayValidator = QIntValidator()
        delayValidator.setRange(1, 120)
        self.delay = QLineEdit()
        self.delay.setAlignment(Qt.AlignCenter)
        self.delay.setValidator(delayValidator)
        self.delay.setText(str(int(self.delayMiliseconds/1000)))
        self.delay.setToolTip("Set delay")
        self.delay.setFixedWidth(100)
        self.delay.textChanged.connect(self.setRefreshTime)
        #################### Export data ##############################
        self.exportData = QCheckBox('Export data')
        self.exportData.stateChanged.connect(lambda:self.exportDataStateChanged(self.exportData))
        ############### Labels setup on layout ########################
        channelSelectorLabelsHlayout = QHBoxLayout()
        channelSelectorLabelsHlayout.addWidget(QLabel("From"))
        channelSelectorLabelsHlayout.addWidget(QLabel("To"))

        setupLabelsVLayout = QVBoxLayout()
        setupLabelsVLayout.addWidget(QLabel("IP"))
        setupLabelsVLayout.addWidget(QLabel("GEMROC_ID"))
        setupLabelsVLayout.addWidget(QLabel("Mode selector"))
        setupLabelsVLayout.addWidget(QLabel("TIGER selector"))
        setupLabelsVLayout.addWidget(QLabel("Parameter selector"))
        setupLabelsVLayout.addWidget(QLabel(""))
        setupLabelsVLayout.addWidget(QLabel("Strips selector"))
        setupLabelsVLayout.addWidget(QLabel("Refresh delay[s]"))
        setupLabelsVLayout.addWidget(QLabel(""))
        ############### Widgets setup on layout #######################
        channelSelectorWidgetsHlayout = QHBoxLayout()
        channelSelectorWidgetsHlayout.addWidget(self.selectedCh_From)
        channelSelectorWidgetsHlayout.addWidget(self.selectedCh_To)

        setupWidgetsVLayout = QVBoxLayout()
        setupWidgetsVLayout.addWidget(self.IP)
        setupWidgetsVLayout.addWidget(self.GEMROC_ID)
        setupWidgetsVLayout.addLayout(modeSelectorHLayout)
        setupWidgetsVLayout.addWidget(self.tigerGroupSelector)
        setupWidgetsVLayout.addWidget(self.parameterSelector)
        setupWidgetsVLayout.addLayout(channelSelectorLabelsHlayout)
        setupWidgetsVLayout.addLayout(channelSelectorWidgetsHlayout)
        setupWidgetsVLayout.addWidget(self.delay)
        setupWidgetsVLayout.addWidget(self.exportData)
        ############## All items setup on layout ######################
        setup_HLayout.addLayout(setupWidgetsVLayout)
        setup_HLayout.addLayout(setupLabelsVLayout)
        setup_VLayout.addLayout(setup_HLayout)
        setup_VLayout.addStretch(1)
        DAQ_setupGroupbox.setLayout(setup_VLayout)
        ############# Set widgets on main Layout ######################
        MainHLayout.addWidget(DAQ_setupGroupbox,0)
        MainHLayout.addWidget(self.tabs,100)
        ############# Set main widgets on window ######################
        MainWidget.setLayout(MainHLayout)
        self.setCentralWidget(MainWidget)

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
        pg.setConfigOption('background', QColor(53, 53, 53))
        pg.setConfigOption('foreground', QColor(255, 255, 255))
        QApplication.setPalette(pal)
# ++++++++++++++++++++++++ Status Messages ++++++++++++++++++++++++++++
    def statuseMessage(self, message):
        self.statusBar().showMessage(message)
# ++++++++++++++++++++++++++++++ Start ++++++++++++++++++++++++++++++++
    def start(self):
        global _Run
        if _Run == False:
            _Run = True
            self.barData = np.zeros(125, dtype=int)
            try:
                self.delayMiliseconds = int(float(self.delay.text())*1000)
            except ValueError:
                try:
                    self.delayMiliseconds = int(float(self.delay.text().replace(",", "."))*1000)
                except ValueError:
                    pass

            self.timer.start(self.delayMiliseconds)
        ############### Clear global data buffer ######################
            try:
                DATA.clear()
                self.statuseMessage("Stop")
            except AttributeError:
                pass
        ################# Data reading thread #########################
            self.readThread = ReadDataThread(GEMROC_id=self.GEMROC_id,
                                             IP=self.IPaddress,
                                             Port=self.Port,
                                             BUFSIZE=self.BUFSIZE,
                                             mode=self.modeSelector,
                                             exportdata=self.exportDataSatate,
                                             delay="0.0001")
        ##################### Start thread ############################
            self.readThread.start()
            self.statuseMessage("Running")
# ++++++++++++++++++++++++++++++ Stop +++++++++++++++++++++++++++++++++
    def stop(self):
        global _Run
        _Run = False
        try:
            self.readThread.quit()
        except AttributeError:
            pass
        self.timer.stop()

        self.statuseMessage("Stop")
# ++++++++++++++++++++++ Selected strip changed +++++++++++++++++++++++
    def selectedStripChanged(self):
        self.selectedstrip_From = int(self.selectedCh_From.text())
        self.selectedstrip_To = int(self.selectedCh_To.text())
# ++++++++++++++++++++++++++++ IP changed +++++++++++++++++++++++++++++
    def IpChanged(self): 
        self.IPaddress = self.IP.text()
# ++++++++++++++++++++++++ GEMROC_ID changed ++++++++++++++++++++++++++
    def gemrocIdChanged(self):
        self.GEMROC_id = int(self.GEMROC_ID.text())
        self.Port = 58880 + self.GEMROC_id
# ++++++++++++++++++++++++++ Mode changed +++++++++++++++++++++++++++++
    def modeClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.modeSelector = radioButton.text()
# +++++++++++++++++++++++ Choose tiger Group ++++++++++++++++++++++++++
    def chooseTigerGroup(self):
        self.selectedTiger = self.tigerGroupSelector.currentText()
        self.barData = np.zeros(125, dtype=int)
        strips = range(1,len(self.barData))
        self.HistPlot.updateHist(strips, self.barData)
# ++++++++++++++++++++++++ Choose parameter +++++++++++++++++++++++++++
    def chooseParameter(self):
        self.selectedPar = self.parameterSelector.currentText()
        self.HistPlot2.setXlabel(self.selectedPar)
        self.TwoDHistPlot.setYlabel(self.selectedPar)
# ++++++++++++++++++++++++ Set refresh time +++++++++++++++++++++++++++
    def setRefreshTime(self):
        self.delayMiliseconds = int(self.delay.text())*1000
        self.timer.start(self.delayMiliseconds)
# +++++++++++++++++++++++ Export data state +++++++++++++++++++++++++++
    def exportDataStateChanged(self, b):
        if b.isChecked() == True:
            self.exportDataSatate = True
        else:
            self.exportDataSatate = False
# ++++++++++++++++++++++++++++ View data ++++++++++++++++++++++++++++++
    def presentData(self):
        try:
            if self.selectedTiger == 'TIGER(0-1)':
                x1 = []
                x2 = []

                y1 = []
                y2 = []
                for index in range(len(DATA['TIGER:0']['strip'])):
                    if DATA['TIGER:0']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x1.append(DATA['TIGER:0']['strip'][index])
                        y1.append(DATA['TIGER:0'][self.selectedPar][index])

                for index in range(len(DATA['TIGER:1']['strip'])):
                    if DATA['TIGER:1']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x2.append(DATA['TIGER:1']['strip'][index])
                        y2.append(DATA['TIGER:1'][self.selectedPar][index])

            elif self.selectedTiger == 'TIGER(2-3)':
                x1 = []
                x2 = []

                y1 = []
                y2 = []

                for index in range(len(DATA['TIGER:2']['strip'])):
                    if DATA['TIGER:2']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x1.append(DATA['TIGER:2']['strip'][index])
                        y1.append(DATA['TIGER:2'][self.selectedPar][index])

                for index in range(len(DATA['TIGER:3']['strip'])):
                    if DATA['TIGER:3']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x2.append(DATA['TIGER:3']['strip'][index])
                        y2.append(DATA['TIGER:3'][self.selectedPar][index])
            
            elif self.selectedTiger == 'TIGER(4-5)':

                x1 = []
                x2 = []

                y1 = []
                y2 = []

                for index in range(len(DATA['TIGER:4']['strip'])):
                    if DATA['TIGER:4']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x1.append(DATA['TIGER:4']['strip'][index])
                        y1.append(DATA['TIGER:4'][self.selectedPar][index])

                for index in range(len(DATA['TIGER:5']['strip'])):
                    if DATA['TIGER:5']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x2.append(DATA['TIGER:5']['strip'][index])
                        y2.append(DATA['TIGER:5'][self.selectedPar][index])
            
            elif self.selectedTiger == 'TIGER(6-7)':

                x1 = []
                x2 = []

                y1 = []
                y2 = []

                for index in range(len(DATA['TIGER:6']['strip'])):
                    if DATA['TIGER:6']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x1.append(DATA['TIGER:6']['strip'][index])
                        y1.append(DATA['TIGER:6'][self.selectedPar][index])

                for index in range(len(DATA['TIGER:7']['strip'])):
                    if DATA['TIGER:7']['strip'][index] in range(self.selectedstrip_From, self.selectedstrip_To):
                        x2.append(DATA['TIGER:7']['strip'][index])
                        y2.append(DATA['TIGER:7'][self.selectedPar][index])

            X = x1 + x2
            Y = y1 + y2
        ################# Update active page ##########################
            counts, xedges = np.histogram(X, bins=range(1,127))
            self.barData = np.add(self.barData, counts)
            strips = range(1,len(self.barData))
            self.HistPlot.updateHist(strips, self.barData)

            try:
                parMin = min(Y)
                parMax = max(Y)

                parameterValueRange = range(parMin, parMax)
                counts, xedges = np.histogram(Y, bins=range(parMin, parMax+1))
                self.HistPlot2.updateHist(parameterValueRange, counts)
            except ValueError:
                pass

            H = [X,Y]
            self.TwoDHistPlot.update2dHist(H)
            #self.TwoDHistPlot1.update2dHist(H)    
            ############### Clear global data buffer ######################
            DATA.clear()
        except KeyError:
            pass
#######################################################################
    def mouseDoubleClickEvent(self, ev):
        ev.accept()
        print("DoubleClickEvent")
    
    def wheelEvent(self, QWheelEvent):
        print("Wheel event")
#######################################################################
#######################################################################
if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    ex = App()
    app.exec_()