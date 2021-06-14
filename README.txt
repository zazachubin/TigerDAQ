########### This is TIGER data acquisition monitoring program ###########

# Requirements:
   * Windows or Linux
   * Python3
   * Python libs:
         python3 -m pip install pyqtgraph
         python3 -m pip install pyqt5
   * Build project by:
         python3 -m pip install pyinstaller

# Build program:
   pyinstaller --noconfirm --onefile --windowed .\TigerDAQ.py

# Run program:
   python3 .\TigerDAQ.py