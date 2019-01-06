import json
import numpy as np
from datetime import datetime

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical, normalize, plot_model
from tensorflow.keras.layers import Input, Dense, Embedding, GRU, TimeDistributed, LSTM
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, TerminateOnNaN
from tensorflow.keras.regularizers import l2

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
max_total = 30
max_origin = 20
max_translate = max_total - max_origin + 1
latent_dim = 20
batch_size = 32
epochs = 500
eos = 0
sos = 1
pad = 2
coi = 3
mis = 4

def get_data():
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):
            sentence = load_a_sentence(user_id, task_id)
            tokenized = [sos] + [vocabs.get(word, mis) for word in sentence][:max_origin] + [coi]
            sentences.append(tokenized)
    return sentences

def get_data_translate():
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):
            sentence = load_a_sentence(user_id, task_id)
            tokenized = [sos] + [vocabs.get(word, mis) for word in sentence][max_origin:max_total] + [eos]
            sentences.append(tokenized)
    return sentences

original = pad_sequences(get_data(), value=0, maxlen=max_origin, padding='pre')
translate = pad_sequences(get_data_translate(), value=0, maxlen=max_translate, padding='post')
trans_onehot = np.array([to_categorical(line, num_classes=num_decoder_tokens) for line in translate])

print('original: ', original)
print('shape: ', original.shape)
print('translate: ', translate)
print('shape: ', translate.shape)


def build_model(load_old = True):
    encoder_inputs = Input(shape=(None,), name="EncoderInput_1")
    embedded_encoder_inputs = Embedding(num_encoder_tokens, latent_dim, mask_zero=True)(encoder_inputs)
    encoder = GRU(latent_dim, return_state=True)
    _, state_h = encoder(embedded_encoder_inputs)
    # we discard `encoder_outputs` and only keep the states.
    encoder_states = state_h

    decoder_inputs = Input(shape=(None,), name="DecoderInput_1")
    embedded_decoder_inputs = Embedding(num_encoder_tokens, latent_dim, mask_zero=True)(decoder_inputs)
    decoder_gru = GRU(latent_dim, return_sequences=True, return_state=True, kernel_regularizer=l2(0.0000001), activity_regularizer=l2(0.0000001))
    x, _ = decoder_gru(embedded_decoder_inputs, initial_state=encoder_states)
    decoder_dense = TimeDistributed(Dense(num_decoder_tokens, activation='softmax'))
    decoder_outputs = decoder_dense(x)

    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
    if load_old:
        model.load_weights('model.h5')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    encoder_model = Model(encoder_inputs, encoder_states)
    decoder_state_input_h = Input(shape=(None,), name="DecoderStateInput_1")
    decoder_outputs, decoder_state_h = decoder_gru(embedded_decoder_inputs, initial_state=decoder_state_input_h)
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = Model([decoder_inputs] + [decoder_state_input_h], [decoder_outputs] + [decoder_state_h])
    return model, encoder_model, decoder_model


load_old = True
model, encoder, decoder = build_model(load_old=load_old)

print(original)
if not load_old:
    model.fit([original, translate], trans_onehot,
        batch_size=batch_size,
        epochs=epochs,
        # validation_split=0.1,
        shuffle=True,
        callbacks=[
            TensorBoard(log_dir=f'./logs/{now.strftime("%Y%m%d-%H%M%S")}/'),
            TerminateOnNaN(),
            ModelCheckpoint(filepath=f'model.h5', verbose=1, save_weights_only=True, save_best_only=False, period=3),
            # EarlyStopping(monitor="loss", patience=10),
        ]
    )

score = model.evaluate([original, translate], trans_onehot)
print('accuracy: ', score[1])

def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1))
    current_step = 0
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0] = vocabs["<SOS>"]

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    decoded_sentence = []

    while True:
        output_tokens, h = decoder.predict([target_seq] + [states_value])
        current_step += 1
        print('output_token: ', output_tokens.shape)
        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])

        predicted_url = id_vocab[sampled_token_index]
        decoded_sentence.append(predicted_url)

        # Exit condition: either hit max length
        # or find stop character.
        if len(decoded_sentence) > max_translate:
            break

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index

        # Update states
        states_value = h
    return decoded_sentence

for idx in range(2):
    input_seq = original[idx:idx+1]
    print('input seq: ', input_seq)
    output_seq = decode_sequence(input_seq)
    print('\n')
    print(output_seq)