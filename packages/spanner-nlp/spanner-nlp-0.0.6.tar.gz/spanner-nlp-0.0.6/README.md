# Stanford CoreNLP Python Wrapper
Python wrapper for [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/index.html) that interfaces with the [Stanford CoreNLP server](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html).
It provides a simple API for text processing tasks such as Tokenization, Part of Speech Tagging, Named Entity Reconigtion, Constituency Parsing, Dependency Parsing, as described in the [Full List Of Annotators](https://stanfordnlp.github.io/CoreNLP/annotators.html).

## Prerequisites
* Java 1.8+ ([Download Page](https://www.java.com/en/)). You can check java version with the command: `java -version`.
* Python 3.6+ ([Download Page](https://www.python.org/downloads/)). You can check python version with the command: `python --version`.
* Stanford CoreNLP files version 4.1.0 ([Download Page](http://nlp.stanford.edu/software/stanford-corenlp-4.1.0.zip)).

## Usage
### Annotators wrapper - Simple Usage - Using local files
This example will demonstrate how to use the annotators wrapper using the local files downloded from [Stanford CoreNLP](http://nlp.stanford.edu/software/stanford-corenlp-4.1.0.zip).   
All the annotators and their information can be found in [Stanford CoreNLP Full List Of Annotators](https://stanfordnlp.github.io/CoreNLP/annotators.html).
```python
from StanfordCoreNLP import StanfordCoreNLP

with StanfordCoreNLP('stanford-corenlp-4.1.0') as nlp:
    print('Tokenize:', nlp.tokenize("Hello world. Hello world again."))
    print('Sentence Splitting:', nlp.ssplit("Hello world. Hello world again."))
    print('Part of Speech:', nlp.pos("Marie was born in Paris."))
```
Example output Tokenize:
```json
Tokenize: [
    {
        "token": "Hello",
        "span": [
            0,
            5
        ]
    },
    {
        "token": "world",
        "span": [
            6,
            11
        ]
    },
    ...
```
Example output Sentence Splitting:
```json
Sentence Splitting: [
    "Hello world.",
    "Hello world again."
]
```
Example output Part of Speech:
```json
Part of Speech: [
    {
        "token": "Marie",
        "pos": "NNP",
        "span": [
            0,
            5
        ]
    },
    {
        "token": "was",
        "pos": "VBD",
        "span": [
            6,
            9
        ]
    },
    ...
```
### Manual Annotators
The examples below will demonstrate how to define annotators Manualy using local files or using existing server.

Properties for using manual annotators:
* annotators: [Full List Of Annotators](https://stanfordnlp.github.io/CoreNLP/annotators.html).
* pinelineLanguage: [Full List Of Human Languages](https://stanfordnlp.github.io/CoreNLP/human-languages.html).
* outputFormat: [JSON, XML, Text, Serialized](https://stanfordnlp.github.io/CoreNLP/corenlp-server.html#annotate-with-corenlp-).
#### Manual Annotators - Using local files
```python
from StanfordCoreNLP import StanfordCoreNLP

nlp = StanfordCoreNLP('stanford-corenlp-4.1.0')
text = 'The small red car turned very quickly around the corner.'
pros = {'annotators' : 'ner', 'pinelineLanguage' : 'en', 'outputFormat' : 'xml'} #Named Entity Recognition example
print(nlp.annotate(text, properties = pros))
nlp.close()
```
Example output:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet href="CoreNLP-to-HTML.xsl" type="text/xsl"?>
<root>
  <document>
    <sentences>
      <sentence id="1">
        <tokens>
          <token id="1">
            <word>The</word>
            <lemma>the</lemma>
            <CharacterOffsetBegin>0</CharacterOffsetBegin>
            <CharacterOffsetEnd>3</CharacterOffsetEnd>
            <POS>DT</POS>
            <NER>O</NER>
          </token>
          <token id="2">
           ...
```

#### Manual Annotators - Using existing server
```python
from StanfordCoreNLP import StanfordCoreNLP

nlp = StanfordCoreNLP('http://corenlp.run', port = 80)
text = 'Joe Smith lives in California. He used to live in Oregon.'
pros = {'annotators' : 'lemma', 'pinelineLanguage' : 'en', 'outputFormat' : 'JSON'} #Lemmatization example
print(nlp.annotate(text, properties = pros))
nlp.close()
```
Example output:
```json
{
  "sentences": [
    {
      "index": 0,
      "tokens": [
        {
          "index": 1,
          "word": "Joe",
          "originalText": "Joe",
          "lemma": "Joe",
          "characterOffsetBegin": 0,
          "characterOffsetEnd": 3,
          "pos": "NNP",
          "before": "",
          "after": " "
        },
        {
          "index": 2,
           ...
```

#### Manual Annotators - Support a number of annotators at the same time - Using local files
Note: This example also support using existing server.
```python
from StanfordCoreNLP import StanfordCoreNLP

nlp = StanfordCoreNLP('stanford-corenlp-4.1.0', lang = 'en')
text = 'Joe Smith lives in California. He used to live in Oregon.'
pros = {'annotators' : 'tokenize, ssplit, pos', 'pinelineLanguage' : 'en', 'outputFormat' : 'JSON'}
print(nlp.annotate(text, pros, True))
nlp.close()
```
Example output:
```json
{
    "tokenize": [
        {
            "token": "Joe",
            "span": [
                0,
                3
            ]
        },
        {
            "token": "Smith",
            "span": [
                4,
                9
            ]
        },
        {
            "token": "lives",
            "span": [
                10,
                15
            ]
        },
        {
            "token": "in",
            "span": [
                16,
                18
            ]
        },
        {
            "token": "California",
            "span": [
                19,
                29
            ]
        },
        ...
```

## Debug
You can debug using the `logging` module in python.
This example will demonstrate how to use the `logging` module:
```python
from StanfordCoreNLP import StanfordCoreNLP
import logging

nlp = StanfordCoreNLP('stanford-corenlp-4.1.0', quiet = False, loggingLevel = logging.DEBUG)
text = 'The small red car turned very quickly around the corner.'
print(nlp.annotate(text)) #default annotate
nlp.close()
```
