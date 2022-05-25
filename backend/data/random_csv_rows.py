# flake8: noqa

import random

ALL_TEXTS = []

with open("data/big_i48.csv", "r") as file:
    ALL_TEXTS = file.readlines()[1:]
    print(f"Read {len(ALL_TEXTS)} texts from file")

N = 30
random_texts = random.choices(population=ALL_TEXTS, k=N)

template = """    FinderTestCase(
        text={text},
        expected_features=[

        ],
    ),"""

for text in random_texts:
    print(template.format(text=text.replace("\n", "")))
