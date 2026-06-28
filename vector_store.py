from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION = "support_docs"

client = QdrantClient(
    url="https://7bcc1017-d58b-470d-95d4-532bc008e7a6.us-east-2-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6ZmM5YzA0ZWQtZDg1MC00OGZiLWIzOTAtOTE3MjUzMzE1YmRhIn0.pWASPhri92yYnypZ2JUF4WL-Hqs1MjGITzk5j5jAE74"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query: str):

    vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        limit=3,
    ).points

    return [r.payload for r in results]