from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow_addons.text import CRFModelWrapper

import numpy as np


class MyBiLSTMCRF:

    def __init__(self, chars_vocabSize, words_vocabSize, tagIndexDict, tagSum, sequence_lengths, batchSize):
        self.chars_vocabSize = chars_vocabSize
        self.words_vocabSize = words_vocabSize
        self.tagSum = tagSum
        self.sequence_lengths = sequence_lengths
        self.tagIndexDict = tagIndexDict
        self.vecSize = 100  # 字 的向量dimension
        self.segSize = 20  # 词 的向量dimension
        self.batchSize = batchSize
        self.baseModel = None
        self.myBiLSTMCRF = None

        self.buildBiLSTMCRF()

    def buildBiLSTMCRF(self):

        input_1 = Input(shape=(self.sequence_lengths,), name='chars')
        input_2 = Input(shape=(self.sequence_lengths,), name='words')

        # 加一操作 是要将pad过程的词token加入的词表中
        embed_1 = Embedding(input_dim=self.chars_vocabSize + 1, output_dim=self.vecSize, name='embed_1')(input_1)
        embed_2 = Embedding(input_dim=self.words_vocabSize + 1, output_dim=self.segSize, name='embed_2')(input_2)

        concate = Concatenate(name='concate')([embed_1, embed_2])

        lstm_1 = Bidirectional(LSTM(units=self.tagSum, activation='tanh'), merge_mode='sum', name='BiLSTM_1')(concate)
        lstm_2 = Bidirectional(LSTM(units=self.tagSum, activation='softmax'), merge_mode='sum', name='BiLSTM_2')(lstm_1)

        self.baseModel = Model(inputs=[input_1, input_2], ouputs=lstm_2, name='base_model')

        crf = CRFModelWrapper(self.baseModel, units=self.tagSum, name='crf')

        crf.compile(optimizer=Adam(3e-5))
        crf.build([(self.batchSize, self.sequence_lengths), (self.batchSize, self.sequence_lengths)])

        self.baseModel.summary()
        crf.summary()
        self.myBiLSTMCRF = crf

    def fit(self, X, y, epochs=30):
        log_dir = "logs"
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        history = self.myBiLSTMCRF.fit(X, y, validation_split=0.1, batch_size=self.batchSize, epochs=epochs, callbacks=[tensorboard_callback])

        return history

    def predict(self, X):
        preYArr = self.myBiLSTMCRF.predict(X)
        return preYArr


if __name__ == "__main__":
    tag2id = {'o': 0,
              'B_ns': 1,
              'B_nr': 2,
              'B_nt': 3,
              'I_nt': 4,
              'I_nr': 5,
              'I_ns': 6,
              }


