from database import ChromaDB
import argparse
import json
import os


def search_document(input_file, collection_name, n_results):
    db = ChromaDB(collection_name=collection_name)  # collection name: ds_misuse
    print(db.get_num_docs())  # sanity check to see if the documents are persisted

    with open(input_file) as f:
        data = json.load(f)

    for _, v in data.items():
        with open(os.path.join(os.path.dirname(__file__), "../data", v["code_file_rel_path"])) as f:
            code = f.read()
        query = code
        condition = {
            "$and": [
                {"lib": {"$eq": v["lib"]}},  # only search code snippets from the same library
                {"id": {"$ne": v["num"]}},  # skip exact clone
                {"complement_id": {"$ne": v["num"]}}  # skip near clone
            ]
        }

        similar_misuse_id = ""
        similar_correct_id = ""

        results = db.search(query=query, n_results=n_results, condition=condition)
        if results and results.get('ids') and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                doc_id = results['ids'][0][i]
                # document_content = results['documents'][0][i]
                # metadata = results['metadatas'][0][i]
                # distance = results['distances'][0][i]

                if similar_correct_id != "" and similar_misuse_id != "":
                    break
                if doc_id.endswith('c') and similar_correct_id == "" and similar_misuse_id == "":
                    similar_correct_id = doc_id
                if doc_id.endswith('c') and similar_correct_id == "" and similar_misuse_id != "" and doc_id[:-1] != similar_misuse_id:
                    similar_correct_id = doc_id
                if not doc_id.endswith('c') and similar_misuse_id == "" and similar_correct_id == "":
                    similar_misuse_id = doc_id
                if not doc_id.endswith('c') and similar_misuse_id == "" and similar_correct_id != "" and doc_id+'c' != similar_correct_id:
                    similar_misuse_id = doc_id

                # print(f"  Result {i+1}:")
                # print(f"    ID: {doc_id}")
                # print(f"    Document Content: {document_content}")
                # print(f"    Metadata: {metadata}")
                # print(f"    Distance: {distance:.4f}")
                # print("-" * 30)
        else:
            print("No relevant search results found for the given query.")

        v["similar_instances"]["misuse_instance"] = similar_misuse_id
        v["similar_instances"]["correct_instance"] = similar_correct_id

    with open(input_file, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search similar code snippets and find the best matching misuse and correct API usage.")
    parser.add_argument('-c', '--collection', type=str, required=True, help="Create a memorable unique name. Remember this to query the collection later.")
    parser.add_argument('-f', '--file', required=True, type=str, help="A file name to find source code paths and metadata. We only look for a JSON file in data directory in the src directory. Provide name including the extension.")
    parser.add_argument('-n', '--num-results', type=int, help="Number of results to be returned from search.")
    args = parser.parse_args()

    input_file_path = os.path.join(os.path.dirname(__file__), "../data", f"{args.file}")
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Cannot find {args.file}")

    # Use underscore instead of hyphen in 'num-results'-->'num_results' when access it in Python. Use as it is when parsing args in cmd     
    search_document(input_file_path, args.collection, args.num_results)
