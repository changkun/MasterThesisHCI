import json
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

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

def difficulty_normalize():
    difficulty = np.array([
        [2, 1, 2, 2, 4, 1, 2, 3, 2],
        [2, 2, 1, 2, 3, 1, 1, 5, 1],
        [3, 2, 2, 2, 5, 3, 3, 1, 3],
        [3, 4, 2, 2, 5, 2, 3, 3, 2],
        [2, 1, 3, 3, 5, 3, 2, 1, 3],
        [2, 2, 1, 3, 4, 1, 1, 3, 2],
        [3, 4, 2, 3, 5, 3, 4, 3, 2],
        [1, 1, 1, 3, 5, 2, 2, 1, 1],
        [2, 3, 2, 2, 5, 2, 3, 1, 1],
        [1, 3, 2, 2, 3, 2, 2, 3, 3],
        [2, 2, 3, 1, 4, 5, 1, 2, 3],
        [3, 2, 1, 3, 4, 1, 3, 2, 2],
        [4, 1, 3, 5, 4, 2, 2, 2, 1],
        [2, 2, 2, 2, 3, 1, 2, 2, 1],
        [5, 1, 3, 2, 4, 1, 4, 2, 3],
        [1, 2, 1, 1, 3, 1, 1, 1, 1],
        [3, 1, 1, 3, 4, 3, 2, 2, 3],
        [2, 2, 1, 2, 3, 1, 3, 2, 2],
        [3, 2, 2, 2, 2, 1, 1, 1, 2],
        [1, 3, 2, 3, 5, 1, 2, 3, 2],
        [3, 3, 2, 3, 5, 4, 2, 3, 5]
    ])
    difficulty_norm = difficulty/difficulty.sum(axis=1)[:,None] # norm
    return difficulty_norm

def plot_length_mult_diff():
    mat_clickstream_length = clickstream_length_normalize()
    mat_task_difficulty = difficulty_normalize()
    Q = np.multiply(mat_clickstream_length, mat_task_difficulty)
    rows = [x for x in range(0, Q.shape[0])]
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    cax = ax.matshow(Q, cmap='RdBu_r')
    fig.colorbar(cax)
    plt.show()

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

import keras
from keras.preprocessing import text

def compute_url_word_sequence():
    clickstream =  load_clickstream(1, 1)
    for obj in clickstream:
        print(text.text_to_word_sequence(obj['current_url']))

# url_map, rate = compute_url_overlap_rate(1)
# print(json.dumps(url_map, sort_keys=True, indent=4))


def compute_url_embedding(task_id):
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

from seq2vec import Seq2VecHash

def compute_url_embedding2(user_id):
    clickstream = load_clickstream(user_id, 1)
    urls = []
    for obj in clickstream:
        urls.append(obj['current_url'])
    transformer = Seq2VecHash(vector_length=30)
    result = transformer.transform(urls)
    return result

from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)

# for user_id in range(1, 22):
#     result = compute_url_embedding2(user_id)


from gensim.models import Word2Vec
