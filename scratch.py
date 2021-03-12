import random
from scipy.sparse import dok_matrix

def generate_matrix(wordstream: list=None) -> dok_matrix:

    corpus = set()
    if wordstream is None:
        with open("corpus.txt", encoding="utf-8") as file:
            wordstream = file.read().replace("\n", " ").replace("\t","").lower()

        wordstream = wordstream.split(" ")
        # wordstream = re.sub(R"([\".,!?])", R" \1", wordstream).split(" ")

    corpus = set(wordstream)
    corpus_indices = list(corpus)
        
    size = len(corpus)
    matrix = dok_matrix((size, size))

    last_word = ""
    done = 0
    for word in wordstream:
        current_index = corpus_indices.index(word)
        last_index = corpus_indices.index(last_word)

        matrix[current_index, last_index] += 1

        last_word = word

        done += 1


    return matrix, corpus, corpus_indices

def markov_chain(matrix: dok_matrix, corpus: set, corpus_indices: list, n: int=None) -> str: # wordstream should be just a list of words

    size = len(corpus)

    starting_word = random.choice(tuple(corpus))

    words = [starting_word]
    if n is None: n = 100

    current_word = starting_word

    for _ in range(n):

        possibilities = []

        [possibilities.extend(
            [corpus_indices[i]] * int(matrix[i, corpus_indices.index(current_word)])
        ) for i in range(size)]

        words.append(random.choice(possibilities))

        current_word = words[-1]

    return " ".join(words)