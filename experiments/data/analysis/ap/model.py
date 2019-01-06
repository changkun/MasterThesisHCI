
import json
import numpy as np
import matplotlib.pyplot as plt
import keras
from datetime import datetime
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical, normalize, plot_model
from keras.layers import Input, Dense, Embedding, GRU, TimeDistributed, LSTM
from keras.models import Model
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, TerminateOnNaN
from keras.regularizers import l2
from IPython.display import clear_output

now = datetime.now()

class PlotLosses(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.fig = plt.figure()
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1
        
    def on_train_end(self, logs=None):
        # plt.plot(self.x, self.losses, label="training loss")
        plt.plot(self.x, self.val_losses, label="validation loss")
        # plt.legend()
        plt.xlabel('training epochs')
        plt.ylabel('categorical crossentropy validation loss')
        plt.savefig(f'save-{now.strftime("%Y%m%d-%H%M%S")}.png')
        
plot_losses = PlotLosses()

# userid 1~21 taskid 1~9
def load_clickstream(user_id, task_id):
    with open(f'../dataset/{user_id}.json') as f:
        return json.load(f)[task_id-1]['clickstream']

def load_a_sentence(user_id, task_id):
    clickstream = load_clickstream(user_id, task_id)
    urls = []
    durations = []
    for obj in clickstream:
        urls.append(obj['previous_url'])
        durations.append(obj['stay_seconds'])
    return urls, (task_id-1)%3, durations

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

# hyperparams
latent_dim = 10
split_ratio = 0.99
batch_size = 32
epochs = 1500


# Layer (type)                    Output Shape         Param #     Connected to
# ==================================================================================================
# ContextEncoderInputRaw (InputLa (None, None)         0
# __________________________________________________________________________________________________
# ContextDecoderInputRaw (InputLa (None, None)         0
# __________________________________________________________________________________________________
# embedding_1 (Embedding)         (None, None, 10)     28730       ContextEncoderInputRaw[0][0]
# __________________________________________________________________________________________________
# embedding_2 (Embedding)         (None, None, 10)     28730       ContextDecoderInputRaw[0][0]
# __________________________________________________________________________________________________
# gru_1 (GRU)                     [(None, 10), (None,  630         embedding_1[0][0]
# __________________________________________________________________________________________________
# gru_2 (GRU)                     [(None, None, 10), ( 630         embedding_2[0][0]
#                                                                  gru_1[0][1]
# __________________________________________________________________________________________________
# time_distributed_1 (TimeDistrib (None, None, 2873)   31603       gru_2[0][0]
# ==================================================================================================
# Total params: 90,323
# Trainable params: 90,323
# Non-trainable params: 0
# __________________________________________________________________________________________________
#
# split_ratio:  val_acc   acc   test_acc
#        0.05,: 0.3644, 0.4147, 0.1698,
#        0.10,: 0.3138, 0.3505, 0.1292,
#        0.15,: 0.3315, 0.3717, 0.1416,
#        0.20,: 0.3272, 0.3692, 0.1415,
#        0.25,: 0.3845, 0.4426, 0.1211,
#        0.30,: 0.3567, 0.3956, 0.1690,
#        0.35,: 0.3879, 0.4343, 0.1713,
#        0.40,: 0.3019, 0.3483, 0.0890,
#        0.45,: 0.3725, 0.4257, 0.1427,
#        0.50,: 0.3407, 0.3891, 0.1165,
#        0.55,: 0.3809, 0.4271, 0.1680,
#        0.60,: 0.4178, 0.4685, 0.1904,
#        0.65,: 0.3960, 0.4540, 0.1450,
#        0.70,: 0.4543, 0.5130, 0.2015,
#        0.75,: 0.4906, 0.5602, 0.1707,
#        0.80,: 0.5549, 0.6307, 0.2227,
#        0.85,: 0.5445, 0.5994, 0.2927,
#        0.90,: 0.6257, 0.7012, 0.2794,
#        0.95,: 0.6783, 0.9253, 0.4459,
#        0.96,: 0.6121, 0.6363, 0.4948,
#        0.97,: 0.7298, 0.7739, 0.5234, i.e. max-3-step future
#        0.98,: 0.7248, 0.7616, 0.5526,
#        0.99,: 0.9947, 1.0000, 0.9737, i.e. 3-class-classification 


# special tokens
pad = 0
soa = 1
coi = 2
sop = 3
eoa_goal    = 4
eoa_fuzzy   = 5
eoa_explore = 6
mis = 7

# consts about data
max_length = 0
min_length = 100000
def get_data():
    input_sentences  = []
    output_sentences = []
    input_durations  = []
    output_durations = []
    for user_id in range(1, 22):
        for task_id in range(1, 10):
            sentence, task_type, duration = load_a_sentence(user_id, task_id)
            global max_length
            global min_length
            if len(sentence) > max_length:
                max_length = len(sentence)
            if len(sentence) < min_length:
                min_length = len(sentence)
            training_lenth = int(len(sentence) * split_ratio)

            input_sentence = sentence[:training_lenth]
            input_duration = duration[:training_lenth]
            output_sentence = sentence[training_lenth:]
            output_duration = duration[training_lenth:]

            input_durations.append(input_duration)
            output_durations.append(output_duration)

            if task_type == 0:
                tokenized_input  = [soa] + [vocabs.get(word, mis) for word in input_sentence] + [coi]
                tokenized_output = [vocabs.get(word, mis) for word in output_sentence] + [eoa_goal]
            elif task_type == 1:
                tokenized_input  = [soa] + [vocabs.get(word, mis) for word in input_sentence] + [coi]
                tokenized_output = [vocabs.get(word, mis) for word in output_sentence] + [eoa_fuzzy]
            elif task_type == 2:
                tokenized_input  = [soa] + [vocabs.get(word, mis) for word in input_sentence]
                tokenized_output = [vocabs.get(word, mis) for word in output_sentence] + [eoa_explore]

            input_sentences.append(tokenized_input)
            output_sentences.append(tokenized_output)
    
    return input_sentences, input_durations, output_sentences, output_durations


input_s, input_d, output_s, output_d = get_data()
input_s = pad_sequences(input_s, value = pad, maxlen=int(max_length*split_ratio))
input_d = pad_sequences(input_d, value = 1, maxlen=int(max_length*split_ratio))
# input_s = np.multiply(input_s, input_d)

output_s = pad_sequences(output_s, value = pad, maxlen=max_length - int(max_length*(split_ratio)), padding='post')
# output_s = np.concatenate((np.ones((output_s.shape[0], 1)) * sop, output_s), axis=1)

output_s_one_shot = np.array([to_categorical(line, num_classes=num_decoder_tokens) for line in output_s])
output_d = pad_sequences(output_d, value = 0, maxlen=max_length - int(max_length*(split_ratio)), padding='post')
# print(input_s, input_d, output_s, output_d)
print(input_s.shape, input_d.shape, output_s.shape, output_d.shape)
print('input sentence size: ', int(max_length*split_ratio))
print('output sentence size: ', int(max_length*(1-split_ratio)))
print('example input:', input_s[0])
print('example output:', output_s[0])

def build_model(load_old = False):
    encoder_input = Input(shape=(None,), name='ContextEncoderInputRaw')
    embedded_encoder_input = Embedding(num_encoder_tokens, latent_dim, mask_zero=True)(encoder_input)
    encoder = GRU(latent_dim, return_state=True)
    _, hidden_state = encoder(embedded_encoder_input)
    context_state = hidden_state

    decoder_input = Input(shape=(None,), name='ContextDecoderInputRaw')
    embedded_decoder_input = Embedding(num_encoder_tokens, latent_dim, mask_zero=True)(decoder_input)
    decoder = GRU(latent_dim, return_sequences=True, return_state=True, kernel_regularizer=l2(0.0000001), activity_regularizer=l2(0.0000001))
    x, _ = decoder(embedded_decoder_input, initial_state=context_state)
    decoder_dense = TimeDistributed(Dense(num_decoder_tokens, activation='softmax'))
    decoder_outputs = decoder_dense(x)

    model = Model([encoder_input, decoder_input], decoder_outputs)
    if load_old:
        model.load_weights('model.h5')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    encoder_model = Model(encoder_input, context_state)
    decoder_state_input_h = Input(shape=(None,), name='ContextDecoderInput')
    decoder_outputs, decoder_state_h = decoder(embedded_decoder_input, initial_state=decoder_state_input_h)
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = Model([decoder_input] + [decoder_state_input_h], [decoder_outputs] + [decoder_state_h])
    return model, encoder_model, decoder_model

load_old = False
model, encoder, decoder = build_model(load_old=load_old)
model.summary()

history = None
train_ratio = 0.92
if not load_old:
    history = model.fit([input_s[:int(input_s.shape[0]*train_ratio)], output_s[:int(output_s.shape[0]*train_ratio)]], output_s_one_shot[:int(output_s_one_shot.shape[0]*train_ratio)], batch_size=batch_size, 
            epochs=epochs,
            validation_split=0.2,
            shuffle=True,
            callbacks=[
                TensorBoard(log_dir=f'./logs/{now.strftime("%Y%m%d-%H%M%S")}/'),
                TerminateOnNaN(),
                ModelCheckpoint(filepath=f'model-{now.strftime("%Y%m%d-%H%M%S")}.h5', verbose=1, save_weights_only=True, save_best_only=True, period=3),
                EarlyStopping(monitor="val_loss", patience=epochs),
                plot_losses,
            ])
# test
score = model.evaluate([input_s[int(input_s.shape[0]*train_ratio):], output_s[int(output_s.shape[0]*train_ratio):]], output_s_one_shot[int(output_s_one_shot.shape[0]*train_ratio):])
print('accuracy: ', score[1])

def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder.predict(input_seq)

    print('context: ', states_value)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0] = sop

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    decoded_sentence = []

    while True:
        output_tokens, h = decoder.predict([target_seq] + [states_value])
        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        # print('output_token: ', sampled_token_index)

        predicted_url = id_vocab[sampled_token_index]
        decoded_sentence.append(predicted_url)

        # Exit condition: either hit max length
        # or find stop character.
        if len(decoded_sentence) > max_length - int(max_length*(split_ratio)) + 1:
            break

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index

        # Update states
        states_value = h
    return decoded_sentence

def search(decoder, src_input, k=1, sequence_max_len=25):
    # (log(1), initialize_of_zeros)
    k_beam = [(0, [0]*(sequence_max_len+1))]

    # l : point on target sentence to predict
    for l in range(sequence_max_len):
        all_k_beams = []
        for prob, sent_predict in k_beam:
            predicted = decoder.predict([np.array([src_input]), np.array([sent_predict])])[0]
            # top k!
            possible_k = predicted[l].argsort()[-k:][::-1]

            # add to all possible candidates for k-beams
            all_k_beams += [
                (
                    sum(np.log(predicted[i][sent_predict[i+1]]) for i in range(l)) + np.log(predicted[l][next_wid]),
                    list(sent_predict[:l+1])+[next_wid]+[0]*(sequence_max_len-l-1)
                )
                for next_wid in possible_k
            ]

        # top k
        k_beam = sorted(all_k_beams)[-k:]

    return k_beam[-1:]

if load_old:
    for input_seq in input_s:
        output_seq = decode_sequence(input_seq)
        print('argmax result: ', output_seq)


    for input_seq in input_s:
        k_beam = search(model, input_seq, k=5, sequence_max_len=30)
        print('beam result: ', k_beam)