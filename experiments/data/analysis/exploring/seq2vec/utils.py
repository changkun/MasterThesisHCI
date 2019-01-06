import numpy as np
from sklearn.utils import murmurhash3_32
from sklearn.preprocessing import normalize

def one_host_encode_seq(seq, max_index):
    encoded_seq = []
    for index in seq:
        arr = np.zeros(max_index)
        arr[index] = 1
        encoded_seq.append(arr)
    return encoded_seq

def hash_seq(seq, max_index):
    return [consistent_hash(word) % max_index + 1 for word in seq]

def word2vec_seq(seq, word2vec):
    transformed_seq = []
    word_embedding_size = word2vec.get_size()
    for word in seq:
        try:
            word_arr = word2vec[word]
            new_word_arr = normalize(word_arr.reshape(1, -1), copy=True)
            transformed_seq.append(new_word_arr.reshape(word_embedding_size))
        except KeyError:
            # FIXME: handling
            pass
    return transformed_seq

def consistent_hash(hash_str):
    return murmurhash3_32(hash_str, seed=0)