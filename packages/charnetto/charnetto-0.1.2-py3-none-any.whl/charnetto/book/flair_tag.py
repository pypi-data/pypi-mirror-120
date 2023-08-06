from tqdm import tqdm
import json
from collections import Counter, defaultdict
import pandas


# TODO add the Mr. / Mrs. in the annotation
# TODO accept maj/min in characters list


def flair_tag(line, tagger):
    """Apply Flair NER to a line"""

    from flair.data import Sentence

    paragraph = Sentence(line, use_tokenizer=True)
    tagger.predict(paragraph)
    return paragraph


def get_lines(path):
    """Parse lines in a file.
    
    Takes a path to a .txt file and splits it on each "\n" to output a list of lines.
    
    Parameters
    ----------
    path: str
        The path of the .txt file

    """
    with open(path, "r", encoding="utf-8", newline="\n") as file:
        content = file.read()
        lines = content.split("\n")
        return lines


def flair_ner(lines, tagger):
    """Apply Flair NER to a file"""

    paragraphs = []
    len_diffs = []

    for line in tqdm(lines):
        line_length = len(line)
        paragraph = flair_tag(line, tagger)
        len_diff = line_length - len(paragraph.to_original_text())
        paragraphs.append(paragraph)
        len_diffs.append(len_diff)

    return paragraphs, len_diffs


def extract_flair_df(lines, tagger):
    """Apply Flair NER to a file and generate a dataframe of all entities

    Each line in the file should correspond to a paragraph for the NER to work optimally.

    The tagger depends on the language of the text.
    For example, for an english text, use SequenceTagger.load('ner').
    See the documentation of Flair for the complete list of available taggers.

    Columns of the dataframe:

    name : text of the entity
    start_pos : starting position of the entity in the text (in characters)
    end_pos : ending position of the entity in the text (in characters)
    tag : category attributed by Flair to the entity
    score : confidence in the tag (attributed by Flair)
    block : id of the line containing the entity

    Parameters
    ----------
    lines: list
        List of lines from the text (can be extracted with get_lines(path))
    tagger: object
        Flair tagger, depends on the language of the text.

    """
    entities = []
    offset = 0

    paragraphs, len_diffs = flair_ner(lines, tagger)

    for i in range(len(paragraphs)):
        paragraph = paragraphs[i]
        len_diff = len_diffs[i]

        for span in paragraph.get_spans("ner"):
            entity = {
                "name": span.text,
                "start_pos": offset + span.start_pos,
                "end_pos": offset + span.end_pos,
                "tag": span.tag,
                "score": span.score,
                "block": i,
            }

            entities.append(entity)

        offset += len(paragraph.to_original_text()) + len_diff + 1

    entity_df = pandas.DataFrame(entities)

    return entity_df


# Bonus: count total occurrences of characters

# Determine if the entity is a person
def is_char(entity):
    return entity.tag == "PER"


# Count occurrences of an entity in a paragraph
def count_char(paragraph):
    nb_char_par = Counter()

    for entity in paragraph.get_spans("ner"):
        if is_char(entity):
            nb_char_par[entity.text] += 1

    return nb_char_par


# Sort by most common characters
def sort_char(char_list):
    characters_sorted = char_list.most_common()
    return characters_sorted


# List sorted characters in a text
def flair_characters(paragraphs):
    nb_characters = Counter()
    context = defaultdict(list)

    for paragraph in paragraphs:
        nb_char_par = count_char(paragraph)
        nb_characters.update(nb_char_par)
        for entity in nb_char_par:
            context[entity].append(paragraph)

    characters_sorted = sort_char(nb_characters)
    return characters_sorted, context


# whole pipeline from path to sorted list of characters
def flair_char_pipe(path, tagger):

    paragraphs, _ = flair_ner(path, tagger)
    characters_sorted, context = flair_characters(paragraphs)
    json_char = {"counter": characters_sorted, "context": str(context)}

    return characters_sorted, context
