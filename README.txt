########### This is TIGER data acquisition monitoring software ###########

* Program reads data from the GEMROC DAQ and TIGER electronics system through ethernet (IP - 192.168.1.200)
  and interprets it with 1D and 2D histograms.

* Software is used for online monitoring purposes.

* Package contains data generator script for testing purpose (DataGenerator\transferDatFile.py)

# Requirements:
   * Windows or Linux
   * Python3
   * Python libs:
         python3 -m pip install pyqt5
         python3 -m pip install pyqtgraph
         python3 -m pip install numpy
         python3 -m pip install keyboard
   * Build project by:
         python3 -m pip install pyinstaller

# Build program:
   pyinstaller --noconfirm --onefile --windowed .\TigerDAQ.py

# Run program source code:
   python3 .\TigerDAQ.py