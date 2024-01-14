import glob
import logging
import os

from pathlib import Path

logging.basicConfig(level=logging.INFO)


def delete_document(document_name):
    # delete pdf and xml files for a paper

    files = []
    for filename in glob.glob(
        str(Path(f"files/{document_name}/{document_name}.*"))
    ):
        files.append(filename)
        os.remove(filename)

    if os.path.exists(f"files/{document_name}"):
        logging.info(f"delete folder files/{document_name}")
        os.rmdir(Path(f"files/{document_name}"))

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
