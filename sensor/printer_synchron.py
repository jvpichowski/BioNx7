
import serial
import time
import io

def getposition(ser):
    for x in range(20):
        res = ser.readline().decode("ascii") 
        if res[0] == "X":
            return res
    return "mistake"
            

ser = serial.Serial("COM8", baudrate = 250000, timeout = 5)

# First 8 lines of output not interesting
# for x in range(8):
#     response = ser.readline().decode("ascii")    
    
# home
time.sleep(2)
ser.write(b"G28\r\n")
time.sleep(18)
ser.write(b"M114\r\n")
pos = getposition(ser)
print(pos)

time.sleep(2)

# move (just one move)
print("move")
ser.write(b"G1 Z40\r\n")
ser.write(b"M114\r\n")
pos = getposition(ser)
print(pos)

# move (just one move)
print("move")
ser.write(b"G1 X500\r\n")
ser.write(b"M114\r\n")
pos = getposition(ser)
print(pos)


time.sleep(2)


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