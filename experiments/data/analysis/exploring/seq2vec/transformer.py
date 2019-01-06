import numpy as np
from .utils import consistent_hash, word2vec_seq
from .padding import generate_padding_array

class Seq2VecHash:
    def __init__(self, vec_len):
        self.vec_len = vec_len

    def transform_single_sequence(self, seq):
        result = np.zeros(self.vec_len)
        for word in seq:
            index = consistent_hash(word) % self.vec_len
            result[index] += 1
        return result

    def __call__(self, seqs):
        result = []
        for seq in seqs:
            result.append(self.transform_single_sequence(seq))
        return np.array(result)

class Seq2VecWordEmbedding:
    def __init__(self, word2vec_model, max_len, inverse=False):
        self.max_len = max_len
        self.word2vec = word2vec_model
        self.word_embedding_size = word2vec_model.get_size()
        self.inverse = inverse
    
    def seq_transform(self, seq):
        return word2vec_seq(seq, self.word2vec)

    def __call__(self, seqs):
        array = generate_padding_array(
            seqs = seqs,
            transform_func = self.seq_transform,
            default = np.zeros(self.word_embedding_size),
            max_len = self.max_len,
            inverse = self.inverse
        )
        return array