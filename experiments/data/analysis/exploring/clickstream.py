import json
import numpy as np
import keras
from keras.preprocessing import text
from seq2vec import Seq2VecHash, Seq2Seq

def load_clickstream_length():
    data = np.zeros((21, 9))
    for i in range(1, 22):
        with open(f'./dataset/{i}.json') as f:
            d = json.load(f)
            for j in range(0, len(d)):
                length = len(d[j]['clickstream'])
                data[i-1][j] = length
    return data

def load_clickstream(user_id, task_id):
    with open(f'./dataset/{user_id}.json') as f:
        return json.load(f)[task_id]['clickstream']

def clickstream_length_normalize():
    mat_length = load_clickstream_length()
    mat_length = mat_length / mat_length.sum(axis=1)[:, None]
    return mat_length

def compute_url_overlap_rate(task_id):
    count = 0
    url_map = dict()
    for user_id in range(1, 22):
        clickstream = load_clickstream(user_id, task_id)
        for obj in clickstream:
            count += 1
            key = obj['current_url']
            if key not in url_map:
                url_map[key] = 1
                continue
            url_map[key] += 1
    return url_map, len(url_map) / count

def compute_url_overlap_rate_all():
    for task_id in range(0, 9):
        _, rate = compute_url_overlap_rate(task_id)
        print(f'task {task_id} clickstream overlap rate: ', 1 - rate)



def compute_url_word_sequence():
    clickstream =  load_clickstream(1, 1)
    for obj in clickstream:
        print(text.text_to_word_sequence(obj['current_url']))

# url_map, rate = compute_url_overlap_rate(1)
# print(json.dumps(url_map, sort_keys=True, indent=4))


def compute_url_mapping(task_id):
    total = {}
    for user_id in range(1, 22):
        clickstream = load_clickstream(user_id, task_id)
        for obj in clickstream:
            previous = obj['previous_url']
            if previous in total:
                current = obj['current_url']
                if current in total[previous]:
                    total[previous][current] += 1
                else:
                    total[previous][current] = 1
            else:
                total[previous] = {}
    with open(f'embeddings/{task_id}.json', 'w+') as f:
        f.write(json.dumps(total, indent=4))

# for task_id in range(0, 9):
#     compute_url_embedding(task_id)




vec_len = 30

def compute_url_embedding(user_id, task_id):
    clickstream = load_clickstream(user_id, task_id)
    urls = []
    for obj in clickstream:
        urls.append(obj['previous_url'])
    transformer = Seq2VecHash(vec_len=vec_len)
    result = transformer(urls)
    print('clickstream: ', result)
    return result

def main():
    sos = np.zeros((1, vec_len))
    coi = np.zeros((1, vec_len)) - 1
    eos = np.zeros((1, vec_len)) - 10
    pad = np.zeros((1, vec_len)) - 100

    max_length = 0
    sentences = []
    for user_id in range(1, 22):
        for task_id in range(0, 9):

            clickstream = compute_url_embedding(user_id, task_id)
            pos = clickstream.shape[0]//2

            clickstream = np.insert(clickstream, pos, coi, 0)
            clickstream = np.insert(clickstream, 0, sos, 0)
            clickstream = np.insert(clickstream, clickstream.shape[0], eos, 0)

            length_sentence = clickstream.shape[0]
            if length_sentence > max_length:
                max_length = length_sentence
            
            sentences.append(clickstream)

    print('max_y:', max_length)

    for idx, sentence in enumerate(sentences):
        padnum = max_length - sentence.shape[0] + 1
        pads = np.repeat(pad, padnum, axis=0)
        sentences[idx] = np.concatenate((sentence, pads), axis=0)

    sentences = np.stack(sentences)
    print(sentences.shape)

    # model = Seq2Seq(output_dim=xx.shape[2], hidden_dim=42, output_length=xx.shape[2], input_shape=(xx.shape[1], xx.shape[2]), peek=True, depth=2, teacher_force=True)
    # model.compile(loss='mse', optimizer='rmsprop')
    # model.fit([xx, yy], yy, epochs=1)

if __name__ == "__main__":
    main()

