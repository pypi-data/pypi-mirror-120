import html
import pandas


def highlight(path, df_path):
    from IPython.display import HTML

    with open(path, "r", encoding="utf-8", newline="\n") as file:
        text = file.read()

    book_df = pandas.read_csv(df_path, index_col=0)

    manual_parts = []
    offset = 0

    color = {
        "PER": "red",
        "LOC": "blue",
        "ORG": "green",
        "MISC": "orange",
    }

    for index, row in book_df.iterrows():
        start_pos = row["start_pos"]
        end_pos = row["end_pos"]
        tag = row["tag"]

        part = html.escape(text[offset:start_pos])
        manual_parts.append(part)

        part = '<span style="color:{}">'.format(color[tag])
        manual_parts.append(part)

        part = html.escape(text[start_pos:end_pos])
        manual_parts.append(part)

        part = "</span>"
        manual_parts.append(part)

        offset = end_pos

        ent_end = text.find("\n", offset)

    part = html.escape(text[end_pos:ent_end])
    manual_parts.append(part)

    return HTML("".join(manual_parts).replace("\n", "<br>"))
