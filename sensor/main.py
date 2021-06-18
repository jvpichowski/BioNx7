import serial
import time
import io
import re

# input: [(x,y),(x,y),(x,y)]


def main():
    printerControll = PrinterControll([(20,20), (40,40), (60,60)])
    print(printerControll.start_run())

class PrinterControll():
    def __init__(self, printer_script):
        self.printer_script = printer_script
        

        #init Ports
        self.ser = serial.Serial("COM8", baudrate = 250000, timeout = 5)
        self.ser_touch = serial.Serial("COM3", baudrate = 9600, timeout = 5)
        self.homing()
        

    def homing(self):
        print("homing")
        time.sleep(2)
        self.ser_touch.write(b"up\r\n")
        self.ser.write(b"G28\r\n")
        time.sleep(15)
        pos = self.getposition()
        print(pos)
        self.ser.close()
        self.ser = serial.Serial("COM8", baudrate = 250000, timeout = 5)
        time.sleep(2)
    
    def readmove(self, value):
        return "G1 X" + str(value[0]) + " Y" + str(value[1]) + "\r\n"

    def start_run(self):
        print("start run")
        positions = []
        for pos in self.printer_script:
            self.ser.write(b"G1 Z40\r\n")
            gcode = ("G1 X" + str(pos[0]) + " Y" + str(pos[1]) + " Z40\r\n").encode("UTF-8")
            print(gcode)
            time.sleep(2)
            self.ser.write(gcode)
            pos = self.measure()
            positions.append(pos)
            print(pos)
        return positions
            #return

    def measure(self):
        print("measuring")
        self.ser_touch.write(b"down\r\n")
        self.ser.write(b"G1 Z0\r\n")
        while 1:
            data = self.ser_touch.readline().decode("ascii")
            if data == "high\r\n": 
                self.ser_touch.write(b"up\r\n")
                self.ser_touch.write(b"stop\r\n")
                pos = self.getposition()
                self.ser_touch.write(b"release\r\n")
                #time.sleep(1) #ggf remove
                #self.ser.close()
                #self.ser = serial.Serial("COM8", baudrate = 250000, timeout = 5)
                #time.sleep(2)
                #gcode_actual_pos = ("G91 X" + str(pos[0]) + " Y" + str(pos[1]) + " Z" + str(pos[2])).encode("UTF-8")
                ##self.ser.write(gcode_actual_pos)   
                gcode = ("G1 Z" + str(40-pos[2]) + "\r\n").encode("UTF-8")                        
                self.ser.write(gcode)
                self.homing()
                return pos


    def getposition(self):
        self.ser.write(b"M114\r\n")
        for x in range(20):
            res = self.ser.readline().decode("ascii") 
            if res[0] == "X":
                pos = self.getpositionvalues(res)
                return pos
        return "mistake"

    def getpositionvalues(self, position_raw):
        reg = '[XYZE]'
        result = re.finditer(reg, position_raw)    
        pos = []
        for match in result:
            pos.append(match.span())
            #print(match.group())
            #print(match.span())
        posX = pos[4][0]
        posY = pos[5][0]
        posZ = pos[6][0]
        #posE = pos[3][0]
        return [float(position_raw[posX+2:posY]),float(position_raw[posY+2:posZ]),float(position_raw[posZ+2:len(position_raw)-1])]

    


if __name__ == "__main__":
    main()


    
    


    

   


