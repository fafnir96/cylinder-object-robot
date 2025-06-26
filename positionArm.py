import serial
import time

portRobot = 'COM4'
baudRobot = 115200
timeoutRobot = None
serRobot = serial.Serial(portRobot,baudRobot,timeout=timeoutRobot)

time.sleep(1)

def wait_complete_robot():
    waitstatus = 1
    while True:
        a = serRobot.readline()
        print(a.decode("utf-8"))
        if "ok" in a.decode("utf-8"):
            waitstatus = 0
            break                    

def calibrate():
    serRobot.write(b'G28\r')
    wait_complete_robot()
    pass

def nonlogam():
    #Pindah ke beban
    serRobot.write(b'G0 X0.00 Y216.90 Z130.00 E130.00 F0.00\r') # Geser Rell
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y216.90 Z50.00 E130.00 F0.00\r') # Maju
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y195.00 Z45.00 E130.00 F0.00\r') # Turun
    wait_complete_robot()

    # Piston ON
    serRobot.write(b'M6\r') #M5 for Piston On
    wait_complete_robot()
    serRobot.write(b'M207\r') #Ini buat apa anj
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y195.00 Z130.00 E130.00 F0.00\r') # Angkat beban
    wait_complete_robot()
    time.sleep(1)
    
    # Pindah barang ke tempat beban
    serRobot.write(b'G0 X0.00 Y195.00 Z130.00 E0.00 F0.00\r') # Pindah Rell
    wait_complete_robot()
    time.sleep(1)
    # serRobot.write(b'G0 XN Y195.00 Z130.00 E0.00 F0.00\r') # Gerak Badan ke tempat taro beban
    # wait_complete_robot()
    # time.sleep(1)
    # serRobot.write(b'G0 XN Y195.00 ZN.00 E0.00 F0.00\r') # Turun
    # wait_complete_robot()
    # time.sleep(1)
    
    # Piston OFF
    serRobot.write(b'M7\r') #M3 for Piston Off
    wait_complete_robot()
    serRobot.write(b'M206\r')
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y216.90 Z130.00 E0.00 F0.00\r') # Kembali ke posisi awal
    pass

def logam():
    #Pindah ke beban
    serRobot.write(b'G0 X0.00 Y216.90 Z130.00 E309.00 F0.00\r') # Geser Rell
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y216.90 Z50.00 E309.00 F0.00\r') # Maju
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y195.00 Z45.00 E309.00 F0.00\r') # Turun
    wait_complete_robot()
        
    # Piston ON
    serRobot.write(b'M6\r')
    wait_complete_robot()
    serRobot.write(b'M207\r')
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y200.00 Z130.00 E309.00 F0.00\r') # Angkat beban
    wait_complete_robot()
    time.sleep(1)
    
    # Pindah barang ke tempat beban
    # serRobot.write(b'G0 X0.00 Y200.00 Z210.00 E0.00 F0.00\r') #Pindah Rell
    serRobot.write(b'G0 X0.00 Y195.00 Z130.00 E0.00 F0.00\r') # Pindah Rell
    wait_complete_robot()
    time.sleep(1)
    # serRobot.write(b'G0 XN Y195.00 Z130.00 E0.00 F0.00\r') # Gerak Badan ke tempat taro beban
    # wait_complete_robot()
    # time.sleep(1)
    # serRobot.write(b'G0 XN Y195.00 ZN.00 E0.00 F0.00\r') # Turun
    # wait_complete_robot()
    # time.sleep(1)
    
    # Piston OFF
    serRobot.write(b'M7\r')
    wait_complete_robot()
    serRobot.write(b'M206\r')
    wait_complete_robot()
    time.sleep(1)
    serRobot.write(b'G0 X0.00 Y216.90 Z130.00 E0.00 F0.00\r') # Kembali ke posisi awal
    pass

calibrate()

while True:
    # Membaca data dari port serial
    data = serRobot.readline().decode('utf-8').strip()
    print(data)  # Menampilkan data yang diterima
    
    if "LOGAM" in data:
        print("S2 OFF")
        print("logam")
        logam()  # Panggil fungsi untuk logam
    if "NON" in data:
        print("S1 OFF")
        print("non")
        nonlogam()  # Panggil fungsi untuk non-logam