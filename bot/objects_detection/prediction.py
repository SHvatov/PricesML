import logging
import pathlib
import numpy as np
import os
import tensorflow as tf
from keras import applications
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from keras.preprocessing.image import img_to_array, load_img

from objects_detection.cropping import crop_image
from cfg.config import (IMG_SIZE, INIT_MODEL_WEIGHTS_PATH, CLASS_INDICES_PATH)

logger = logging.getLogger(__name__)
CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
INIT_MODEL_WEIGHTS_PATH = os.path.join(CURRENT_DIR, INIT_MODEL_WEIGHTS_PATH)
CLASS_INDICES_PATH = os.path.join(CURRENT_DIR, CLASS_INDICES_PATH)


def predict(image_path):
    class_dictionary = np.load(CLASS_INDICES_PATH, allow_pickle=True).item()

    num_classes = len(class_dictionary)

    crop_image(image_path)

    image = load_img(image_path, target_size=IMG_SIZE)
    image = img_to_array(image)

    image = image / 255
    image = np.expand_dims(image, axis=0)

    model = applications.VGG16(include_top=False, weights='imagenet')
    initial_model_prediction = model.predict(image)

    model = Sequential()
    model.add(Flatten(input_shape=initial_model_prediction.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='sigmoid'))

    model.load_weights(INIT_MODEL_WEIGHTS_PATH)

    class_predicted = model.predict_classes(initial_model_prediction)
    probabilities = model.predict_proba(initial_model_prediction)
    logger.info(f'Predictions for classes: {probabilities}')

    reversed_cls_dict = {value: key for key, value in class_dictionary.items()}
    label = reversed_cls_dict[class_predicted[0]]
    logger.info(f'Image: {image_path}, Label: {label}')

    return label
