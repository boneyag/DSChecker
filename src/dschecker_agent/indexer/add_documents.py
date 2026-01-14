from selectolax.parser import HTMLParser
import os

from dschecker_agent.indexer.document_index import APIDocIndex
from dschecker.logging_util.logger import setup_logger

logger = setup_logger(__name__)


def add_documents_to_index(file_path):
    with open(file_path, 'r') as f:
        html_content = f.read()

    lib_name = file_path.split("/")[-2]

    tree = HTMLParser(html_content)

    meta_tag = tree.css_first('meta[property="og:url"]')
    if meta_tag:
        page_url = meta_tag.attributes.get("content", "")
        doc_type = classify_doc(page_url, tree)
    else:
        doc_type = ""

    extracted_text = []

    title_node = tree.css_first('h1')

    if title_node is None:
        logger.error(f"Document {file_path} does not have a title")
        return

    title = title_node.text(strip=True)
    if title.endswith('#'):
        title = title[:-1].strip()

    extracted_text.append(title)

    fqn, text = extract_doc_content(tree)
    extracted_text.extend(text)

    plain_text = "\n".join(extracted_text)

    doc_index = APIDocIndex()
    doc_index.add_document(
        title=title,
        fqn=",".join(fqn),
        doc_type=doc_type,
        lib=lib_name,
        path=file_path[76:],  # length of the file path string from / to html = 76
        content=plain_text
    )


def classify_doc(url, html_tree):
    if html_tree.css_first("dl.py.class, dl.py.function, dl.py.property, dl.py.attribute, dl.py.method, dl.py.data"):
        return "APIref"
    if html_tree.css_first("section.sphx-glr-example-title"):
        return "Example"
    if "auto_examples" in url or "examples" in url:
        return "Example"
    if "user_guide" in url or "tutorial" in url:
        return "Guide"
    # if "whatsnew" in url or "release" in url:
    #     return "ReleaseNotes"
    return "Other"


def extract_doc_content(tree):
    main = tree.css_first('main#main-content.bd-main')
    if main:
        article = main.css_first('article.bd-article')
    else:
        # Fallback: look for article directly (Seaborn case)
        article = tree.css_first('article.bd-article[role="main"]')

    if not article:
        return [], []

    dl_tags = article.css('dl.py.class, dl.py.function, dl.py.property, dl.py.attribute, dl.py.method, dl.py.data')

    fqn = []
    text_parts = []

    if dl_tags:
        for dl in dl_tags:
            dt_tag = dl.css_first('dt[id]')
            if dt_tag:
                api_id = dt_tag.attributes.get('id', '')
                if api_id:
                    fqn.append(api_id)
                    text_parts.append(api_id)
            text_parts.append(dl.text(separator=' ', strip=True))
    else:
        text_parts.append(article.text(separator=' ', strip=True))

    return fqn, text_parts


if __name__ == '__main__':
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__), '../html')):
        for file in files:
            if file.endswith('.html'):
                # logger.info(f"Adding document {file} to the index")
                add_documents_to_index(os.path.join(root, file))

    doc_index = APIDocIndex()
    doc_index.count_num_docs()
