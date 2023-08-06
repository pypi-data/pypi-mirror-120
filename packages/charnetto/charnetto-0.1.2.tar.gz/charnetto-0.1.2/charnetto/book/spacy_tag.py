from tqdm import tqdm
import pandas


def spacy_tag(line, tagger):
    """Apply Spacy NER to a line"""
    paragraph = tagger(line)
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


def spacy_ner(lines, tagger):
    """Apply Spacy NER to a file"""
    paragraphs = []
    len_diffs = []

    for line in tqdm(lines):
        line_length = len(line)
        paragraph = spacy_tag(line, tagger)
        len_diff = line_length - len(paragraph.text)
        paragraphs.append(paragraph)
        len_diffs.append(len_diff)

    return paragraphs, len_diffs


def extract_spacy_df(lines, tagger):
    """Apply Spacy NER to a file and generate a dataframe of all entities

    Each line in the file should correspond to a paragraph for the NER to work optimally.

    The tagger depends on the language of the text.
    For example, for an english text, use spacy.load("en_core_web_lg").
    See the documentation of Spacy for the complete list of available taggers.

    Columns of the dataframe:

    name : text of the entity
    start_pos : starting position of the entity in the text (in characters)
    end_pos : ending position of the entity in the text (in characters)
    tag : category attributed by Spacy to the entity
    score : 1 (the confidence is given by Flair but not by Spacy, so we choose a default value of 1)
    block : id of the line containing the entity

    Parameters
    ----------
    lines: list
        List of lines from the text (can be extracted with get_lines(path))
    tagger: object
        Spacy tagger, depends on the language of the text.
    """
    entities = []
    offset = 0

    paragraphs, len_diffs = spacy_ner(lines, tagger)

    for i in range(len(paragraphs)):
        paragraph = paragraphs[i]
        len_diff = len_diffs[i]

        for ent in paragraph.ents:
            entity = {
                "name": ent.text,
                "start_pos": offset + ent.start_char,
                "end_pos": offset + ent.end_char,
                "tag": ent.label_,
                "score": 1,
                "block": i,
            }

            entities.append(entity)

        offset += len(paragraph.text) + len_diff + 1

    entity_df = pandas.DataFrame(entities)

    return entity_df


def unify_tags(spacy_df):
    """Unify the tags attributed by Spacy to match those of Flair"""
    conversion = {
        "LAW": "MISC",
        "PERSON": "PER",
        "ORG": "ORG",
        "DATE": None,
        "TIME": None,
        "LOC": "LOC",
        "NORP": "MISC",
        "FAC": "MISC",
        "CARDINAL": None,
        "GPE": "LOC",
        "WORK_OF_ART": "MISC",
        "QUANTITY": None,
        "ORDINAL": None,
        "PRODUCT": "MISC",
        "EVENT": "MISC",
        "MONEY": None,
        "LANGUAGE": None,
        "PERCENT": None,
    }

    spacy_df = spacy_df.replace(to_replace=conversion)
    spacy_df = spacy_df.dropna(subset=["tag"])

    return spacy_df
