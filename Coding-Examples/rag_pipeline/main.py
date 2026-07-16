# rag_pipeline.py — ShopKart multi-document RAG (Session 21 lab)
#
# Builds on Session 20's minimal RAG loop. The big change today:
# instead of four hardcoded policy strings, we LOAD real policy files
# (.txt / .pdf) from a folder, CLEAN them, CHUNK them with overlap, then
# feed the chunks into the SAME retrieve -> generate loop you already know.

import os  # File paths and folder listing (os.listdir, os.path.join)
import re  # Regular expressions — used to collapse extra whitespace in cleaned text
from typing import Any, Dict, List  # Type hints make function signatures self-documenting
import chromadb  # Vector database for storing and searching the chunked policy text
from sentence_transformers import SentenceTransformer  # Loads the local BGE embedding model
from groq import Groq  # Client for the hosted LLM generation API (free, OpenAI-compatible)
from dotenv import load_dotenv  # Loads key=value pairs from a local .env file into os.environ
from pypdf import PdfReader  # Extracts text from PDF files, one page at a time

# Read the local .env file once at import time so GROQ_API_KEY is available everywhere
load_dotenv()  # Looks for a .env file in the current/parent directories and populates os.environ

# ---------------------------------------------------------------------------
# Configuration — one place to change models, paths, and chunk settings
# ---------------------------------------------------------------------------
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # SAME BGE model for both indexing and querying
GENERATION_MODEL_NAME = "llama-3.1-8b-instant"  # Groq-hosted LLM used as the generator
POLICY_FOLDER = "./policy_documents"  # Folder holding the ShopKart policy .txt / .pdf files
CHROMA_PATH = "./chroma_store"  # On-disk Chroma persistence path (survives after the script ends)
COLLECTION_NAME = "shopkart_policy_kb_v2"  # New collection name — keeps chunked policies separate from Session 20
DEFAULT_CHUNK_SIZE = 100  # Words per chunk — small enough for precise retrieval
DEFAULT_CHUNK_OVERLAP = 20  # Overlapping words between consecutive chunks — keeps split rules together


# ===========================================================================
# STAGE 1 — DOCUMENT LOADERS: turn files on disk into cleaned text + metadata
# ===========================================================================
def infer_policy_category(filename: str) -> str:
    # Decide the policy area from the file NAME so each chunk can be tagged
    name = filename.lower()  # Lowercase once for case-insensitive matching
    if "return" in name:
        return "returns"  # returns_policy.txt -> "returns"
    if "shipping" in name:
        return "shipping"  # shipping_policy.txt -> "shipping"
    if "warranty" in name:
        return "warranty"  # warranty_policy.txt -> "warranty"
    if "refund" in name:
        return "refunds"  # refunds_policy.txt -> "refunds"
    return "general"  # Fallback when the file name matches no known pattern


def clean_text(raw_text: str) -> str:
    # Normalize messy text (especially from PDFs) before chunking
    text = raw_text.replace("\n", " ")  # Replace line breaks with spaces so words don't glue together
    text = re.sub(r"\s+", " ", text)  # Collapse any run of whitespace into a single space
    return text.strip()  # Remove leading/trailing whitespace


def load_txt_file(file_path: str) -> List[Dict[str, Any]]:
    # Simplest loader — read a whole .txt file into one cleaned document
    with open(file_path, "r", encoding="utf-8") as handle:  # Open as UTF-8 so accents/symbols survive
        raw_text = handle.read()  # Read the entire file into one string

    cleaned = clean_text(raw_text)  # Normalize whitespace before chunking
    filename = os.path.basename(file_path)  # Keep just the file name (not the full path) for metadata

    # Return a list with ONE document dict — same shape the PDF loader returns
    return [
        {
            "text": cleaned,  # Full cleaned policy text from this file
            "metadata": {
                "source": filename,  # Which file this text came from
                "category": infer_policy_category(filename),  # returns/shipping/warranty/refunds
                "file_type": "txt",  # Records which loader produced this document
            },
        }
    ]


def load_pdf_file(file_path: str) -> List[Dict[str, Any]]:
    # PDF loader — read text-based PDFs ONE PAGE at a time (scanned image PDFs would need OCR)
    documents: List[Dict[str, Any]] = []  # One dict per non-empty PDF page
    filename = os.path.basename(file_path)  # PDF file name for metadata
    category = infer_policy_category(filename)  # Policy area inferred from the file name
    reader = PdfReader(file_path)  # Open the PDF for page-wise text extraction

    # enumerate(..., start=1) gives human-friendly page numbers (1, 2, 3, ...)
    for page_number, page in enumerate(reader.pages, start=1):
        cleaned = clean_text(page.extract_text() or "")  # Extract page text ("" if the page has none)
        if not cleaned:  # Skip blank pages so we don't index empty chunks
            continue
        documents.append(
            {
                "text": cleaned,  # Cleaned text for this page
                "metadata": {
                    "source": filename,  # Source PDF file name
                    "category": category,  # Policy area label
                    "file_type": "pdf",  # Loader type used
                    "page": page_number,  # Page number inside the PDF
                },
            }
        )

    return documents  # All page-documents extracted from this PDF


def load_all_policy_documents(folder_path: str) -> List[Dict[str, Any]]:
    # Scan the policy folder and route each file to the correct loader by extension
    all_documents: List[Dict[str, Any]] = []  # Master list across every policy file

    for filename in sorted(os.listdir(folder_path)):  # Sorted for predictable console logs
        full_path = os.path.join(folder_path, filename)  # Build the full path to each file

        if filename.endswith(".txt"):  # TXT branch
            docs = load_txt_file(full_path)
        elif filename.endswith(".pdf"):  # PDF branch
            docs = load_pdf_file(full_path)
        else:  # Ignore anything that is not .txt or .pdf
            continue

        all_documents.extend(docs)  # Add this file's documents to the master list
        print(f"Loaded {len(docs)} document(s) from {filename}")  # Per-file loader trace

    print(f"Total loaded documents: {len(all_documents)}")  # Summary after the folder scan
    return all_documents  # Loaded documents ready for chunking


# ===========================================================================
# STAGE 2 — CHUNKING: split long documents into small, searchable units
# ===========================================================================
def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[str]:
    # Fixed-size overlap chunking measured in WORDS (simple and predictable)
    words = text.split()  # Split text into a list of words on whitespace
    if not words:  # Empty input produces no chunks
        return []

    chunks: List[str] = []  # Output list of chunk strings
    start = 0  # Index of the first word in the current chunk

    while start < len(words):  # Loop until every word has been placed in a chunk
        end = start + chunk_size  # Exclusive end index for this chunk
        chunks.append(" ".join(words[start:end]))  # Join this word slice back into one string
        if end >= len(words):  # Stop once the final chunk has been added
            break
        start += chunk_size - overlap  # Move forward, but step back by `overlap` words so they REPEAT

    return chunks  # Overlapping word-based chunks from one document


def create_chunks_from_documents(
    documents: List[Dict[str, Any]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[Dict[str, Any]]:
    # Turn loaded documents into a FLAT list of chunk records ready for Chroma
    all_chunks: List[Dict[str, Any]] = []  # Flat list of chunk dicts

    for doc_index, document in enumerate(documents):  # Each loaded file or PDF page
        for chunk_index, chunk_body in enumerate(
            chunk_text(document["text"], chunk_size, overlap)  # Split this document into chunks
        ):
            category = document["metadata"].get("category", "general")  # Policy area tag for the id
            chunk_metadata = dict(document["metadata"])  # Copy parent metadata (don't mutate the original)
            chunk_metadata["chunk_index"] = chunk_index  # Record this chunk's position in its document

            all_chunks.append(
                {
                    "id": f"{category}_{doc_index}_{chunk_index}",  # Stable, unique id (e.g. returns_0_1)
                    "text": chunk_body,  # The searchable chunk text
                    "metadata": chunk_metadata,  # source, category, file_type, chunk_index
                }
            )

    print(f"Total chunks created: {len(all_chunks)}")  # Should be greater than 4 in this lab
    return all_chunks  # Ready for embedding and upsert


# ===========================================================================
# STAGE 3 — INDEX: embed the chunks and store them in Chroma (offline, once)
# ===========================================================================
def create_embedding_model() -> SentenceTransformer:
    # Load the local BGE embedding model once — reuse for every encode call in this script
    return SentenceTransformer(EMBEDDING_MODEL_NAME)  # Downloads ~130MB BGE model on first run


def setup_chroma_collection():
    # Connect to on-disk Chroma storage so the index survives after the script ends
    client = chromadb.PersistentClient(path=CHROMA_PATH)  # Local persistent database folder

    # Open or create the chunked-policy collection
    return client.get_or_create_collection(
        name=COLLECTION_NAME,  # Named bucket for the chunked ShopKart policies
        embedding_function=None,  # We pass embeddings manually with SentenceTransformer
    )


def index_policy_chunks(
    collection,
    model: SentenceTransformer,
    chunks: List[Dict[str, Any]],
) -> None:
    # Embed every chunk and write all rows into Chroma in one batch
    if not chunks:  # Guard against an empty ingestion result
        print("No chunks to index.")
        return

    ids = [row["id"] for row in chunks]  # One unique id per chunk
    documents = [row["text"] for row in chunks]  # Plain text stored and returned in search
    metadatas = [row["metadata"] for row in chunks]  # category, source, chunk_index per row

    # Encode all chunk texts to vectors — SAME model and settings will be used for queries later
    embeddings = model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True,  # Recommended for BGE so cosine-style similarity behaves well
    ).tolist()  # Chroma expects plain Python lists, not numpy arrays

    # upsert = insert new ids OR update existing ones — safe to rerun
    collection.upsert(
        ids=ids,  # Primary keys
        documents=documents,  # Human-readable chunk bodies
        metadatas=metadatas,  # Policy labels per chunk
        embeddings=embeddings,  # Meaning vectors used for similarity search
    )

    print(f"Indexed {collection.count()} chunks into {COLLECTION_NAME}.")  # Post-upsert count


def build_knowledge_base(model, collection, folder_path: str = POLICY_FOLDER) -> None:
    # The WHOLE offline pipeline in one call: load -> chunk -> embed -> store
    documents = load_all_policy_documents(folder_path)  # Stage 1 — document loaders
    chunks = create_chunks_from_documents(documents)  # Stage 2 — chunking
    index_policy_chunks(collection, model, chunks)  # Stage 3 — embed and store
    print("Knowledge base build complete.")  # Offline ingestion finished


# ===========================================================================
# STAGE 4 — RETRIEVER: embed the question and fetch the nearest chunks
# ===========================================================================
def retrieve_policy_chunks(
    collection,
    model: SentenceTransformer,
    user_query: str,
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    # Convert the customer's question into a vector using the SAME BGE settings as indexing
    query_embedding = model.encode(
        [user_query],
        convert_to_numpy=True,
        normalize_embeddings=True,  # Must match the index-time setting above
    ).tolist()  # Batch of one query as a plain list

    # Ask Chroma for the nearest stored chunk vectors to this question vector
    results = collection.query(
        query_embeddings=query_embedding,  # Query as numbers — not the raw string
        n_results=top_k,  # How many chunks to return (top-k). 3 because each file now makes many chunks
        include=["documents", "metadatas", "distances"],  # Ask for text, tags, and similarity scores
    )

    retrieved = []  # Clean evidence list we will pass to the generator

    # Loop through each rank in the top-k result lists — index 0 is the best match
    for doc, meta, dist in zip(
        results["documents"][0],  # Matched chunk texts
        results["metadatas"][0],  # Metadata aligned with each match
        results["distances"][0],  # Distance scores — lower usually means closer meaning
    ):
        retrieved.append(
            {
                "text": doc,  # Retrieved chunk text
                "metadata": meta,  # source, category, chunk_index labels
                "distance": dist,  # Similarity score for inspection
            }
        )

    return retrieved  # Top-k policy excerpts for this question


# ===========================================================================
# STAGE 5 — GENERATOR: write a grounded answer using only the retrieved text
# ===========================================================================
def create_groq_client() -> Groq:
    # Read the API key from the environment (populated from .env by load_dotenv above)
    api_key = os.environ.get("GROQ_API_KEY")  # Never hard-code secrets in source

    # Fail fast with a clear message instead of a confusing auth error deep in the API call
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Create a .env file next to rag_pipeline.py containing:\n"
            "    GROQ_API_KEY=your_key_here"
        )

    return Groq(api_key=api_key)  # Authenticated client for the generation step


def build_grounded_prompt(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    # Stitch the retrieved excerpts into one labeled context block the LLM can read
    context_block = ""  # Start empty — append each chunk with source + category labels
    for index, chunk in enumerate(retrieved_chunks, start=1):  # Number excerpts for clarity
        metadata = chunk.get("metadata") or {}  # Guard: metadata may be missing or None
        source_name = metadata.get("source", "unknown")  # Which policy file this came from
        category = metadata.get("category", "unknown")  # Which policy area this came from
        text = chunk.get("text", "")  # Guard: avoid KeyError if a chunk has no text
        context_block += f"\nExcerpt {index} (source: {source_name}, category: {category}):\n{text}\n"

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


def generate_grounded_answer(
    client: Groq,
    user_query: str,
    retrieved_chunks: List[Dict[str, Any]],
) -> str:
    # Build the grounded prompt from the retrieved evidence
    prompt = build_grounded_prompt(user_query, retrieved_chunks)  # Context + question + rules

    # Call the hosted LLM on Groq — the generator step of RAG
    response = client.chat.completions.create(
        model=GENERATION_MODEL_NAME,  # Which Groq LLM writes the final reply
        messages=[
            {
                "role": "system",  # High-level behavior instruction
                "content": "You are a precise ShopKart support assistant. Follow the policy excerpts exactly.",
            },
            {"role": "user", "content": prompt},  # Grounded prompt with the evidence block
        ],
    )

    # Extract the assistant's text from the API response object
    return response.choices[0].message.content.strip()  # Final grounded answer string


# ===========================================================================
# STAGE 6 — INSPECT + WIRE THE LOOP: retrieve -> print ranks -> generate
# ===========================================================================
def print_retrieved_chunks(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> None:
    # Quality-check helper — SEE what the retriever found before reading the LLM answer
    print("\n" + "=" * 72)  # Visual divider in terminal output
    print(f"Customer question: {user_query}")  # Echo the query under inspection
    print("=" * 72)  # Closing divider line

    for rank, chunk in enumerate(retrieved_chunks, start=1):  # Rank 1 = best match
        print(f"\nRank {rank}")  # Human-friendly rank label
        print(f"  Category : {chunk['metadata'].get('category')}")  # returns/shipping/warranty/refunds
        print(f"  Source   : {chunk['metadata'].get('source')}")  # File name the chunk came from
        print(f"  Distance : {chunk['distance']:.4f}")  # Lower usually = closer vector match
        print(f"  Text     : {chunk['text']}")  # The actual chunk text retrieved


def answer_with_rag(
    client: Groq,
    collection,
    model: SentenceTransformer,
    user_query: str,
    top_k: int = 3,
) -> str:
    # Step A — Retrieve relevant ShopKart policy chunks
    retrieved_chunks = retrieve_policy_chunks(
        collection=collection,  # Chroma collection holding the chunked policies
        model=model,  # Shared embedding model
        user_query=user_query,  # Customer's natural-language question
        top_k=top_k,  # How many excerpts to fetch
    )

    # Step B — Print retrieval results so you can judge intent match BEFORE generation
    print_retrieved_chunks(user_query, retrieved_chunks)  # Inspection step — not optional in learning

    # Step C — Generate a grounded natural-language answer from the retrieved evidence
    return generate_grounded_answer(
        client=client,  # Groq client
        user_query=user_query,  # Original question
        retrieved_chunks=retrieved_chunks,  # Evidence from the retriever
    )


# ===========================================================================
# MAIN — ingest once, then answer a spread of demo questions
# ===========================================================================
def main() -> None:
    # Load the embedding model once and reuse it for the whole run
    model = create_embedding_model()  # Local BGE encoder

    # Open (or create) the persistent Chroma collection on disk
    collection = setup_chroma_collection()  # Handle for storing/searching vectors

    # Offline ingestion: load files -> chunk -> embed -> store (run once per content change)
    build_knowledge_base(model, collection)  # Persists ids, documents, metadata, embeddings

    # Create the Groq client once (key from .env) and reuse it for every generation call
    client = create_groq_client()  # Authenticated using GROQ_API_KEY from the environment

    # Representative customer questions spanning returns, shipping, warranty, refunds
    demo_queries = [
        "I received my phone case yesterday unopened. How many days do I have to return it?",
        "Will express shipping reach my address in a metro city by tomorrow?",
        "My wireless earphones stopped working after 10 months. Is repair covered?",
        "I returned a defective kettle on COD last week. When will the refund reach my UPI?",
    ]

    # Run each demo query through the full RAG loop (retrieve + inspect + generate)
    for user_query in demo_queries:
        print("\n\n" + "#" * 72)  # Section header per question
        print("QUESTION:", user_query)  # Show the current customer line

        answer = answer_with_rag(
            client=client,  # Generator client
            collection=collection,  # Retriever storage
            model=model,  # Embedding model
            user_query=user_query,  # Customer's natural-language question
            top_k=3,  # Fetch three nearest policy chunks
        )

        print("\nFinal grounded answer:")  # Label the final output
        print(answer)  # Print the grounded ShopKart reply


if __name__ == "__main__":
    main()  # Run ingestion then the demo queries when this file is executed directly
