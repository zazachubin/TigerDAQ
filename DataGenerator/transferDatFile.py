import socket
import time
import binascii
import os
import keyboard

GEMROC_ID = 0
port = 58880 + GEMROC_ID
IP_address = "127.0.0.1"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(None)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

path = "./RUN26_SubRUN_0_GEMROC_0_TL.dat"
statinfo = os.stat(path)

#file1 = open("T.txt", "w")
#file1.close()

with open(path, 'rb') as f:
    for _ in range(0, statinfo.st_size // 8):
        if keyboard.is_pressed("q"):
            sock.close()
            break
        data_pack = f.read(1440)

        for slices in range(0,len(data_pack)//8):
            data=data_pack[slices*8:slices*8+8]

            hexdata = binascii.hexlify(data)
            string= "{:064b}".format(int(hexdata,16))
            raw_raw="{} \n".format(string)
            inverted=[]
            for i in range (8,0,-1):
                inverted.append(string[(i-1)*8:i*8])
            string_inv="".join(inverted)
            int_x = int(string_inv,2)
            raw = "{:064b}  ".format(int_x)

            if (((int_x & 0xFF00000000000000) >> 59) == 0x04):  # It's a frameword
                s = 'TIGER: ' + '%01X ' % ((int_x >> 56) & 0x7) + 'HB: ' + 'Framecount: %08X ' % (
                        (int_x >> 15) & 0xFFFF) + 'SEUcount: %08X\n' % (int_x & 0x7FFF)
                print(s)
            
            if (((int_x & 0xFF00000000000000) >> 59) == 0x08):
                s = 'TIGER ' + '%01X: ' % ((int_x >> 56) & 0x7) + 'CW: ' + 'ChID: %02X ' % (
                        (int_x >> 24) & 0x3F) + ' CounterWord: %016X\n' % (int_x & 0x00FFFFFF)

            if (((int_x & 0xFF00000000000000) >> 59) == 0x00):
                s = 'TIGER ' + '%01X: ' % ((int_x >> 56) & 0x7) + 'EW: ' + 'ChID: %02X ' % (
                            (int_x >> 48) & 0x3F) + 'tacID: %01X ' % ((int_x >> 46) & 0x3) + 'Tcoarse: %04X ' % (
                                (int_x >> 30) & 0xFFFF) + 'Ecoarse: %03X ' % (
                                (int_x >> 20) & 0x3FF) + 'Tfine: %03X ' % ((int_x >> 10) & 0x3FF) + 'Efine: %03X \n' % (
                                int_x & 0x3FF)

                tigerId = ((int_x >> 56) & 0x7)
                ch = ((int_x >> 48) & 0x3F)
                tacId = ((int_x >> 46) & 0x3)
                tcoarse = ((int_x >> 30) & 0xFFFF)
                ecoarse = ((int_x >> 20) & 0x3FF)
                tfine = ((int_x >> 10) & 0x3FF)
                efine = (int_x & 0x3FF)
                print("***************")
                print("TIGER: {}\nChannel: {}\nTAC: {}\nT_coarse: {}\nE_coarse: {}\nT_fine: {}\nE_fine: {}".format(str(tigerId),str(ch),str(tacId),str(tcoarse),str(ecoarse),str(tfine),str(efine)))

            #with open("T.txt", 'a') as ff:
            #    ff.write("{}".format(s))

        sock.sendto(data_pack, (IP_address, port))
        #time.sleep(0.01)
