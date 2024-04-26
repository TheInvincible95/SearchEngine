# Search Engine

## Introduction
rave is a fully local, voice-enabled basic local search engine, using Okapi-BM25 algorithm (an improvement over traditional TF-IDF algorithms), written in Python.

## UI
![rave Homepage](./img/homepage.png)
*Homepage of rave*

![rave Results](./img/results1.png)
*Results displayed by rave for query "India" in categories "Politics" and "Entertainment"*

![rave Expanded Results](./img/results2.png)
*Expanded result data shown in rave when user clicks on a result title*

![rave Voice Search](./img/voice_search.png)
*rave processing user's spoken query*

## Usage
1. Create a python virtual environment and activate it via the activate scripts present in bin folder, depending on your shell.
2. Install the relevant version of pytorch for your system from: https://pytorch.org/get-started/locally/
3. Pull in dependencies and requirements by running
```pip install -r requirements.txt```  
4. Before starting, run this in a python shell/REPL: 

```
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```
5. Start the python http server by running
```python server.py```
6. The website will be accessible on localhost. Visit ```localhost:8000/start``` on your browser of choice.

## TODO
- [X] Use a different tokenizer and preprocess the text.
- [X] Use cosine distance for similarity
- [X] Use actual documents
- [X] Write indexes to disk
- [X] Make a frontend for the search engine

## Corpus Used
https://www.kaggle.com/datasets/sunilthite/text-document-classification-dataset (BBC News Yr. 2005 Corpus) 
