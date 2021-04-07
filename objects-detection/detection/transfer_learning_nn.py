import math
import time
import os
import traceback

import numpy as np
from keras import applications
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.utils.np_utils import to_categorical

IMG_SIZE = (348, 348)

INIT_MODEL_WEIGHTS_PATH = 'initial_model.h5'
INIT_MODEL_TRAIN_FEATURES_PATH = 'bottleneck_features_train.npy'
INIT_MODEL_VALIDATION_FEATURES_PATH = 'bottleneck_features_validation.npy'
CLASS_INDICES_PATH = 'class_indices.npy'
TRAIN_DATASET_DIR = './ref-data/dataset/train'
VALIDATION_DATASET_DIR = './ref-data/dataset/validation'

EPOCHS_NUM = 2

BATCH_SIZE = 16


def prepare_model_for_transfer():
    vgg16 = applications.VGG16(include_top=False,
                               weights='imagenet')

    data_gen = ImageDataGenerator(rescale=1. / 255)

    generator = data_gen.flow_from_directory(TRAIN_DATASET_DIR,
                                             target_size=IMG_SIZE,
                                             batch_size=BATCH_SIZE,
                                             class_mode=None,
                                             shuffle=False)

    predict_size_train = int(math.ceil(len(generator.filenames) / BATCH_SIZE))

    init_model_train = vgg16.predict_generator(generator, predict_size_train)
    np.save(INIT_MODEL_TRAIN_FEATURES_PATH, init_model_train)

    generator = data_gen.flow_from_directory(VALIDATION_DATASET_DIR,
                                             target_size=(IMG_SIZE),
                                             batch_size=BATCH_SIZE,
                                             class_mode=None,
                                             shuffle=False)

    predict_size_validation = int(
        math.ceil(len(generator.filenames) / BATCH_SIZE))

    bottleneck_features_validation = vgg16.predict_generator(generator, predict_size_validation)

    np.save(INIT_MODEL_VALIDATION_FEATURES_PATH, bottleneck_features_validation)


def train_transfer_model():
    data_gen = ImageDataGenerator(rescale=1. / 255)
    generator = data_gen.flow_from_directory(TRAIN_DATASET_DIR,
                                             target_size=IMG_SIZE,
                                             batch_size=BATCH_SIZE,
                                             class_mode='categorical',
                                             shuffle=False)

    np.save(CLASS_INDICES_PATH, generator.class_indices)

    train_data = np.load(INIT_MODEL_TRAIN_FEATURES_PATH, allow_pickle=True)
    train_labels = to_categorical(generator.classes, num_classes=len(generator.class_indices))

    generator = data_gen.flow_from_directory(VALIDATION_DATASET_DIR,
                                             target_size=IMG_SIZE,
                                             batch_size=BATCH_SIZE,
                                             class_mode='categorical',
                                             shuffle=False)

    validation_data = np.load(INIT_MODEL_VALIDATION_FEATURES_PATH, allow_pickle=True)
    validation_labels = to_categorical(generator.classes, num_classes=len(generator.class_indices))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(generator.class_indices), activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['acc'])

    model.fit(train_data, train_labels,
              epochs=EPOCHS_NUM,
              batch_size=BATCH_SIZE,
              validation_data=(validation_data, validation_labels))

    model.save_weights(INIT_MODEL_WEIGHTS_PATH)

    (eval_loss, eval_accuracy) = model.evaluate(validation_data, validation_labels,
                                                batch_size=BATCH_SIZE,
                                                verbose=1)

    print("[INFO] accuracy: {:.2f}%".format(eval_accuracy * 100))
    print("[INFO] Loss: {}".format(eval_loss))


def predict(image_path):
    class_dictionary = np.load('class_indices.npy', allow_pickle=True).item()

    num_classes = len(class_dictionary)

    # todo: add image cropping
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
    print("[INFO] Predictions for classes: {}".format(probabilities))

    reversed_cls_dict = {value: key for key, value in class_dictionary.items()}
    label = reversed_cls_dict[class_predicted[0]]
    print("[INFO] Image: {}, Label: {}".format(image_path, label))
    return label


def poll_directory(polling_path, results_path, on_new_file):
    managed_files = set()
    total_slept_time = 0
    while True:
        try:
            for file_path in os.listdir(polling_path):
                initial_data_path = polling_path + os.sep + file_path
                if initial_data_path not in managed_files and os.path.isfile(initial_data_path):
                    print("[INFO]: New file fetched for processing: [{}]".format(initial_data_path))
                    managed_files.add(initial_data_path)

                    label = on_new_file(initial_data_path)
                    result_data_path = results_path + os.sep + os.path.splitext(file_path)[0] + '_label.txt'
                    with(open(result_data_path, 'w')) as result_file:
                        result_file.write(label)
                    print("[INFO]: Saved processing results to [{}]".format(result_data_path))

            time.sleep(5)
            total_slept_time += 5

            if total_slept_time % 30 == 0:
                for file_path in managed_files:
                    os.remove(file_path)
                    del file_path
        except Exception as e:
            print("[ERROR]: Encountered following error while performing prediction: [{}]".format(e))


if __name__ == '__main__':
    print("[INFO]: Model started!")

    if not os.path.exists(INIT_MODEL_WEIGHTS_PATH):
        print("[INFO]: Model fitting started!")
        prepare_model_for_transfer()
        train_transfer_model()
        print("[INFO]: Model fitting finished!")
    else:
        print("[INFO]: Model data already exists!")

    print("[INFO]: Started polling service!")
    poll_directory('ref-data/sample_images',
                   'ref-data/sample_results',
                   lambda path: predict(path))
