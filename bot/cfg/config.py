import os

TOKEN = os.environ.get('BOT_TOKEN', '')
API_URL = os.environ.get('API_URL', 'http://api:8080/')
API_ENDPOINT = 'data'

IMG_SIZE = (348, 348)
INIT_MODEL_WEIGHTS_PATH = 'data/initial_model.h5'
CLASS_INDICES_PATH = 'data/class_indices.npy'
