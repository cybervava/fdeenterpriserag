from pathlib import Path


BASE_DIR = Path(
    "data/knowledge_base"
)


files = list(
    BASE_DIR.rglob("*.txt")
)

print("=" * 60)
print("DATASET INSPECTION")
print("=" * 60)

print(
    "\nTotal documents:",
    len(files)
)


print("\nDocuments by category:")

for directory in sorted(BASE_DIR.iterdir()):

    if directory.is_dir():

        count = len(
            list(directory.glob("*.txt"))
        )

        print(
            f"{directory.name:20s}: {count}"
        )


print("\nSample document")
print("-" * 60)

sample = files[0]

print("File:", sample)

print(
    sample.read_text(
        encoding="utf-8"
    )
)
