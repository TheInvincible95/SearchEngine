# utility code to convert the corpus to a dictionary with the following format:
# document Number : (contents, label)

import csv


def getCorpus(filePath):
    corpus = {}

    with open(filePath, mode="r") as file:

        csvFile = csv.reader(file)
        # convert the corpus to a dict with the following format:
        # document Number : (contents, label)

        for i, lines in enumerate(csvFile):
            # print(lines)
            corpus[i] = (lines[0], lines[1])

    return corpus
