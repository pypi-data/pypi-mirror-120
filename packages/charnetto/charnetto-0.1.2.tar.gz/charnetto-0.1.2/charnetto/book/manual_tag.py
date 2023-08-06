import pandas
import re


def get_lines(manual_path):
    """Parse lines in a file.
    
    Takes a path to a .txt file and splits it on each "\n" to output a list of lines.
    
    Parameters
    ----------
    path: str
        The path of the .txt file

    """
    with open(manual_path, "r", encoding="utf-8", newline="\n") as file:
        content = file.read()
        lines = content.split("\n")
        return lines


def manual_tag(line, offset=0, len_previoustext=0):
    """Export manual annotations (in markdown mode)"""
    ent_list = []
    pattern = re.compile(r"\[([^\]]+)\]\((\w+)\)")
    iterator = pattern.finditer(line)
    for match in iterator:
        offset += 1
        text_span = match.span(1)
        start = text_span[0] + len_previoustext - offset
        end = text_span[1] + len_previoustext - offset

        tag_span = match.span(2)
        len_tag = tag_span[1] - tag_span[0]
        offset += 3 + len_tag

        entity = {
            "name": match.group(1),
            "start_pos": start,
            "end_pos": end,
            "tag": match.group(2),
            "score": 1,
        }

        ent_list.append(entity)
        len_line = len(line)
    return ent_list, offset


def manual_ner(lines):
    entities = []
    offset = 0
    len_text = 0
    paragraph_nb = 0

    for line in lines:
        len_line = len(line) + 1
        ent_list, offset = manual_tag(line, offset=offset, len_previoustext=len_text)
        len_text += len_line

        for ent in ent_list:
            ent["block"] = paragraph_nb
            entities.append(ent)

        paragraph_nb += 1

    return entities


def extract_manual_df(lines):
    """Export manual annotations (in markdown mode) and generate a dataframe of all entities

    The following syntax is expected in the file:

    [Mark](PER) is outside.

    The entity is put in square brackets [], and the tag is given in parentheses () just after the entity.
    This is the syntax used for URLs in Markdown, which allows you to use a Markdown editor and put the tags as hyperlinks on the entities.

    Columns of the output dataframe:

    name : text of the entity
    start_pos : starting position of the entity in the text (in characters)
    end_pos : ending position of the entity in the text (in characters)
    tag : category attributed to the entity
    score : 1 (the confidence is given by Flair, so we choose a default value of 1 to unify the outputs)
    block : id of the line containing the entity

    Parameters
    ----------
    lines: list
        List of lines from the text (can be extracted with get_lines(path))
    """
    entities = manual_ner(lines)
    entity_df = pandas.DataFrame(entities)

    return entity_df
