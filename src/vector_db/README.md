### Some details of the vector DB

collection name: `ds_misuse` (Need to know this to search code. Can find the name programmatically if forgotten.)

```python
import chromadb
db_path = os.path.join(os.path.dirname(__file__), "storage/chroma")
client = chromadb.PersistentClient(path=db_path)
collections = client.list_collections()
if collections:
    for collection in collections:
        print(collection.name)
```