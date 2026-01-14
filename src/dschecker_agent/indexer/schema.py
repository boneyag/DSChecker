from whoosh.fields import SchemaClass, TEXT, ID, KEYWORD
from whoosh.analysis import StemmingAnalyzer


class APIDocSchema(SchemaClass):
    title = TEXT(stored=True, field_boost=3.0)
    fqn = KEYWORD(stored=True, commas=True, scorable=True, lowercase=True, field_boost=2.0)
    lib = KEYWORD(stored=True, lowercase=True)
    doc_type = TEXT(stored=True)
    path = ID(stored=True, unique=True)
    content = TEXT(analyzer=StemmingAnalyzer(), stored=True, field_boost=1.0)
