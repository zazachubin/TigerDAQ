from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QMessageBox, QPushButton, QAction, QVBoxLayout,
                             QHBoxLayout, QDockWidget, QFileDialog, QTabWidget,
                             QGridLayout, QGroupBox, QLineEdit, QLabel, QComboBox, QProgressBar)
from PyQt5.QtGui import QIcon, QPalette, QColor, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt, QDir, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.offsetbox import AnchoredText
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import binascii
import random
import copy
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
# Global control of threads (run & stop)
_Run  = False
# Control debugging
debug = False

# save txt file
saveFile = False

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
                     'color':  'Black',
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
            self.hist, self.xbins, self.ybins, self.im = self.ax.hist2d(self.X, self.Y, cmap = 'plasma', bins=x_max, norm = mpl.colors.LogNorm())
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
                     'color':  'Black',
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
        self.ax.minorticks_on()
        self.ax.grid()
# ++++++++++++++++++++++++++++ updateHist +++++++++++++++++++++++++++++
    def updateHist(self, data):
        ############### Clear 2D histogram data #######################
        self.ax.clear()
        ################# Calculate statistics ########################
        try:
            Data_Entries = np.size(data)
            Data_min = round(np.min(data),2)
            Data_max = round(np.max(data),2)
            Data_mean = round(np.mean(data),2)
            Data_median = round(np.median(data),2)
            Data_std = round(np.std(data),2)
        except ValueError:
            Data_Entries = 0
            Data_min = 0
            Data_max = 0
            Data_mean = 0
            Data_median = 0
            Data_std = 0
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
        self.ax.minorticks_on()
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
    progress = pyqtSignal(float)
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
        #while _Run:
        ###################### Read data ##############################
        self.datFileReading()
        _Run = False
        #################### Simulate data ############################
            #self.simulateData()
            #QThread.msleep(self.delay)
# ++++++++++++++++++++++++ DAT file reading +++++++++++++++++++++++++++
    def datFileReading(self, outputFileName="path.datout.txt"):
        ################ get info about file ##########################
        statinfo = os.stat(self.path)
        outputFileName = self.path.split('.dat')[0] + '.datout.txt'

        ############## Create output text file ########################
        if saveFile:
            f = open(outputFileName, 'w')
            f.close()

        self.thr_scan_matrix = np.zeros((8, 64))  # Tiger, Channel

        ################ Read dat file data ###########################
        with open(self.path, 'rb') as f:
            for i in range(0, int(statinfo.st_size / 8)):
                percent = i*100/int(statinfo.st_size / 8)
                self.progress.emit(percent)
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
                try:
                    tigerId = ((int_x >> 56) & 0x7)
                    ch = ((int_x >> 48) & 0x3F)
                    ch = mapping['Chip{}_Ch{}'.format(tigerId+1, ch)]
                    print('TIGER:{} -- Ch{}'.format(tigerId, ch))

                    tacId = ((int_x >> 46) & 0x3)
                    tcoarse = ((int_x >> 30) & 0xFFFF)
                    ecoarse = ((int_x >> 20) & 0x3FF)
                    tfine = ((int_x >> 10) & 0x3FF)
                    efine = (int_x & 0x3FF)
        ######### calculate ToT ##################
                    if (((int_x >> 20)&0x3FF) - ((int_x >> 30)&0x3FF)) > 0:
                        ToT=(((int_x >> 20)&0x3FF) - ((int_x >> 30)&0x3FF))
                    else:
                        ToT=(((int_x >> 20)&0x3FF) - ((int_x >> 30)&0x3FF)) + 1023
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
                        DATA["TIGER:{}".format(tigerId)]['ToT'].append(ToT)
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

                        DATA["TIGER:{}".format(tigerId)]['ToT'].append(ToT)
        ############# Debugging of data reading #######################
                    if debug:
                        print('******************')
                        print('TIGER: {}'.format(tigerId))
                        print('Strip: {}'.format(ch))
                        print('tacId: {}'.format(tacId))
                        print('Tcoarse: {}'.format(tcoarse))
                        print('Ecoarse: {}'.format(ecoarse))
                        print('Tfine: {}'.format(tfine))
                        print('Efine: {}'.format(efine))
                        print('ToT: {}'.format(ToT))
        ############### Calculate current time ########################
                    # Time= Framecount*204,8ns + Tcoarse*6,25ns
                    if ((int_x >> 30) & 0xFFFF) < 2^15:
                        Time = ((int_x >> 15) & 0xFFFF) * 204800 + ((int_x >> 30) & 0xFFFF) * 6.25
                    
                    if ((int_x >> 30) & 0xFFFF) > 2^15:
                        Time= ((int_x >> 15) & 0xFFFF) * 204800 + (((int_x >> 30) & 0xFFFF)-2^15) * 6.25
        ############### Write data to log file ########################
                    if saveFile:
                        with open(outputFileName, 'a') as ff:
                            #ff.write("{}     {}".format(raw, s))
                            ff.write("{}".format(s))
                except KeyError:
                    pass
        #################### Thread delay #############################
                #QThread.msleep(self.delay)
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon('img/DAQ.svg'))
        self.setWindowTitle('DAQ')
        self.setGeometry(0, 0, 1500, 800)
        self.statuseMessage("")

        self.selectedPar = 'tcoarse'
        self.selectedTiger = 'TIGER(0-1)'
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


        self.TwoDHistPlot = Plot2DHistogram(title="2D hist",Xlabel="Strips",Ylabel=self.selectedPar)
        viewWidgetsPage1_VLayout.addWidget(self.TwoDHistPlot)

        TwoDHistPlot_toolbar = NavigationToolbar2QT(self.TwoDHistPlot, self)
        viewWidgetsPage1_VLayout.addWidget(TwoDHistPlot_toolbar)
        self.viewWidgetsPage1.setLayout(viewWidgetsPage1_VLayout)

        ##############################
        self.TwoDHistPlot1 = Plot2DHistogram(title="Tcourse 2D hist",Xlabel="Strips",Ylabel="Tcourse")
        self.TwoDHistPlot2 = Plot2DHistogram(title="Ecoarse 2D hist",Xlabel="Strips",Ylabel="Ecoarse")
        self.TwoDHistPlot3 = Plot2DHistogram(title="Tfine 2D hist",Xlabel="Strips",Ylabel="Tfine")
        self.TwoDHistPlot4 = Plot2DHistogram(title="Efine 2D hist",Xlabel="Strips",Ylabel="Efine")


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
        ############## Parameter selector label #######################
        parameterSelectorLabel = QLabel("Parameter selector")
        ############ Set widgets on delay layouts #####################
        delayHLayout.addWidget(self.delay)
        delayHLayout.addWidget(delayLabel)
        ################ Tiger selector Layout ########################
        tigerSelectorHLayout = QHBoxLayout()
        ################ Tiger selector label #########################
        tigerSelectorLabel = QLabel("Tiger selector")
        ###############################################################
        # Create combobox and add items.
        self.tigerGroupSelector = QComboBox()
        self.tigerGroupSelector.addItems(['TIGER(0-1)','TIGER(2-3)','TIGER(4-5)'])
        self.tigerGroupSelector.currentIndexChanged.connect(self.chooseTigerGroup)
        ##### Set widgets on tiger Group Selector layouts #############
        tigerSelectorHLayout.addWidget(self.tigerGroupSelector)
        tigerSelectorHLayout.addWidget(tigerSelectorLabel)
        ################ Channel selector Layout ######################
        channelSelectorHLayout = QHBoxLayout()
        ################# Channel selector label ######################
        channelSelectorLabel = QLabel("Channel selector")
        #################### Channel selector #########################
        validator = QIntValidator()
        validator.setRange(1, 124)
        self.selectedCh = QLineEdit()
        self.selectedCh.textChanged.connect(self.setRefreshTime)
        self.selectedCh.setAlignment(Qt.AlignCenter)
        self.selectedCh.setValidator(validator)
        self.selectedCh.setText('')
        ##### Set widgets on tiger Group Selector layouts #############
        channelSelectorHLayout.addWidget(self.selectedCh)
        channelSelectorHLayout.addWidget(channelSelectorLabel)
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
        DAQ_VLayout.addLayout(tigerSelectorHLayout)
        DAQ_VLayout.addLayout(parameterSelectorHLayout)
        DAQ_VLayout.addLayout(channelSelectorHLayout)
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
############################# ProgressBar  ############################
        self.progressBar = QProgressBar()   
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setValue(0)
        self.progressBar.setFormat("%.02f %%" % 0)

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
                self.thread1.progress.connect(self.viewProgressBar)
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
# +++++++++++++++++++++++ Choose tiger Group ++++++++++++++++++++++++++
    def chooseTigerGroup(self):
        self.selectedTiger = self.tigerGroupSelector.currentText()
# ++++++++++++++++++++++++++++ View data ++++++++++++++++++++++++++++++
    def presentData(self):
        ######### Check global buffer if contains data ################
        if len(DATA.keys()) != 0:
        ####### Get all TIGER ID keys from global buffer ##############
            try:
                if self.selectedCh.text() != '':
                    if self.selectedTiger == 'TIGER(0-1)':
                        x1 = []
                        x2 = []

                        y1 = []
                        y2 = []

                        for index in range(len(DATA['TIGER:0']['ch'])):
                            if DATA['TIGER:0']['ch'][index] == int(self.selectedCh.text()):
                                x1.append(DATA['TIGER:0']['ch'][index])
                                y1.append(DATA['TIGER:0'][self.selectedPar][index])

                        for index in range(len(DATA['TIGER:1']['ch'])):
                            if DATA['TIGER:1']['ch'][index] == int(self.selectedCh.text()):
                                x2.append(DATA['TIGER:1']['ch'][index])
                                y2.append(DATA['TIGER:1'][self.selectedPar][index])

                    elif self.selectedTiger == 'TIGER(2-3)':
                        x1 = []
                        x2 = []

                        y1 = []
                        y2 = []

                        for index in range(len(DATA['TIGER:2']['ch'])):
                            if DATA['TIGER:2']['ch'][index] == int(self.selectedCh.text()):
                                x1.append(DATA['TIGER:2']['ch'][index])
                                y1.append(DATA['TIGER:2'][self.selectedPar][index])

                        for index in range(len(DATA['TIGER:3']['ch'])):
                            if DATA['TIGER:3']['ch'][index] == int(self.selectedCh.text()):
                                x2.append(DATA['TIGER:3']['ch'][index])
                                y2.append(DATA['TIGER:3'][self.selectedPar][index])
                    
                    elif self.selectedTiger == 'TIGER(4-5)':

                        x1 = []
                        x2 = []

                        y1 = []
                        y2 = []

                        for index in range(len(DATA['TIGER:4']['ch'])):
                            if DATA['TIGER:4']['ch'][index] == int(self.selectedCh.text()):
                                x1.append(DATA['TIGER:4']['ch'][index])
                                y1.append(DATA['TIGER:4'][self.selectedPar][index])

                        for index in range(len(DATA['TIGER:5']['ch'])):
                            if DATA['TIGER:5']['ch'][index] == int(self.selectedCh.text()):
                                x2.append(DATA['TIGER:5']['ch'][index])
                                y2.append(DATA['TIGER:5'][self.selectedPar][index])

                else:
                    if self.selectedTiger == 'TIGER(0-1)':
                        x1 = DATA['TIGER:0']['ch']
                        x2 = DATA['TIGER:1']['ch']

                        y1 = DATA['TIGER:0'][self.selectedPar]
                        y2 = DATA['TIGER:1'][self.selectedPar]
                    
                    elif self.selectedTiger == 'TIGER(2-3)':
                        x1 = DATA['TIGER:2']['ch']
                        x2 = DATA['TIGER:3']['ch']

                        y1 = DATA['TIGER:2'][self.selectedPar]
                        y2 = DATA['TIGER:3'][self.selectedPar]
                    
                    elif self.selectedTiger == 'TIGER(4-5)':
                        x1 = DATA['TIGER:4']['ch']
                        x2 = DATA['TIGER:5']['ch']

                        y1 = DATA['TIGER:4'][self.selectedPar]
                        y2 = DATA['TIGER:5'][self.selectedPar]

                X = x1 + x2
                Y = y1 + y2
            ################# Update active page ##########################
                ############### Page 1 ################################
                if self.tabs.currentIndex() == 0:
                    self.HistPlot.updateHist(Y)
                    self.TwoDHistPlot.update2dHist([X, Y])
                ############### Page 2 ################################
                elif self.tabs.currentIndex() == 1:
                    if self.selectedTiger == 'TIGER(0-1)':
                        tcoarse = DATA['TIGER:0']['tcoarse'] + DATA['TIGER:1']['tcoarse']
                        ecoarse = DATA['TIGER:0']['ecoarse'] + DATA['TIGER:1']['ecoarse']
                        tfine = DATA['TIGER:0']['tfine'] + DATA['TIGER:1']['tfine']
                        efine = DATA['TIGER:0']['efine'] + DATA['TIGER:1']['efine']
                    
                    elif self.selectedTiger == 'TIGER(2-3)':
                        tcoarse = DATA['TIGER:2']['tcoarse'] + DATA['TIGER:3']['tcoarse']
                        ecoarse = DATA['TIGER:2']['ecoarse'] + DATA['TIGER:3']['ecoarse']
                        tfine = DATA['TIGER:2']['tfine'] + DATA['TIGER:3']['tfine']
                        efine = DATA['TIGER:2']['efine'] + DATA['TIGER:3']['efine']
                    
                    elif self.selectedTiger == 'TIGER(4-5)':
                        tcoarse = DATA['TIGER:4']['tcoarse'] + DATA['TIGER:5']['tcoarse']
                        ecoarse = DATA['TIGER:4']['ecoarse'] + DATA['TIGER:5']['ecoarse']
                        tfine = DATA['TIGER:4']['tfine'] + DATA['TIGER:5']['tfine']
                        efine = DATA['TIGER:4']['efine'] + DATA['TIGER:5']['efine']

                    self.TwoDHistPlot1.update2dHist([X, tcoarse])
                    self.TwoDHistPlot2.update2dHist([X, ecoarse])
                    self.TwoDHistPlot3.update2dHist([X, tfine])
                    self.TwoDHistPlot4.update2dHist([X, efine])
            ############### Clear global data buffer ######################
                DATA.clear()

            except KeyError:
                pass        
# ++++++++++++++++++++++++ View ProgressBar +++++++++++++++++++++++++++
    def viewProgressBar(self, percent):
        self.progressBar.setValue(percent)
        self.progressBar.setFormat("%.02f %%" % percent)
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