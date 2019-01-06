import numpy as np

def _padding_array(seqs, from_post, max_len, default):
    seqs_len = len(seqs)
    if seqs_len == max_len:
        return seqs

    if seqs_len > max_len:
        if from_post:
            return seqs[0:max_len]
        start = seqs_len - max_len
        return seqs[start:]

    append_times = max_len - seqs_len
    if from_post:
        list_to_be_append = seqs
    else:
        list_to_be_append = seqs[::-1]

    for _ in range(append_times):
        list_to_be_append.append(default)
    
    if from_post:
        return list_to_be_append
    return list_to_be_append[::-1]

def generate_padding_array(seqs, transform_func, default, max_len, inverse=False):
    transformed_seqs = []
    for seq in seqs:
        if inverse:
            seq = seq[::-1]
        transformed_seqs.append(_padding_array(
            transform_func(seq[::-1]), False, max_len, default,
        ))
    return np.array(transformed_seqs)