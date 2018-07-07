#! /usr/bin/env python

import keras
from keras.layers.merge import Concatenate
from keras.models import Sequential, model_from_json, Model
from keras.layers import Activation, Dense, Conv2D, Flatten, Dropout, concatenate, MaxPool2D, Merge, Input
from keras.preprocessing.image import ImageDataGenerator
# from sklearn.model_selection import train_test_split

import numpy as np
import cv2

np_scan = np.load('my_files/np_scan.npy')
np_frame_name =  np.load('my_files/np_frame_name.npy')
np_cmd_x = np.load('my_files/np_cmd_x.npy')
np_cmd_y = np.load('my_files/np_cmd_y.npy')

imgs = []
scan_i = []
cmd = []

img_size = (640, 480)

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
# np_cmd = np.array(cmd)

np_imgs = np_imgs.astype('float32')
np_imgs = np_imgs / 127.5 - 1.0

print np_imgs.shape
print np_scan_i.shape
# print np_cmd.shape

# print np_cmd

# print np_cmd_y

# print np_scan_i[0][0]

# exit(0)

img_inputs = Input(shape=(250, 500, 3))
scan_inputs = Input(shape=(120, ))

conv_1 = Conv2D(24, (5, 5), strides=(2, 2), activation='elu')(img_inputs)

conv_2 = Conv2D(36, (5, 5), strides=(2, 2), activation='elu')(conv_1)

conv_3 = Conv2D(48, (5, 5), strides=(2, 2), activation='elu')(conv_2)

conv_4 = Conv2D(64, (3, 3), activation='elu')(conv_3)

conv_5 = Conv2D(128, (3, 3), activation='elu')(conv_4)

drop1 = Dropout(0.2)(conv_5)

pool_1 = MaxPool2D(pool_size=(2,2), strides=(2,2))(drop1)

conv_6 = Conv2D(256, (3, 3), activation='elu')(pool_1)

flat_1 = Flatten()(conv_6)

image_fc = Dense(128, activation='relu')(flat_1)

image_fc_2 = Dense(64, activation='relu')(image_fc)

image_fc_3 = Dense(32, activation='relu')(image_fc_2)

dropca = Dropout(0.25)(image_fc_3)

image_fc_4 = Dense(10, activation='relu')(dropca)

scan_fc = Dense(256, activation='relu')(scan_inputs)

scan_fc2 = Dense(128, activation='relu')(scan_fc)

dropcc = Dropout(0.25)(scan_fc2)

scan_fc3 = Dense(64, activation='relu')(dropcc)

concatenate_layer = concatenate([image_fc_3, scan_fc3])

all_fc = Dense(32, activation='relu')(concatenate_layer)

all_fc2 = Dense(16, activation='relu')(all_fc)

all_fc3 = Dense(8, activation='relu')(all_fc2)

outputs = Dense(1, activation='tanh')(all_fc3)

final_model = Model(inputs=[img_inputs, scan_inputs], outputs=outputs)

final_model.compile(loss='mean_squared_error',
                    optimizer=keras.optimizers.Adam(lr=0.00001), metrics=["accuracy"])

final_model.summary()

# datagen = ImageDataGenerator(featurewise_center=True,
#                                 width_shift_range=0.2,
#                                 height_shift_range=0.2)

# datagen.fit(np_imgs)

# final_model.fit_generator(datagen.flow([np_imgs, np_scan_i], np_cmd_y, batch_size=1),
#                         epochs=15, steps_per_epoch=np_imgs.shape[0],
#                         validation_data=([np_imgs, np_scan_i], np_cmd_y))

final_model.fit([np_imgs, np_scan_i], np_cmd_y, shuffle=True,
                epochs=15, batch_size=1,
                validation_data=([np_imgs, np_scan_i], np_cmd_y))


final_model.save_weights('my_files/my_model.h5')
with open('my_files/my_model.json', 'w') as json_file:
    json_file.write(final_model.to_json())
