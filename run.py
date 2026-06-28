from supportos.orchestrator import run_supportos

print("=" * 60)
print("SupportOS")
print("=" * 60)

while True:

    query = input("\nUser > ")

    if query.lower() == "exit":
        break

    result = run_supportos(query)

    print("\n" + "=" * 60)
    print("ANSWER\n")
    print(result["answer"])

    print("\n" + "=" * 60)
    print("VERIFICATION\n")
    print(result["verification"])