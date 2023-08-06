import re
import pandas


def extract_movie_df(text):
    """Extract entities in a movie script and load them in a dataframe.

    The extraction is based on a regex and a blacklist for tokens which should not
    appear in a character name. Therefore, the script should look like those of IMSDB.

    Columns of the output dataframe:

    name : text of the entity
    start_pos : starting position of the entity in the text (in characters)
    end_pos : ending position of the entity in the text (in characters)
    tag : category attributed to the entity (here always 'PER')
    score : 1 (the confidence is given by Flair, so we choose a default value of 1 to unify the outputs)
    block : id of the scene containing the entity

    Parameters
    ----------
    text: str
        Script of the film in .txt
    """
    header_regex = re.compile(r"(?m)\n*\s*\n*^\s*([^a-z]+?)\s*(\([\w'\s.]+\))?$")

    character_blacklist = [
        " - ",
        "*",
        " -- ",
        "...",
        "!",
        " AT ",
        "LATER",
        "LATE",
        "FADE OUT",
        "FADE IN",
        "CUT TO",
        "EXT.",
        "EXTERIOR",
        "INT.",
        "INTERIOR",
        "INSIDE",
        "OUTSIDE",
        "ANGLE ON",
        "MUSIC ON",
        "MUSIC UP",
        "CLOSE ON",
        "THE END",
        "CUT FROM",
        "CAMERA",
        "LENS",
        "MINIATURE",
        "ANGLE",
        "POV",
        "SUNSET",
        "AERIAL VIEW",
        "FANTASY",
        "CLOSE UP",
        "SLOW MOTION",
        "CLOSE-UP",
        " END ",
        " END." " DAY ",
        "NIGHT",
        "MORNING",
        "EVENING",
        "WEEK",
        "SCENE",
        "ACTION",
        "CONTINUED",
        "CHANGED",
        "HORIZON",
        "ENDS",
        "MONTAGE",
        "FROM",
        "WIDE-SHOT",
        "SHOT",
        "EXPLOSION",
        "THEY",
        "DISSOLVE",
        "FOOTAGE",
        "CONTINUED",
        "ROOM",
        "UP AHEAD",
        "SHOOTING SCRIPT",
        "NEARBY",
        "CUTS",
        "SEES",
        "INSERT",
        "REVEAL",
        " IN ",
        " OF ",
        " ON ",
        " TO ",
        " BACK ",
        " THAT ",
        " AND ",
    ]

    entities = []
    reply_scene = 0

    for match in header_regex.finditer(text):
        if any([w in match.group(0) for w in character_blacklist]):
            reply_scene += 1
            continue
        char_name = match.group(1).strip()
        if char_name:
            start = match.span()[0]
            end = match.span()[1]

            entity = {
                "name": char_name,
                "start_pos": start,
                "end_pos": end,
                "tag": "PER",
                "score": 1,
                "block": reply_scene,
            }

            entities.append(entity)

    entity_df = pandas.DataFrame(entities)

    return entity_df
