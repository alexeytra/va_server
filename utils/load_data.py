import pickle
from keras.models import load_model

model = load_model('./static/models/intents.h5')

with open('./static/data/classes.pkl', 'rb') as file:
    classes = pickle.load(file)

with open('./static/data/tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

with open('./static/data/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)
