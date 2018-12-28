import json, sys
import numpy as np
from datetime import datetime

import tensorflow as tf
from tf.keras.preprocessing.sequence import pad_sequences
from tf.keras.utils import to_categorical, normalize
from tf.keras.layers import Input, Dense, Embedding, GRU, TimeDistributed, LSTM
from tf.keras.models import Model
from tf.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, TerminateOnNaN
from tf.keras.regularizers import l2

def load_clickstream(user_id, task_id):
    with open(f'../dataset/{user_id}.json') as f:
        return json.load(f)[task_id]['clickstream']

def load_a_sentence(user_id, task_id):
    clickstream = load_clickstream(user_id, task_id)
    urls = []
    for obj in clickstream:
        urls.append(obj['previous_url'])
    return urls

def generate_vocabs():
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):
            sentence = load_a_sentence(user_id, task_id)
            sentences += sentence
    sentences += ['<SOS>', '<EOS>', '<COI>', '<PAD>', '<MIS>']
    vocabs = list(set(sentences))
    with open('vocabs.txt', 'w+') as f:
        f.writelines('\n'.join(vocabs))

def load_vocabs():
    vocabs = {}
    with open('vocabs.txt', 'r') as f:
        for idx, line in enumerate(f):
            vocabs[line.strip()] = idx
    return vocabs

vocabs = load_vocabs()
id_vocab = {value: key for key, value in vocabs.items()}
num_encoder_tokens = len(vocabs)
num_decoder_tokens = len(vocabs)
max_total = 30
max_origin = 20
max_translate = max_total - max_origin
latent_dim = 20
batch_size = 32
epochs = 2000
eos = 0
sos = 1
pad = 2
coi = 3
mis = 4

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
            model.load_weights(f'model.h5')
        except OSError:
            print('cannot find model.h5')
            sys.exit(2)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

original = pad_sequences(get_data(), value=0, maxlen=max_origin)
translate = pad_sequences(get_data_translate(), value=0, maxlen=max_translate)
trans_onehot = np.array([to_categorical(line, num_classes=num_decoder_tokens) for line in translate])

model = build_model(load_old=True)
model.evaluate()