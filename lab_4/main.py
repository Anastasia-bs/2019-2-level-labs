import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    clean_text = []
    if isinstance(texts, list):
        for doc in texts:
            if isinstance(doc, str):
                while '<br />' in doc:
                    doc = doc.replace('<br />', ' ')
                for symbol in doc:
                    if not symbol.isalpha() and symbol not in ' \n':
                        doc = doc.replace(symbol, '')
                clean_text.append(doc.lower().split())
    return clean_text


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        if isinstance(self.corpus, list):
            for sentence in self.corpus:
                if isinstance(sentence, list):
                    self.tf_values.append({})
                    sentence = [el for el in sentence if isinstance(el, str)]
                    for word in sentence:
                        word_in_sentence = sentence.count(word)
                        self.tf_values[-1][word] = word_in_sentence/len(sentence)

    def calculate_idf(self):
        if isinstance(self.corpus, list):
            self.corpus = [el for el in self.corpus if isinstance(el, list)]
            for i, sentence in enumerate(self.corpus):
                sentence = [el for el in sentence if isinstance(el, str)]
                for word in sentence:
                    if word not in self.idf_values:
                        count = 1
                        for other_sentences in self.corpus[i+1:]:
                            if word in other_sentences:
                                count += 1
                        self.idf_values[word] = math.log(len(self.corpus) / count)

    def calculate(self):
        if self.tf_values and self.idf_values:
            for i, doc in enumerate(self.tf_values):
                self.tf_idf_values.append({})
                for key in doc:
                    if key in self.tf_values[i] and key in self.idf_values:
                        self.tf_idf_values[-1][key] = self.tf_values[i][key] * self.idf_values[key]

    def report_on(self, word, document_index):
        if self.tf_idf_values and document_index <= len(self.tf_idf_values):
            document = self.tf_idf_values[document_index]
            if word in document:
                words_in_doc = sorted(document, key=document.get, reverse=True)
                place = words_in_doc.index(word)
                return document[word], place
        return ()


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
