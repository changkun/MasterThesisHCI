import json
import random
import numpy as np
from datetime import datetime
now = datetime.now()

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
padding_length = 29
latent_dim = 20
batch_size = 150
epochs = 2000
eos = 0
sos = 1
pad = 2
coi = 3
mis = 4

rand = 0

def get_data():
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):
            sentence = load_a_sentence(user_id, task_id)
            tokenized = [sos] + [vocabs.get(word, mis) for word in sentence][:padding_length-1] + [coi]
            sentences.append(tokenized)
    rand = random.randint(0, len(sentences))
    return sentences[rand:] + sentences[:rand]

def get_data_translate():
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):
            sentence = load_a_sentence(user_id, task_id)
            tokenized = [vocabs.get(word, mis) for word in sentence][padding_length:] + [eos]
            sentences.append(tokenized)
    return sentences[rand:] + sentences[:rand]

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical, normalize
from tensorflow.keras.layers import Input, Dense, Embedding, GRU, TimeDistributed, LSTM
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, TerminateOnNaN
from tensorflow.keras.regularizers import l2


original = pad_sequences(get_data(), value=0, maxlen=50)
translate = pad_sequences(get_data_translate(), value=0, maxlen=50)
trans_onehot = np.array([to_categorical(line, num_classes=num_decoder_tokens) for line in translate])

# original = normalize(original)
# translate = normalize(translate)
# print(original)
# print(translate)

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
try:
    model.load_weights('model.h5')
except OSError:
    pass
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit([original, translate], trans_onehot,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.1,
    shuffle=True,
    callbacks=[
        TensorBoard(log_dir="./logs/" + now.strftime("%Y%m%d-%H%M%S") + "/"),
        TerminateOnNaN(),
        ModelCheckpoint(filepath="model.h5", verbose=1, save_weights_only=True, save_best_only=False, period=3),
        # EarlyStopping(monitor="loss", patience=10),
    ]
)