"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    frequencies = {}
    if isinstance(text, str):
        text = text.lower()
        for symbol in text:
            if not symbol.isalpha() and symbol not in ' \n':
                text = text.replace(symbol, '')
        text_list = text.split()
        frequencies = {element: text_list.count(element) for element in text_list}
    return frequencies


def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    """
    Removes all stop words from th given frequencies dictionary
    """
    if frequencies:
        if stop_words:
            for word in stop_words:
                if word in frequencies:
                    del frequencies[word]
            not_str = [k for k in frequencies if not isinstance(k, str)]
            for a in not_str:
                if a in frequencies:
                    del frequencies[a]
    return frequencies


def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    word_list = []
    if top_n > len(frequencies):
        top_n = len(frequencies)
    if frequencies:
        for i in range(top_n):
            word = max(frequencies, key=frequencies.get)
            word_list.append(word)
            del frequencies[word]
    return tuple(word_list)


def read_from_file(path_to_file: str, lines_limit: int) -> str:
    with open(path_to_file, encoding='utf-8') as text:
        text = text.readlines()[:lines_limit]
    text = ''.join(text)
    return text


def write_to_file(path_to_file: str, content: tuple):
    with open(path_to_file, 'w') as new_text:
        for word in content:
            new_text.write(word+'\n')

