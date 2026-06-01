import chromadb
from sentence_transformers import SentenceTransformer
from pprint import pprint

records = [
    {"id": "doc1", "text": "Customers can return products within 30 days of delivery.",
     "metadata": {"category": "returns",  "source": "policy"}},
    {"id": "doc2", "text": "Refunds are processed within 5 to 7 business days after the return is approved.",
     "metadata": {"category": "returns",  "source": "policy"}},
    {"id": "doc3", "text": "Orders above 499 rupees qualify for free shipping.",
     "metadata": {"category": "shipping", "source": "faq"}},
    {"id": "doc4", "text": "You can reset your password from the account settings page.",
     "metadata": {"category": "account",  "source": "help_center"}},
    {"id": "doc5", "text": "Express delivery orders usually arrive within 24 to 48 hours.",
     "metadata": {"category": "shipping", "source": "faq"}},
    {"id": "doc6", "text": "If your payment fails, try another card or use UPI.",
     "metadata": {"category": "payments", "source": "help_center"}},
]
# One idea per record -> better retrieval. Parallel id/text/metadata lists feed upsert next.

# Local disk storage — survives restarts
client = chromadb.PersistentClient(path="./chroma_store")

# Open existing OR create new — idempotent
collection = client.get_or_create_collection(
    name="support_knowledge_base",
    embedding_function=None,   # we pass embeddings manually
)

print("Collection ready:", collection.name)
print("Current count:", collection.count())   # 0 on fresh run

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [r["text"]     for r in records]
ids       = [r["id"]       for r in records]
metadatas = [r["metadata"] for r in records]

document_embeddings = model.encode(
    documents, convert_to_numpy=True
).tolist()    # Chroma wants Python lists

collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=document_embeddings,
)
print("Total records now:", collection.count())   # expect 6

# 1. Row count — one number
print("Total:", collection.count())
# Wrong count -> stop and fix before querying

# 2. Sample rows — eyeball stored text + tags
print("\nPeek:")
pprint(collection.peek())

# 3. Exact id fetch — SQL WHERE id = 'doc4'
one_row = collection.get(ids=["doc4"])
print("\nExact fetch for doc4:")
pprint(one_row)

user_query = "I want to return my shoes and get my money back"

# SAME SentenceTransformer model as document ingest
query_embedding = model.encode(
    [user_query], convert_to_numpy=True
).tolist()    # list-of-lists for query_embeddings

print(f"\nQuery Embedding for '{user_query}': {query_embedding}")

results = collection.query(
    query_embeddings=query_embedding,
    n_results=3,     # top-k
)

print(f"\nFirst User Query --> {user_query}\n")

for i in range(len(results["ids"][0])):
    print(f"Rank {i+1}")
    print("  ID:",       results["ids"][0][i])
    print("  Document:", results["documents"][0][i])
    print("  Metadata:", results["metadatas"][0][i])
    if results.get("distances"):
        print("  Distance:", results["distances"][0][i])

second_query = "How do I change my login password?"

# Same model — never swap mid-lab
second_embedding = model.encode(
    [second_query], convert_to_numpy=True
).tolist()

second_results = collection.query(
    query_embeddings=second_embedding,
    n_results=2,     # smaller top-k this time
)

print(f"\nSecond User Query --> {second_query}\n")
for i in range(len(second_results["ids"][0])):
    print(f"Rank {i+1}:", second_results["documents"][0][i])
