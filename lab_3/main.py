"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if isinstance(word, str) and word not in self.storage:
            self.storage[word] = len(self.storage) + 1
            return self.storage[word]

    def get_id_of(self, word: str) -> int:
        if isinstance(word, str):
            if word in self.storage:
                return self.storage[word]
        return -1

    def get_original_by(self, id: int) -> str:
        if isinstance(id, int) and id in self.storage.values():
            for k, v in self.storage.items():
                if id == v:
                    return k
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if isinstance(corpus, tuple):
            for word in corpus:
                self.put(word)
        return self.storage


class NGramTrie:
    def __init__(self, n):
        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        if isinstance(sentence, tuple):
            gram_list = [sentence[i:i+self.size] for i in range(len(sentence)) if
                         len(sentence[i:i+self.size]) == self.size]
            for gram in gram_list:
                if gram not in self.gram_frequencies:
                    self.gram_frequencies[gram] = 1
                else:
                    self.gram_frequencies[gram] += 1
        if self.gram_frequencies:
            return 'OK'
        return 'ERROR'

    def calculate_log_probabilities(self):
        for gram in self.gram_frequencies:
            all_grams = 0
            for other_gram in self.gram_frequencies:
                if gram[:-1] == other_gram[:-1]:
                    all_grams += self.gram_frequencies[other_gram]
            self.gram_log_probabilities[gram] = math.log(self.gram_frequencies[gram] / all_grams)
        return self.gram_log_probabilities

    def predict_next_sentence(self, prefix: tuple) -> list:
        if isinstance(prefix, tuple) and len(prefix) == self.size-1:
        predicted = list(prefix)
            while True:
               most_prob = [(self.gram_log_probabilities[gram], gram) for gram in self.gram_log_probabilities if
                            gram[:-1] == prefix]
               if most_prob:
                   most_prob = max(most_prob)
                   predicted.append(most_prob[1][-1])
                   prefix = tuple(predicted[-self.size+1:])
               else:
                   return predicted
        return []


def encode(storage_instance, corpus) -> list:
    if isinstance(storage_instance, WordStorage) and isinstance(corpus, list):
        for sentence in corpus:
            storage_instance.from_corpus(tuple(sentence))
            for i, token in enumerate(sentence):
                sentence[i] = storage_instance.get_id_of(token)
        return corpus


def split_by_sentence(text: str) -> list:
    sentences = []
    if text and ('.' in text or '?' in text or '!' in text):
        for symbol in text:
            if not symbol.isalpha() and symbol not in '.?! \n':
                text = text.replace(symbol, '')
        text = text.split()
        text = ' '.join(text)
        for i in range(len(text) - 2):
            if text[i:i + 2] in ('? ', '! ', '. ') and text[i + 2].isupper():
                text = text.replace(text[i:i + 2], '//')
        if text[-1] in '.!?':
            text = text.replace(text[-1], '')
        if text:
            sentences = text.lower().split('//')
            for i, sentence in enumerate(sentences):
                sentences[i] = sentence.split()
                sentences[i].insert(0, '<s>')
                sentences[i].insert(len(sentence), '</s>')
    return sentences
