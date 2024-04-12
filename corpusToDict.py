# utility code to convert the corpus to a dictionary with the following format:
# document Number : (contents, label)

import csv


def getCorpus(filePath):
    # Converts the corpus to a dictionary with the following format:
    # document Number : (contents, label)
    corpus = {}

    with open(filePath, mode="r") as file:

        csvFile = csv.reader(file)

        for i, lines in enumerate(csvFile):
            # print(lines)
            corpus[i] = (lines[0], lines[1])

    return corpus
