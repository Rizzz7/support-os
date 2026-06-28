from pathlib import Path
import time

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

COLLECTION = "support_docs"

client = QdrantClient(
    url="https://7bcc1017-d58b-470d-95d4-532bc008e7a6.us-east-2-0.aws.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6ZmM5YzA0ZWQtZDg1MC00OGZiLWIzOTAtOTE3MjUzMzE1YmRhIn0.pWASPhri92yYnypZ2JUF4WL-Hqs1MjGITzk5j5jAE74",
    timeout=120
)

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Recreating collection...")

try:
    client.delete_collection(COLLECTION)
except Exception:
    pass

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

points = []
point_id = 0

print("Reading documentation...")

for file in Path("docs").glob("*.md"):

    print(f"  {file.name}")

    text = file.read_text(encoding="utf-8")

    chunks = text.split("\n\n")

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) < 30:
            continue

        vector = model.encode(chunk).tolist()

        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "text": chunk,
                    "source": file.name
                }
            )
        )

        point_id += 1

print(f"\nPrepared {len(points)} chunks.")

BATCH_SIZE = 64

uploaded = 0

for i in range(0, len(points), BATCH_SIZE):

    batch = points[i:i + BATCH_SIZE]

    success = False

    for attempt in range(3):

        try:

            client.upsert(
                collection_name=COLLECTION,
                points=batch,
                wait=True
            )

            uploaded += len(batch)

            print(
                f"Uploaded {uploaded}/{len(points)}"
            )

            success = True

            break

        except Exception as e:

            print(
                f"Retry {attempt+1}: {e}"
            )

            time.sleep(2)

    if not success:

        raise Exception(
            "Batch upload failed."
        )

print("\nIndexing complete.")