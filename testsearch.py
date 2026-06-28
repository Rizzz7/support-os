from vector_store import search

query = input("Query: ")

results = search(query)

print("\nRESULTS\n")

for i, r in enumerate(results, start=1):
    print("=" * 60)
    print(f"Result {i}")
    print("Source:", r["source"])
    print()
    print(r["text"])
    print()