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