import json
import os

import tiktoken
from dotenv import load_dotenv
from extract_text import TEIFile
from grobid_client_python.grobid_client.grobid_client import GrobidClient
from openai import OpenAI
from utils import remove_last_x_percent


def process_pdf_grobid(
    file, config_path="configs/grobid_config.json", output="./files/"
):
    client = GrobidClient(config_path=config_path)
    client.process(
        "processFulltextDocument", "files/", output=output, force=True
    )


def send_prompt_to_openai(prompt, system_role):
    load_dotenv()

    with open("configs/openai_config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    api_key = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=config["model"],
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt},
        ],
    )
    return response


def get_summary(paper: str):
    print(paper)

    process_pdf_grobid(file=f"files/{paper}")
    file_location = f"files/{paper.replace('.pdf','')}.grobid.tei.xml"
    print(file_location)
    try:
        os.path.exists(file_location)
        teifile = TEIFile(file_location)
        body = teifile.get_body()
        body_texts = [t for para in body for t in para["text"]]
        full_text = " ".join(body_texts)

        n = num_tokens_from_string(full_text)
        with open("configs/openai_config.json", "r") as jsonfile:
            config = json.load(jsonfile)

        while n > config["context_window"]:  # text is too big
            full_text = remove_last_x_percent(full_text)
            print("Text has been reduced,")
            n = num_tokens_from_string(full_text)

        # noqa: E501
        prompt = f"""Summarize the text below. The summary should be 300 characters max and describes what this paper is about.

        {full_text}
        """  # noqa: E501

        system_role = "You are a helpful summarizer."
        response = send_prompt_to_openai(
            prompt=prompt, system_role=system_role
        )
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        print(f"An error has occured: {e}")


def get_embedding(text, model="text-embedding-ada-002"):
    load_dotenv()

    api_key = os.getenv("OPENAI_KEY")
    client = OpenAI(api_key=api_key)

    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=model).data[0].embedding
    )


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""

    with open("configs/openai_config.json", "r") as jsonfile:
        config = json.load(jsonfile)
    encoding = tiktoken.encoding_for_model(config["model"])

    num_tokens = len(encoding.encode(string))
    return num_tokens


def answer_question_rag(question: str, context: list):
    docs = []
    for i in range(len(context["ids"][0])):
        print(context["ids"][0][i])
        paper = context["ids"][0][i]
        file_location = f"files/{paper.replace('.pdf','')}.grobid.tei.xml"
        os.path.exists(file_location)
        teifile = TEIFile(file_location)
        body = teifile.get_body()
        body_texts = [t for para in body for t in para["text"]]
        full_text = " ".join(body_texts)
        docs.append(full_text)

    context_str = " ".join(docs)

    n = num_tokens_from_string(context_str)
    print("Context number of tokens : ", n)
    with open("configs/openai_config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    while n > config["context_window"]:  # text is too big
        context_str = remove_last_x_percent(context_str)
        print("Text has been reduced,")
        n = num_tokens_from_string(context_str)

    system_role = (
        "You are an assistant and you can only answer based on the provided"
        " context. If a response cannot be formed strictly using the context,"
        " politely say you don't have knowledge about that topic."
    )
    prompt = f"""Context information is below.
        -------------------------------------------
        Context: {context_str}
        -------------------------------------------
        Given the context information and not prior knowledge, answer the query.
        Query: {question}
        Answer:
        """  # noqa: E501
    response = send_prompt_to_openai(prompt=prompt, system_role=system_role)
    answer = response.choices[0].message.content
    return answer
