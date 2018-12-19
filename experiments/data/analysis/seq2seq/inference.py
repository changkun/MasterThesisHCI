import json
import numpy as np
from datetime import datetime

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical, normalize
from tensorflow.keras.layers import Input, Dense, Embedding, GRU, TimeDistributed, LSTM
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, TerminateOnNaN
from tensorflow.keras.regularizers import l2

def build_model(load_old = False):
    encoder_inputs = Input(shape=(None,), name="EncoderInput_1")
    embedded_encoder_inputs = Embedding(num_encoder_tokens, latent_dim, mask_zero=True)(encoder_inputs)
    encoder = GRU(latent_dim, return_state=True)
    _, state_h = encoder(embedded_encoder_inputs)
    # we discard `encoder_outputs` and only keep the states.
    encoder_states = state_h

    decoder_inputs = Input(shape=(None,), name="DecoderInput_1")
    embedded_decoder_inputs = Embedding(num_encoder_tokens, latent_dim, mask_zero=True)(decoder_inputs)
    decoder_lstm = GRU(latent_dim, return_sequences=True, return_state=True, kernel_regularizer=l2(0.0000001), activity_regularizer=l2(0.0000001))
    x, _ = decoder_lstm(embedded_decoder_inputs, initial_state=encoder_states)
    decoder_dense = TimeDistributed(Dense(num_decoder_tokens, activation='softmax'))
    decoder_outputs = decoder_dense(x)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    if load_old:
        try:
            model.load_weights(f'model-{now.strftime("%Y%m%d-%H%M%S")}.h5')
        except OSError:
            pass
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model