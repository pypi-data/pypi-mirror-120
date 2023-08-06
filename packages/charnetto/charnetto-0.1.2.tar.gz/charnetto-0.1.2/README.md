# Charnetto

This module is designed to create an automated character network based on a book or a movie script.

## Getting started

Charnetto is implemented both with spaCy and Flair for the named entity recognition step. Please install the desired library using

```
pip install spacy
```

or 

```
pip install flair
```

For more information, see the [online documentation](https://charnetto.readthedocs.io/en/latest/).

## How to use charnetto

You can use the Jupyter Notebook `charnetto_example.ipynb` to see a full example of how to generate a character network based on a book (with Flair as a NER tool or with manual annotations) or on a movie script.

## Supported data
* The books must be in `.txt`, ideally with one paragraph per line. For english books, replacing `,'` by `',` at the end of dialogues tends to give better results with the NER part.

* The movie scripts need to resemble those available on [IMSDB](https://imsdb.com/): the regex for character names looks for capital letters preceded by at least two line breaks.

* If you want to annotate some books manually, you can follow the URL notation in Markdown to identify characters. Online editors like [StackEdit](https://stackedit.io/) allow you to double-click on a name and add an URL (with `CTRL+L`). By writing `PER` in the URL part (for the tag "PERSON"), you will then be able to use charnetto to extract the annotated entities and generate a character network.