# Search Engine

## Usage
1. Create a python virtual environment and activate it via the activate scripts present in bin folder, depending on your shell.
2. Install the relevant version of pytorch(2.2.1) for your system from: https://pytorch.org/get-started/locally/
3. Pull in dependencies and requirements by running
```pip install -r requirements.txt```
4. Start the python http server by running
```python server.py```
5. The website will be accessible on localhost. Visit ```localhost:8000/start``` on your browser of choice.

## TODO
- [X] Use a different tokenizer and preprocess the text.
- [X] Use cosine distance for similarity
- [X] Use actual documents
- [X] Write indexes to disk
- [X] Make a frontend for the search engine

## Corpus Used
https://www.kaggle.com/datasets/sunilthite/text-document-classification-dataset

Before Running, run this in python: 

```
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```
