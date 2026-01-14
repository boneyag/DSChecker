from dschecker_agent.indexer.document_index import APIDocIndex


def search_documents_in_index(query_word):
    doc_index = APIDocIndex()
    doc_text = doc_index.search_index(query_word)
    if doc_text:
        return doc_text


if __name__ == '__main__':
    doc_index = APIDocIndex()
    search_documents_in_index("StandardScaler")  # sklearn.metrics.roc_curve
