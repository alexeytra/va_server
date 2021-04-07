import pickle
from keras.models import load_model

# load data for intent classifier
ic_model = load_model('./static/data/intent_classifier/intents.h5')
with open('./static/data/intent_classifier/classes.pkl', 'rb') as file:
    classes = pickle.load(file)
with open('./static/data/intent_classifier/tokenizer.pkl', 'rb') as file:
    ic_tokenizer = pickle.load(file)
with open('./static/data/intent_classifier/label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)
with open('./static/data/intent_classifier/max_len.pkl', 'rb') as f:
    max_len = data_new = pickle.load(f)['max_len']

# load data for seq2seq
seq2seq_model = load_model('./static/data/seq2seq/seq2seq_training_model.h5')
with open('./static/data/seq2seq/seq2seq_tokenizer.pkl', 'rb') as file:
    seq2seq_tokenizer = pickle.load(file)