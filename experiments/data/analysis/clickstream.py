import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    return len(url_map) / count

for task_id in range(0, 9):
    print(f'task {task_id} clickstream overlap rate: ', 1 - compute_url_overlap_rate(task_id))