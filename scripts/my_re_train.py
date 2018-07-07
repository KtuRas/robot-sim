#! /usr/bin/env python

import keras
from keras.models import Sequential, model_from_json

import numpy as np
from numpy import inf
import cv2

np_scan = np.load('my_files/np_scan.npy')
np_frame_name =  np.load('my_files/np_frame_name.npy')
np_cmd_x = np.load('my_files/np_cmd_x.npy')
np_cmd_y = np.load('my_files/np_cmd_y.npy')

imgs = []
scan_i = []
cmd = []

for i in range(len(np_frame_name)):
    # print np_frame_name[i]
    try:
        img = cv2.imread('my_files/' + np_frame_name[i])
        img = cv2.resize(img, (500, 500))
        img = img[250:500,:]
        imgs.append(img)
        scan_i.append(np.concatenate((np_scan[i][0:60], np_scan[i][-61:-1]), axis=0))
        # np_cmd_y[i] += 1.0
        cmd.append(np.append(np_cmd_x[i], np_cmd_y[i]))
    except cv2.error as e:
        pass
    # cv2.imshow('img', img)
    # cv2.waitKey(100)

np_scan_i = np.array(scan_i)
np_imgs = np.array(imgs)

np_imgs = np_imgs.astype('float32')
np_imgs = np_imgs / 127.5 - 1.0

json_file = open('my_files/my_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("my_files/my_model.h5")

loaded_model.compile(loss='mean_squared_error',
                    optimizer=keras.optimizers.Adam(lr=0.00001), metrics=["accuracy"])

loaded_model.summary()

loaded_model.fit([np_imgs, np_scan_i], np_cmd_y, shuffle=True,
                epochs=10, batch_size=1,
                validation_data=([np_imgs, np_scan_i], np_cmd_y))

loaded_model.save_weights('my_files/my_model.h5')
with open('my_files/my_model.json', 'w') as json_file:
    json_file.write(loaded_model.to_json())