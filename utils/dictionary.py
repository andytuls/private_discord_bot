import os

ALL_WORDS = None
_WORDS_BY_LETTER = None

def load_dictionary():
    global ALL_WORDS, _WORDS_BY_LETTER
    file_path = os.path.join(os.path.dirname(__file__), '..', 'nouns.txt')
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Папка nouns не найдена по пути: {file_path}")

    all_words = set()
    words_by_letter = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word:
                all_words.add(word)
                first_letter = word[0]
                if first_letter not in words_by_letter:
                    words_by_letter[first_letter] = set()
                words_by_letter[first_letter].add(word)

    ALL_WORDS = all_words
    _WORDS_BY_LETTER = words_by_letter