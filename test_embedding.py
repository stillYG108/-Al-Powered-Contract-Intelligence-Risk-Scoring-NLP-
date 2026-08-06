"""
Day 1 Task: Embedding model testing
Member 6 - Vector Search / Infra Engineer
"""


from sentence_transformers import SentenceTransformer

def test_embedding_generation():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    sample_clause = "India is a diverse democratic country in South Asia with New Delhi as its capital."

    embedding = model.encode(sample_clause)

    print(f"Embedding generated successfully!")
    print(f"Embedding dimension: {embedding.shape}")

    assert embedding.shape[0] == 384, "Embedding dimension mismatch...!"
    print("Test passed successfully...!")

if __name__ == "__main__":
    test_embedding_generation()