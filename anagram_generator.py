import functools
import sys
from collections import Counter

with open("words.txt", "r") as f:
    corpus = [word.lower() for word in f.read().splitlines() if len(word) > 1]


def counter_is_subset(counter1: Counter, counter2: Counter) -> bool:
    left = counter1 - counter2
    right = counter2 - counter1
    if left != counter1 and right == Counter():
        return True
    else:
        return False


@functools.lru_cache
def create_counter(word: str) -> Counter:
    return Counter(word.replace("'", "").replace(" ", ""))


def anagram_generator(input_counter: Counter) -> list[str]:
    possible_words = set()
    for word in corpus:
        word_counter = create_counter(word)
        if counter_is_subset(input_counter, word_counter):
            possible_words.add(word)

    final_words = []

    def anagram_generator_helper(
        input_counter: Counter, possible_words: set[str], words: list[str]
    ) -> None:
        if len(input_counter) == 0:
            final_words.append(" ".join(words))
            possible_words = possible_words - set(words)

        for word in possible_words:
            word_counter = create_counter(word)
            if counter_is_subset(input_counter, word_counter):
                anagram_generator_helper(
                    input_counter - word_counter,
                    possible_words - set(word),
                    words + [word],
                )

    anagram_generator_helper(input_counter, possible_words, [])

    return final_words


def main() -> int:
    input_words = " ".join(sys.argv[1:])
    input_counter = create_counter(input_words)
    result = anagram_generator(input_counter)

    print(result)

    return 0


if __name__ == "__main__":
    sys.exit(main())
