
import serial
import time
import io
import re

def getposition(ser):
    for x in range(20):
        res = ser.readline().decode("ascii") 
        if res[0] == "X":
            pos = getpositionvalues(res)
            return pos
    return "mistake"

def getpositionvalues(position_raw):
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


def readmove(direction, value):
    return "G1 " + direction + str(value) + "\r\n"


            

ser = serial.Serial("COM8", baudrate = 250000, timeout = 5)
ser_touch = serial.Serial("COM3", baudrate = 9600, timeout = 5)

# First 8 lines of output not interesting
# for x in range(8):
#     response = ser.readline().decode("ascii")  
time.sleep(5)  
ser_touch.write(b'up\r\n')

ser_touch.write(b"release\r\n")

# home
print("homing")
time.sleep(2)
ser.write(b"G28\r\n")
time.sleep(10)
ser.write(b"M114\r\n")
pos = getposition(ser)
print(pos)

ser.close()
ser = serial.Serial("COM8", baudrate = 250000, timeout = 5)

time.sleep(2)

# move (just one move)
print("move Z 40")
ser.write(b"G1 Z40\r\n")
time.sleep(10)
ser.write(b"M114\r\n")
pos = getposition(ser)
print(pos)

# move (just one move)
print("move X 50")
ser.write(b"G1 X50\r\n")
time.sleep(10)
ser.write(b"M114\r\n")
pos = getposition(ser)
print(pos)


time.sleep(2)

print("Touchsensor down")
ser_touch.write(b"down\r\n")
time.sleep(2)
#print("move")
print("move Z 0")
ser.write(b"G1 Z0\r\n")
#time.sleep(18)
#ser.write(b"M114\r\n")
#pos = getposition(ser)
#print(pos)

while 1:
    #ser.write(b"down")
    data = ser_touch.readline().decode("ascii")
    # print("Point: "+data)
    if data == "high\r\n": 
        #pos = getposition()  
        ser_touch.write(b"up\r\n")
        ser_touch.write(b"stop\r\n")
        ser.write(b"M114\r\n") 
        pos = getposition(ser)           
        #points.append(pos)        
        print(pos)
        break
    
    

#ser.write(b"M114\r\n")




# sio.flush() # it is buffering. required to get the data out *now*
# response = sio.readline()
# for x in range(5):
#     response = ser.readline()
#     print(response)
#     print(x)



# ser.write(b"G1 X10\r\n")
# ser.write(b"M114\r\n")
# count = 0
# while 1:
#     ser.readline().decode("ascii")
#     count += 1
#     print(count)
#     if count == 10:
#         break
# ser.write(b"G1 Y50\r\n")
# ser.write(b"G1 Z20\r\n")
# time.sleep(1)
ser.close()
print("connected: " + str(ser.isOpen()))

# if ser.isOpen():
#     ser.close()

# ser.open()
# print("connected: " + str(ser.isOpen()))

# def getposition():
#     '''get position printer head from printer'''
#     # [x,y,z] 
#     return [1,1,1]

# # prototypischer Listener, der koordinaten speichert, wenn Touch-Sensor berührt wird
# points = []
# while 1:
#     ser.write(b"G0 X12")
#     # data = ser.readline().decode("ascii")
#     # print("Point: "+data)
#     # if data == "high\r\n": 
#     #     pos = getposition()              
#     #     points.append(pos)        
#     #     print("Point: " + data + "Memory: " + str(points))
#     # Abruch nach 10 Messungen
#     # elif len(points) == 10:
#     #     break
#     break

# ser.close()
# print("connected: " + str(ser.isOpen()))