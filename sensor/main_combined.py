import serial
import time
import io
import re
import cv2
import tensorflow as tf
import numpy as np
#loading model
from tensorflow import keras
from keras.models import model_from_json

# input: [(x,y),(x,y),(x,y)]

COM_printer = "COM3"
COM_touch = "COM4"



#set this Path right !!!!
path= "C:\\Users\\Jan Lukas\\Desktop\\BioNx7\\model"
print("This path is used to locate the model: ", path)



class PrinterControll():
    def __init__(self, printer_script):
        self.printer_script = printer_script
        

        #init Ports
        self.ser = serial.Serial(COM_printer, baudrate = 250000, timeout = 5)
        self.ser_touch = serial.Serial(COM_touch, baudrate = 9600, timeout = 5)
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
        self.ser = serial.Serial(COM_printer, baudrate = 250000, timeout = 5)
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
                #self.ser = serial.Serial(COM_printer, baudrate = 250000, timeout = 5)
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

model = keras.models.load_model(path)

model.summary()

#choose right camera either 0 or 1 
cam = cv2.VideoCapture(1)
img_counter = 0 
cv2.namedWindow("test")
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        image = frame
        img_counter = img_counter+1
        cv2.imwrite(img_name,image)
        break

cam.release()

from PIL import Image

def crop_Images(path):
  # Opens a image in RGB mode
  
  import cv2 
  import os 
  import glob
  img = Image.open(img_name) 
  width, height = img.size
    
  # Setting the points for cropped image
  left = 240
  top = 100
  right = width
  bottom =  height
    
  # Cropped image of above dimension
  # (It will not change orginal image)
  im1 = img.crop((left, top, right, bottom))
  im1.save(img_name)


#testing


image = cv2.imread(img_name)
import matplotlib.pyplot as plt
plt.imshow(image.astype("uint8"))
plt.show()

crop_Images(img_name)

image = cv2.imread(img_name)

import matplotlib.pyplot as plt
plt.imshow(image.astype("uint8"))
plt.show()

image_size = (400, 380)

img = keras.preprocessing.image.load_img(
      img_name, target_size=image_size
  )
img_array = keras.preprocessing.image.img_to_array(img)
percentages = model.predict(tf.expand_dims(img_array, 0))

# 0-> 6er Wellplate | 1 -> 12er Wellplate | 2-> 96er Wellplate
print(percentages)
well_type= np.argmax(percentages)
print(well_type)

well_0 = [[-2.35,2.25],[-4,0],[-4,0],[0,4],[4,0],[4,0]]
well_1 = [[-2.35,1.55],[-2.7,0],[-2.7,0],[-2.7,0],[0,2.7],[2.7,0],[2.7,0],[2.7,0],[0,2.7],[-2.7,0],[-2.7,0],[-2.7,0]]
well_2 = [[-1.4,1.1],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[0,0.9],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0], [0,0.9],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[0,0.9],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0], [0,0.9],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[0,0.9],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0,0.9],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0]]
printerControll = []

if(well_type==0):
    printerControll = [[j*10 for j in i] for i in well_0]
elif(well_type==1):
    printerControll = [[j*10 for j in i] for i in well_1]
else:
    printerControll = [[j*10 for j in i] for i in well_2]

print(printerControll)



#printerControll = PrinterControll([(20,20), (40,40), (60,60)])
print(printerControll.start_run())


    




    
    


    

   


