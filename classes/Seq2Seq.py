from keras.models import Model, Input
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import re


class Seq2SeqModel:
    def __init__(self, model, tokenizer, max_len_questions):
        self._model = model
        self._tokenizer = tokenizer
        self._max_len_questions = max_len_questions
        self._encoder_model, self._decoder_model = self._make_inference_models()

    def _str_to_tokens(self, sentence: str):
        words = self._clean_text(sentence).lower().split()
        return pad_sequences(self._tokenizer.texts_to_sequences([words]), maxlen=self._max_len_questions,
                             padding='post')

    def _clean_text(self, sentence: str):
        sentence = sentence.lower()
        sentence = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", sentence)
        return sentence

    def _make_inference_models(self):
        encoder_inputs = self._model.input[0]
        encoder_embedding = self._model.layers[2](encoder_inputs)
        encoder_outputs, state_h_enc, state_c_enc = self._model.layers[4](encoder_embedding)
        encoder_states = [state_h_enc, state_c_enc]

        encoder_model = Model(encoder_inputs, encoder_states)

        decoder_inputs = self._model.input[1]
        decoder_state_input_h = Input(shape=(200,), name='decoderStateInput_h')
        decoder_state_input_c = Input(shape=(200,), name='decoderStateInput_c')

        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        decoder_embedding = self._model.layers[3](decoder_inputs)
        decoder_LSTM = self._model.layers[5]
        decoder_outputs, state_h_dec, state_c_dec = decoder_LSTM(decoder_embedding, initial_state=decoder_states_inputs)
        decoder_states = [state_h_dec, state_c_dec]
        decoder_dense = self._model.layers[6]
        decoder_outputs = decoder_dense(decoder_outputs)

        decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)

        return encoder_model, decoder_model

    def get_answer(self, sentence: str):
        states_values = self._encoder_model.predict(self._str_to_tokens(sentence))
        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = self._tokenizer.word_index['start']
        stop_condition = False
        decoded_translation = ''
        while not stop_condition:
            dec_outputs, h, c = self._decoder_model.predict([empty_target_seq] + states_values)
            sampled_word_index = np.argmax(dec_outputs[0, 0, :])

            word = self._tokenizer.index_word[sampled_word_index]
            if word == 'end' or len(decoded_translation.split()) > 21:
                stop_condition = True
            else:
                decoded_translation += ' {}'.format(word)

            empty_target_seq = np.zeros((1, 1))
            empty_target_seq[0, 0] = sampled_word_index
            states_values = [h, c]
        decoded_translation = decoded_translation.strip().capitalize()
        return decoded_translation
