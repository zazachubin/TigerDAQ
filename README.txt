########### This is TIGER data acquisition monitoring program ###########

# Requirements:
   * Windows or Linux
   * Python3
   * Python libs:
         python3 -m pip install matplotlib
         python3 -m pip install pyqt5
         python3 -m pip install numpy
   * Build project by:
         python3 -m pip install pyinstaller

# Build program:
   pyinstaller --noconfirm --onefile --windowed .\TigerDAQ.py

# Run program source code:
   python3 .\TigerDAQ.py