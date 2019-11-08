"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if isinstance(num_cols, int):
        return [[0 for j in range(num_cols)] for i in range(num_rows)]
    return []


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    if edit_matrix and isinstance(add_weight, int) and isinstance(remove_weight, int) and edit_matrix[0]:
        for i in range(1, len(edit_matrix)):
            edit_matrix[i][0] = edit_matrix[i - 1][0] + remove_weight
        for j in range(1, len(edit_matrix[0])):
            edit_matrix[0][j] = edit_matrix[0][j - 1] + add_weight
    return list(edit_matrix)


def minimum_value(numbers: tuple) -> int:
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    if original_word and isinstance(add_weight, int) and isinstance(remove_weight, int) \
            and isinstance(substitute_weight, int):
        for i in range(1, len(edit_matrix)):
            for j in range(1, len(edit_matrix[0])):
                add = edit_matrix[i][j-1] + add_weight
                remove = edit_matrix[i-1][j] + remove_weight
                if original_word[i-1] == target_word[j-1]:
                    sub = edit_matrix[i-1][j-1]
                else:
                    sub = edit_matrix[i-1][j-1] + substitute_weight
                edit_matrix[i][j] = minimum_value((add, remove, sub))
    return list(edit_matrix)


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
    with open(path_to_file, 'w') as file:
        for line in edit_matrix:
            for i, num in enumerate(line):
                line[i] = str(num)
            file.write(','.join(line) + '\n')


def load_from_csv(path_to_file: str) -> list:
    with open(path_to_file) as matrix:
        matrix = matrix.readlines()
        for i, string in enumerate(matrix):
            matrix[i] = string.split(',')
            for j, num in enumerate(matrix[i]):
                matrix[i][j] = int(num)
    return matrix
