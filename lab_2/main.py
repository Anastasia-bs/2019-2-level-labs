"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if isinstance(num_cols, int):
        return [[0 for j in range(num_cols)] for i in range(num_rows)]
    return []


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    m = edit_matrix
    if m and isinstance(add_weight, int) and isinstance(remove_weight, int):
        if len(m[0]):
            for i in range(1, len(m)):
                m[i][0] = m[i - 1][0] + remove_weight
            for j in range(1, len(m[0])):
                m[0][j] = m[0][j - 1] + add_weight
    return list(m)


def minimum_value(numbers: tuple) -> int:
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    m = edit_matrix
    if original_word and isinstance(add_weight, int) and isinstance(remove_weight, int) \
            and isinstance(substitute_weight, int):
        for i in range(1, len(m)):
            for j in range(1, len(m[0])):
                add = m[i][j-1] + add_weight
                remove = m[i-1][j] + remove_weight
                if original_word[i-1] == target_word[j-1]:
                    sub = m[i-1][j-1]
                else:
                    sub = m[i-1][j-1] + substitute_weight
                m[i][j] = minimum_value((add, remove, sub))
    return list(m)


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if isinstance(original_word, str) and isinstance(target_word, str) and isinstance(add_weight, int) \
            and isinstance(remove_weight, int) and isinstance(substitute_weight, int):
        return fill_edit_matrix(tuple(initialize_edit_matrix(tuple(generate_edit_matrix(len(original_word)+1,
                                                                                        len(target_word)+1)),
                                                             add_weight,
                                                             remove_weight)),
                                add_weight,
                                remove_weight,
                                substitute_weight,
                                original_word,
                                target_word)[-1][-1]
    return -1


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    with open(path_to_file, 'w') as f:
        for line in edit_matrix:
            for i in range(len(line)):
                line[i] = str(line[i])
            f.write(','.join(line) + '\n')


def load_from_csv(path_to_file: str) -> list:
    with open(path_to_file) as m:
        m = m.readlines()
        for i in range(len(m)):
            m[i] = m[i].split(',')
            for j in range(len(m[i])):
                m[i][j] = int(m[i][j])
    return m
