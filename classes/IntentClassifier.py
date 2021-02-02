import numpy as np
from keras.preprocessing.sequence import pad_sequences


class IntentClassifier:
    def __init__(self, classes, model, tokenizer, label_encoder):
        self._classes = classes
        self._classifier = model
        self._tokenizer = tokenizer
        self._label_encoder = label_encoder

    def get_intent(self, text):
        text = [text]
        test_keras = self._tokenizer.texts_to_sequences(text)
        test_keras_sequence = pad_sequences(test_keras, maxlen=7, padding='post')
        pred = self._classifier.predict(test_keras_sequence)
        result_index = np.argmax(pred, 1)
        per_prediction = pred[0][result_index]
        if per_prediction[0] >= .80:
            return self._label_encoder.inverse_transform(np.argmax(pred, 1))[0]
        else:
            return 'unrecognized_question'
