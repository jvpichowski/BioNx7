import serial

ser = serial.Serial("COM3", baudrate = 9600, timeout = 1)

if ser.isOpen():
    ser.close()

ser.open()
print("connected: " + str(ser.isOpen()))

def getposition():
    '''get position printer head from printer'''
    # [x,y,z] 
    return [1,1,1]

# prototypischer Listener, der koordinaten speichert, wenn Touch-Sensor berührt wird
points = []
while 1:
    ser.write(b"down")
    data = ser.readline().decode("ascii")
    # print("Point: "+data)
    if data == "high\r\n": 
        pos = getposition()              
        points.append(pos)        
        print("Point: " + data + "Memory: " + str(points))
    # Abruch nach 10 Messungen
    elif len(points) == 10:
        break


 

# Nutzer kann Befehle über Terminal eingeben
# while 1:
#     # User Input:
#     userInput = input("action: ")
#     if userInput == "down":
#         ser.write(b"down")
#         print("move down")
#     if userInput == "up":
#         ser.write(b"up")
#         print("move up")
#     if userInput == "test":
#         ser.write(b"test")
#         print("test Mode")
#     if userInput == "alarm":
#         ser.write(b"alarm")
#         print("alarm Mode")
#     if userInput == "n":
#         break


        
ser.close()
print("connected: " + str(ser.isOpen()))






# while 1:
#     arduinodata = ser.readline().decode("ascii")
#     print(arduinodata)
