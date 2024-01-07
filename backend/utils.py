import glob
import os

from pathlib import Path


def delete_document(document_name):
    # delete pdf and xml files for a paper

    files = []
    for filename in glob.glob(
        str(Path(f"files/{document_name}")).replace(".pdf", ".*")
    ):
        files.append(filename)
        os.remove(filename)
    if files != []:
        file_deletion_message = f"Files [{files}] were found and deleted."
    else:
        file_deletion_message = "No Files were found and deleted."

    return file_deletion_message


def remove_last_x_percent(text: str, percent: int = 10):
    words = text.split(" ")
    n_words_to_remove = int(len(words) * (percent / 100))
    words = words[: len(words) - n_words_to_remove]
    return " ".join(words)
