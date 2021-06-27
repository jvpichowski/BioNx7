import cv2
import tensorflow as tf
import numpy as np
#loading model
from tensorflow import keras
from keras.models import model_from_json

#set this Path right !!!!
path= "C:\\Users\\janlu\\Desktop\\BioNx7\\model"
model = keras.models.load_model(path)

model.summary()



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
'''


img_name = "C:\\Users\\janlu\\Desktop\\BioNx7\\data\\test_images\\0.jpg"
#crop_Images(img_name)
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
print(np.argmax(percentages))


# 0-> 6er Wellplate | 1 -> 12er Wellplate | 2-> 96er Wellplate
