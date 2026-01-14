import os
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser, MultifieldParser

from dschecker_agent.indexer.schema import APIDocSchema
from dschecker.logging_util.logger import setup_logger

logger = setup_logger(__name__)


class APIDocIndex:
    def __init__(self):
        index_path = os.path.join(os.path.dirname(__file__), "../docindex")
        if not os.path.exists(index_path) or not os.listdir(index_path):
            os.makedirs(index_path, exist_ok=True)
            self.ix = create_in(index_path, APIDocSchema)
        else:
            self.ix = open_dir(index_path)

    def add_document(self, title, fqn, lib, doc_type, path, content):
        with self.ix.searcher() as searcher:
            parser = QueryParser("path", self.ix.schema)
            query = parser.parse(path)
            results = searcher.search(query)

            if results:
                for result in results:
                    logger.info(f"Document with path {path} already exists in the index.")
                    with self.ix.writer() as writer:
                        writer.delete_by_term("path", result['path'])

        with self.ix.writer() as writer:
            writer.add_document(
                title=title,
                fqn=fqn,
                lib=lib,
                doc_type=doc_type,
                path=path,
                content=content
            )

    def count_num_docs(self):
        with self.ix.searcher() as searcher:
            logger.info("Indexed Documents:")
            logger.info(f"Number of documents: {searcher.doc_count()}")

    def print_index(self):
        with self.ix.searcher() as searcher:
            for term in searcher.lexicon("content"):
                logger.info(term.decode("utf-8"))
            logger.info("End of Index.")

    def print_index_by_doc(self):
        with self.ix.searcher() as searcher:
            reader = searcher.reader()

            for docnum in reader.all_doc_ids():
                stored_fields = reader.stored_fields(docnum)
                print(f"Doc {docnum} (title={stored_fields.get('title')}):")

                terms = list(reader.field_terms("content"))
                doc_terms = [t for t in terms if t.startswith("roc")]
                print(f"Doc terms: {doc_terms}")

    def check_term_in_docs(self, term):
        with self.ix.searcher() as searcher:
            reader = searcher.reader()
            postings = list(reader.postings("content", term).all_ids())
            print(f"Docs containing '{term}': {postings}")
            for docnum in postings:
                stored = reader.stored_fields(docnum)
                print(f"  Doc {docnum} title={stored.get('title')}")

    def search_index(self, query_word):
        with self.ix.searcher() as searcher:
            # query = QueryParser("content", self.ix.schema).parse(query_word)
            parser = MultifieldParser(["title", "fqn", "content"], schema=self.ix.schema)
            query = parser.parse(query_word)
            logger.info(f"query: {query}")
            results = searcher.search(query, limit=5)
            logger.info(f"Found {len(results)} results for {query_word}")
            if results:
                docs = []
                for result in results:
                    logger.info(f"title: {result['title']} -- type: {result['doc_type']} -- path: {result['path']}")
                    docs.append(
                        {
                            "title": result['title'],
                            "type": result['doc_type'],
                            "content": result['content']
                        }
                    )
                return docs
            else:
                {"message": "No matching documents"}
