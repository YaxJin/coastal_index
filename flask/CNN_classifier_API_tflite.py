#!/usr/bin/env python
# coding: utf-8
import tensorflow as tf

import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import PIL


img_size = 64
fpath = r"C:\Users\admin\Desktop\beachData2"
imgFolder = r"C:\Users\admin\Desktop\beach1_1280"


def load_model(model_name):
    interpreter = tf.lite.Interpreter(model_path=model_name)
    interpreter.allocate_tensors()
    return interpreter


def predict_trash(img_path, model):
    # load image
    test = tf.keras.preprocessing.image.load_img(img_path)
    s = test.size
    
    input_details = model.get_input_details()
    output_details = model.get_output_details()
    input_shape = input_details[0]['shape']

    objects = []
    classes = []

    for h in range(0, s[1], img_size):
        for w in range(0,s[0],img_size):
            if w+img_size <= s[0] and h+img_size <= s[1]:
                img = test.crop((w, h, w+img_size, h+img_size))
                obj = {"x": w, "y": h, "w": img_size, "h": img_size, "prediction": None}
            elif w+img_size > s[0] and h+img_size <= s[1]:
                img = test.crop((w, h, s[0], h+img_size))
                img = img.resize((64, 64), resample=PIL.Image.NEAREST)
                obj = {"x": w, "y": h, "w": s[0]-w, "h": img_size, "prediction": None}
            elif w+img_size <= s[0] and h+img_size > s[1]:
                img = test.crop((w, h, w+img_size, s[1]))
                img = img.resize((64, 64), resample=PIL.Image.NEAREST)
                obj = {"x": w, "y": h, "w": img_size, "h": s[1]-h, "prediction": None}
            elif w+img_size > s[0] and h+img_size > s[1]:
                img = test.crop((w, h, s[0], s[1]))
                img = img.resize((64, 64), resample=PIL.Image.NEAREST)
                obj = {"x": w, "y": h, "w": s[0]-w, "h": s[1]-h, "prediction": None}
                
            img = tf.keras.preprocessing.image.img_to_array(img)
            img = np.expand_dims(img, axis=0) # expand dimension to fit input shape
            
            # Test the model on input data.
            model.set_tensor(input_details[0]['index'], img)
            model.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            prediction = model.get_tensor(output_details[0]['index'])
            prediction = np.argmax(prediction, axis=1) # get predicted class
            obj["prediction"] = prediction[0] # 
            classes.append(prediction[0])
            objects.append(obj)
            
    # print(classes)
    # print(objects)
    
    return classes, objects


# mask prediction result on image
def mask_prediction(img_path, classes, border=-1, alpha=0.25, beta=0.75, img_size=64):
    c = 0
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    height, weight, _ = img.shape
    
    for h in range(0, height, img_size):
        for w in range(0, weight, img_size):
            if classes[c]==1:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (0,255,0), border) #green
            elif classes[c]==2:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (0,255,0), border) #green
            elif classes[c]==3:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (0,255,0), border) #green
            elif classes[c]==4:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (0,255,0), border) #green
            elif classes[c]==6:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (255,0,0), border) #red
            elif classes[c]==11:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (255,150,0), border) #red
            elif classes[c]==9:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (0,255,0), border) #yellow
            else:
                mask = cv2.rectangle(img.copy(), (w, h), (w+img_size, h+img_size), (255,255,255), border) #white
            c += 1
            img = cv2.addWeighted(mask, alpha, img, beta, 0.0)
            
    # show result
    plt.imshow(img)
    plt.show()

    
# calculate dirty score
def calculate_score(predictions):
    unique, counts = np.unique(predictions, return_counts=True)

    d = dict(zip(unique, counts))

    total_beach = d.get(1, 0) + d.get(2, 0) + d.get(3, 0) + d.get(4, 0) + d.get(9, 0) + d.get(6, 0) + d.get(11,0)
    trash = d.get(6, 0) + d.get(11,0)
    if total_beach == 0:
        print("No beach detected")
        return None
    else:
        dirty_score = trash/total_beach
        print("Dirty_Score: {:.1f}%".format(dirty_score*100))
        return dirty_score


# test
if __name__ == "__main__":
    model_name = "model.tflite"
    loaded_model = load_model(model_name)

    imgPath = r"C:\Users\admin\Desktop\beach1_1280\clean.jpg"
    predictions, objs = predict_trash(imgPath, loaded_model)
    mask_prediction(imgPath, predictions)
    score = calculate_score(predictions)
    result = {"score": score, "objects": objs}
    print(result)
