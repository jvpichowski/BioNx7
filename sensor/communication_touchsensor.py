import serial

ser = serial.Serial("COM3", baudrate = 9600, timeout = 1)

if ser.isOpen():
    ser.close()

ser.open()
print("connected: " + str(ser.isOpen()))


while 1:
    userInput = input("action: ")
    if userInput == "down":
        ser.write(b"down")
        print("move down")
    if userInput == "up":
        ser.write(b"up")
        print("move up")
    if userInput == "test":
        ser.write(b"test")
        print("test Mode")
    if userInput == "alarm":
        ser.write(b"alarm")
        print("alarm Mode")
    if userInput == "n":
        break
        
ser.close()
print("connected: " + str(ser.isOpen()))






# while 1:
#     arduinodata = ser.readline().decode("ascii")
#     print(arduinodata)
