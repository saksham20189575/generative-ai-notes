# shopkart_rag.py — minimal RAG loop for ShopKart customer support

import os  # Read environment variables like GROQ_API_KEY
from typing import Any, Dict, List  # Type hints for the retriever's return value
import chromadb  # Vector database for storing and searching policy chunks
from sentence_transformers import SentenceTransformer  # Loads the BGE embedding model for retriever
from groq import Groq  # Client for LLM generation API calls (free, OpenAI-compatible)
from dotenv import load_dotenv  # Loads key=value pairs from a local .env file into os.environ

# Read the local .env file once at import time so GROQ_API_KEY is available everywhere
load_dotenv()  # Looks for a .env file in the current/parent directories and populates os.environ

# ---------------------------------------------------------------------------
# ShopKart policy records — these are our knowledge sources for this lab
# Each dict becomes one row in Chroma: id, text, metadata
# ---------------------------------------------------------------------------
POLICY_RECORDS = [
    {  # Returns policy chunk
        "id": "shopkart_returns_1",  # Unique primary key for this policy row
        "text": (
            "Unopened items may be returned within 7 calendar days of delivery. "
            "Opened or used items are not eligible unless defective."
        ),  # Human-readable returns rule — source of truth for return questions
        "metadata": {"category": "returns", "source": "returns_policy"},  # Tags for display and later filtering
    },
    {  # Shipping policy chunk
        "id": "shopkart_shipping_1",  # Unique id for shipping row
        "text": (
            "Standard delivery takes 3 to 5 business days after dispatch. "
            "Express delivery (paid) arrives in 1 to 2 business days in metro cities only."
        ),  # Shipping timelines customers ask about often
        "metadata": {"category": "shipping", "source": "shipping_policy"},  # Shipping category tag
    },
    {  # Warranty policy chunk
        "id": "shopkart_warranty_1",  # Unique id for warranty row
        "text": (
            "Electronics carry a 12-month manufacturer warranty from the date of delivery. "
            "Warranty does not cover physical damage or liquid exposure."
        ),  # Warranty coverage and exclusions
        "metadata": {"category": "warranty", "source": "warranty_policy"},  # Warranty category tag
    },
    {  # Refund policy chunk
        "id": "shopkart_refunds_1",  # Unique id for refund row
        "text": (
            "Refunds are credited within 5 to 7 business days after the returned item "
            "passes warehouse verification. Cash-on-delivery orders are refunded to the "
            "original UPI or bank account only."
        ),  # Refund timing and COD path
        "metadata": {"category": "refunds", "source": "refunds_policy"},  # Refunds category tag
    },
]

# Embedding model name — MUST stay the same for documents and every query
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # Free BGE model from Hugging Face

# LLM model name for generation — free Groq model; swap for any model Groq lists
GENERATION_MODEL_NAME = "llama-3.3-70b-versatile"  # Groq-hosted LLM used as the generator


def create_embedding_model() -> SentenceTransformer:
    # Load the local BGE embedding model once — reuse for all encode calls in this script
    return SentenceTransformer(EMBEDDING_MODEL_NAME)  # Downloads ~130MB BGE model on first run

def setup_chroma_collection():
    # Connect to on-disk Chroma storage in ./chroma_store (survives after script ends)
    client = chromadb.PersistentClient(path="./chroma_store")  # Local persistent database folder

    # Open or create the ShopKart policy collection — separate name from older demo collections
    collection = client.get_or_create_collection(
        name="shopkart_policy_kb",  # Named bucket for ShopKart policy rows
        embedding_function=None,  # We pass embeddings manually — same teaching pattern as before
    )

    return collection  # Return collection handle for upsert and query

  # Expect 4 after first successful run

def index_policy_records(collection, model: SentenceTransformer) -> None:
    # Build parallel lists from POLICY_RECORDS — index alignment matters for upsert
    ids = [row["id"] for row in POLICY_RECORDS]  # One unique id per policy chunk
    documents = [row["text"] for row in POLICY_RECORDS]  # Plain text stored and returned in search
    metadatas = [row["metadata"] for row in POLICY_RECORDS]  # Category and source tags per row

    # Encode all policy texts to vectors in one batch — same model as queries later
    # normalize_embeddings=True is recommended for BGE so cosine-style similarity behaves well
    embeddings = model.encode(documents, convert_to_numpy=True, normalize_embeddings=True).tolist()  # Chroma expects Python lists

    # Write all rows into Chroma — upsert is safe to rerun (updates by id if already present)
    collection.upsert(
        ids=ids,  # Primary keys
        documents=documents,  # Readable policy sentences
        metadatas=metadatas,  # Tags stored alongside each row
        embeddings=embeddings,  # Meaning vectors used for similarity search
    )

    print(f"Indexed {collection.count()} ShopKart policy records.")

def retrieve_policy_chunks(
    collection,
    model: SentenceTransformer,
    user_query: str,
    top_k: int = 2,
) -> List[Dict[str, Any]]:
    # Convert the customer's question into an embedding vector using the SAME BGE model as indexing
    query_embedding = model.encode([user_query], convert_to_numpy=True, normalize_embeddings=True).tolist()  # Batch of one query

    # Ask Chroma for the nearest stored policy vectors to this question vector
    results = collection.query(
        query_embeddings=query_embedding,  # Query as numbers — not raw string
        n_results=top_k,  # How many chunks to return (top-k)
        include=["documents", "metadatas", "distances"],  # Ask for text, tags, and scores
    )

    retrieved = []  # Clean list we will pass to the generator

    # Loop through each rank in the top-k result lists — index 0 is best match
    for doc, meta, dist in zip(
        results["documents"][0],  # Matched policy text strings
        results["metadatas"][0],  # Metadata dicts aligned with each match
        results["distances"][0],  # Distance scores — lower usually means closer meaning
    ):
        retrieved.append(
            {
                "text": doc,  # Policy excerpt text
                "metadata": meta,  # Source and category labels
                "distance": dist,  # Similarity score for inspection
            }
        )

    return retrieved  # List of dicts — retriever output for this query


def create_groq_client() -> Groq:
    # Read the API key from the environment (populated from .env by load_dotenv above)
    api_key = os.environ.get("GROQ_API_KEY")  # Never hard-code secrets in source

    # Fail fast with a clear message instead of a confusing auth error deep in the API call
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Create a .env file next to rag.py containing:\n"
            "    GROQ_API_KEY=your_key_here"
        )

    return Groq(api_key=api_key)  # Authenticated client for the generation step

def build_grounded_prompt(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    # Stitch retrieved policy excerpts into one context block the LLM can read
    context_block = ""  # Start empty — append each chunk with a label
    for index, chunk in enumerate(retrieved_chunks, start=1):  # Number chunks for clarity
        metadata = chunk.get("metadata") or {}  # Guard: metadata may be missing or None
        source_name = metadata.get("source", "unknown")  # Which policy file this came from
        text = chunk.get("text", "")  # Guard: avoid KeyError if a chunk has no text
        context_block += f"\nExcerpt {index} (source: {source_name}):\n{text}\n"  # One labeled paragraph

    # If retrieval returned nothing, tell the model explicitly so it triggers the "not enough info" rule
    if not context_block:
        context_block = "\n(No policy excerpts were retrieved for this question.)\n"

    # Full instruction prompt — rules + evidence + question
    prompt = f"""You are ShopKart customer support.
    Answer the customer's question using ONLY the policy excerpts below.
    Rules:
    1. Do not invent numbers, timelines, or eligibility rules not present in the excerpts.
    2. If the excerpts do not contain enough information, say:
    "I do not have enough information in the provided policy excerpts."
    3. Keep the answer short, polite, and clear.
    4. Mention important conditions (opened vs unopened, metro-only express, COD refund path) when they appear in the excerpts.

    Policy excerpts:
    {context_block}

    Customer question:
    {user_query}

    Final answer:"""

    return prompt  # String ready to send to the LLM API


def generate_grounded_answer(client: Groq, user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    # Build the grounded prompt from retrieved evidence
    prompt = build_grounded_prompt(user_query, retrieved_chunks)  # Context + question + rules

    # Call the hosted LLM on Groq — generator step of RAG
    response = client.chat.completions.create(
        model=GENERATION_MODEL_NAME,  # Which Groq LLM writes the final reply
        messages=[
            {
                "role": "system",  # High-level behavior instruction
                "content": "You are a precise ShopKart support assistant. Follow the policy excerpts exactly.",
            },
            {"role": "user", "content": prompt},  # Grounded prompt with evidence block
        ],
    )

    # Extract assistant text from the API response object
    return response.choices[0].message.content.strip()  # Final grounded answer string

def print_retrieved_chunks(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> None:
    # Debug helper — show what the retriever found before reading the LLM answer
    print("\n" + "=" * 72)  # Visual divider in terminal output
    print(f"Customer question: {user_query}")  # Echo the query
    print("=" * 72)  # Closing divider line

    for rank, chunk in enumerate(retrieved_chunks, start=1):  # Rank 1 = best match
        print(f"\nRank {rank}")  # Human-friendly rank label
        print(f"  Source   : {chunk['metadata'].get('source')}")  # Policy source tag
        print(f"  Category : {chunk['metadata'].get('category')}")  # Returns/shipping/etc.
        print(f"  Distance : {chunk['distance']:.4f}")  # Lower usually = closer vector match
        print(f"  Text     : {chunk['text']}")  # Actual policy excerpt retrieved


def answer_with_rag(
    client: Groq,
    collection,
    model: SentenceTransformer,
    user_query: str,
    top_k: int = 2,
) -> str:
    # Step A — Retrieve relevant ShopKart policy excerpts
    retrieved_chunks = retrieve_policy_chunks(
        collection=collection,  # Chroma collection holding policy rows
        model=model,  # Shared embedding model
        user_query=user_query,  # Customer's natural-language question
        top_k=top_k,  # How many excerpts to fetch
    )

    # Step B — Print retrieval results so you can judge intent match before generation
    print_retrieved_chunks(user_query, retrieved_chunks)  # Inspection step — not optional in learning

    # Step C — Generate grounded natural-language answer from retrieved evidence
    grounded_answer = generate_grounded_answer(
        client=client,  # Groq client
        user_query=user_query,  # Original question
        retrieved_chunks=retrieved_chunks,  # Evidence from retriever
    )

    return grounded_answer  # Final reply to show the customer


def main() -> None:
    # Load the embedding model once and reuse it for the whole run
    model = create_embedding_model()  # Local BGE encoder

    # Open (or create) the persistent Chroma collection on disk
    collection = setup_chroma_collection()  # Handle for storing/searching vectors

    # Encode every policy record and write all embeddings into ChromaDB
    index_policy_records(collection, model)  # Persists ids, documents, metadata, embeddings

    # print("Count:", collection.count())  # Should be 4
    # print("Peek sample:", collection.peek())  # Eyeball ids and document text

    # Create the Groq client once (key from .env) and reuse it for every generation call
    client = create_groq_client()  # Authenticated using GROQ_API_KEY from the environment

    # Run a sample question through the full RAG loop to confirm everything is wired up
    sample_query = "How many days do I have to return an item?"  # Example customer question
    sample_answer = answer_with_rag(
        client=client,  # Generator client
        collection=collection,  # Retriever storage
        model=model,  # Embedding model
        user_query=sample_query,  # Customer's natural-language question
        top_k=3,  # Fetch three nearest policy chunks
    )

    print(f"\nGrounded answer:\n{sample_answer}")  # Final RAG output for the sample question

    # Representative customer questions spanning returns, shipping, warranty, refunds
    demo_queries = [
        "I received my phone case yesterday unopened. How many days do I have to return it?",
        "Will express shipping reach my address in a metro city by tomorrow?",
        "My wireless earphones stopped working after 10 months. Is repair covered?",
        "I returned a defective kettle on COD last week. When will the refund reach my UPI?",
    ]

    # Run each demo query through the full RAG loop (retrieve + generate)
    for user_query in demo_queries:
        print("\n\n" + "#" * 72)  # Section header per question
        print("QUESTION:", user_query)  # Show current test question

        print("\n--- RAG (retrieve + generate) ---")  # Grounded pipeline label
        rag_answer = answer_with_rag(
            client=client,  # Generator client
            collection=collection,  # Retriever storage
            model=model,  # Embedding model
            user_query=user_query,  # Customer's natural-language question
            top_k=2,  # Fetch two nearest policy chunks
        )
        print("\nFinal grounded answer:")  # Label final output
        print(rag_answer)  # Print grounded answer

if __name__ == "__main__":
    main()  # Run the indexing pipeline when this file is executed directly