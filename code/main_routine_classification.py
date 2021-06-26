import cv2
import tensorflow as tf
import numpy as np
#loading model
from tensorflow import keras
from keras.models import model_from_json

#set this Path right !!!!
path= "C:\\Users\\Jan Lukas\\Desktop\\BioNx7\\model"
model = keras.models.load_model(path)

model.summary()

#choose right camera either 0 or 1 
cam = cv2.VideoCapture(0)
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

'''
image = cv2.imread(img_name)
import matplotlib.pyplot as plt
plt.imshow(image.astype("uint8"))
plt.show()

crop_Images(img_name)
'''
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
well_type= np.argmax(percentages)
print(well_type)

well_0 = [[-2.35,2.25],[-4,0],[-4,0],[0,4],[4,0],[4,0]]
well_1 = [[-2.35,1.55],[-2.7,0],[-2.7,0],[-2.7,0],[0,2.7],[2.7,0],[2.7,0],[2.7,0],[0,2.7],[-2.7,0],[-2.7,0],[-2.7,0]]
well_2 = [[-1.4,1.1],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[0,0.9],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0], [0,0.9],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[0,0.9],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0], [0,0.9],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[0,0.9],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0.9,0],[0,0.9],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0],[-0.9,0]]

if(well_type==0):
    print(well_0)
elif(well_type==1):
    print(well_1)
else:
    print(well_2)
