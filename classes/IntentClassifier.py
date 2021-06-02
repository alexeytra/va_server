import numpy as np
from keras.preprocessing.sequence import pad_sequences


class IntentClassifier:
    def __init__(self, classes, model, tokenizer, label_encoder, max_len):
        self.__classes = classes
        self.__classifier = model
        self.__tokenizer = tokenizer
        self.__label_encoder = label_encoder
        self.__accuracy = 0.0
        self.__max_len = max_len

    def get_intent(self, text):
        text = [text]
        test_keras = self.__tokenizer.texts_to_sequences(text)
        test_keras_sequence = pad_sequences(test_keras, maxlen=self.__max_len, padding='post')
        pred = self.__classifier.predict(test_keras_sequence)
        result_index = np.argmax(pred, 1)
        per_prediction = pred[0][result_index]
        self.__accuracy = per_prediction[0]
        if per_prediction[0] >= .84:
            return self.__label_encoder.inverse_transform(np.argmax(pred, 1))[0]
        else:
            return 'unrecognized_question'

    @property
    def accuracy(self):
        return self.__accuracy
