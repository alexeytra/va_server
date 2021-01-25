import numpy as np
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder


class IntentClassifier:
    def __init__(self, classes, model, tokenizer, label_encoder):
        self.classes = classes
        self.classifier = model
        self.tokenizer = tokenizer
        self.label_encoder = label_encoder

    def get_intent(self, text):
        _text = [text]
        _test_keras = self.tokenizer.texts_to_sequences(_text)
        _test_keras_sequence = pad_sequences(_test_keras, maxlen=7, padding='post')
        _pred = self.classifier.predict(_test_keras_sequence)
        # print(self.pred[0])
        # result_index = np.argmax(_pred, 1)
        # print(self.pred[0][result_index])
        return self.label_encoder.inverse_transform(np.argmax(_pred, 1))[0]
