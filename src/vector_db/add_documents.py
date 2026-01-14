from database import ChromaDB
import argparse
import os
import json


def add_documents(file, collection_name, db_name=None):
    with open(file) as f:
        data = json.load(f)

    ids = []
    documents = []
    metadatas = []

    for k, v in data.items():
        ids.append(k)
        with open(os.path.join(os.path.dirname(__file__), "../data", f"{v["code_file_rel_path"]}")) as code_f:
            documents.append(code_f.read())
        metadatas.append(
            {
                "lib": v["lib"],
                "id": k,
                "complement_id": k[:-1] if k.endswith("c") else k+"c"
            }
        )

    db = ChromaDB(collection_name=collection_name)
    db.insert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Populate a collection of source codes to calculate code similarity")
    parser.add_argument('-c', '--collection', type=str, required=True, help="Create a memorable unique name. Remember this to query the collection later.")
    parser.add_argument('-f', '--file', required=True, type=str, help="A file name to find source code paths and metadata. We only look for a JSON file in data directory in the src directory. Provide name including the extension.")

    args = parser.parse_args()
    input_file_path = os.path.join(os.path.dirname(__file__), "../data", args.file)
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Cannot find {args.file}")

    add_documents(input_file_path, args.collection)
