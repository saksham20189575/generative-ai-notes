# rag_pipeline.py — ShopKart RAG: evaluate & improve (Session 22 lab)
#
# Builds DIRECTLY on Session 21's multi-document pipeline. Everything from the
# previous build is kept UNCHANGED — loaders, overlap chunking, indexing,
# retrieve_policy_chunks, generate_grounded_answer, print_retrieved_chunks.
#
# What is NEW today (added BEFORE main()):
#   1. TEST_QUERIES        — realistic edge-case customer questions
#   2. build_strict_prompt / generate_strict_answer — stricter grounding + refusal
#   3. guess_category / retrieve_filtered           — optional metadata filtering
#   4. run_queries + a BASELINE vs IMPROVED main()  — before/after experiment
#
# The workflow you practice: test -> diagnose -> improve -> re-test.

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
COLLECTION_NAME = "shopkart_policy_kb_v2"  # SAME collection as Session 21 — we reuse the chunked store
DEFAULT_CHUNK_SIZE = 100  # Words per chunk — bump to 120 as an optional second iteration
DEFAULT_CHUNK_OVERLAP = 20  # Overlapping words between chunks — bump to 30 if rules keep splitting


# ===========================================================================
# STAGE 1 — DOCUMENT LOADERS: turn files on disk into cleaned text + metadata
# (unchanged from Session 21)
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
# (unchanged from Session 21)
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
# (unchanged from Session 21)
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
    print(f"PRINTING METADATA ----> {metadatas}")


def build_knowledge_base(model, collection, folder_path: str = POLICY_FOLDER) -> None:
    # The WHOLE offline pipeline in one call: load -> chunk -> embed -> store
    documents = load_all_policy_documents(folder_path)  # Stage 1 — document loaders
    chunks = create_chunks_from_documents(documents)  # Stage 2 — chunking
    index_policy_chunks(collection, model, chunks)  # Stage 3 — embed and store
    print("Knowledge base build complete.")  # Offline ingestion finished


# ===========================================================================
# STAGE 4 — RETRIEVER: embed the question and fetch the nearest chunks
# (unchanged from Session 21)
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
# (unchanged from Session 21)
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
# STAGE 6 — INSPECT: SEE what the retriever found before reading the answer
# (unchanged from Session 21)
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


# ###########################################################################
# #                       NEW IN SESSION 22 BELOW                           #
# ###########################################################################

# ===========================================================================
# NEW — STEP 1: edge-case TEST_QUERIES (run the SAME list baseline + improved)
# ===========================================================================
TEST_QUERIES = [
    "Can I return a laptop charger if the box is opened?",  # Returns — opened / electronics
    "Is UPI refund available for prepaid orders?",  # Corpus gap — must refuse, not invent
    "I returned a defective kettle on COD last week. When will the refund reach my UPI?",  # Refunds — COD timeline
    "My earphones got water damage after 8 months. Is repair covered?",  # Warranty — liquid excluded
    "Will express shipping reach my non-metro pin code in 1 day?",  # Shipping — metro only
    "I ordered at 7 PM yesterday. When will standard shipping dispatch?",  # Shipping — after 6 PM rule
    "When will I get my refund after return?",  # Refunds — not delivery (word "when" trap)
    "When will my express order arrive in a metro city?",  # Shipping — not refunds (word "when" trap)
]


# ===========================================================================
# NEW — STEP 2: stricter grounding prompt (hallucination + generation fix)
# ===========================================================================
REFUSAL = "I do not have enough information in the provided policy excerpts."  # Same line as Session 21


def build_strict_prompt(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    # Like build_grounded_prompt, but with HARDER "do not invent" rules + an exact refusal sentence
    context = ""  # One string built from all retrieved chunks
    for i, chunk in enumerate(retrieved_chunks, start=1):  # Number each excerpt for clarity
        src = chunk["metadata"].get("source", "unknown")  # File name for traceability
        cat = chunk["metadata"].get("category", "unknown")  # returns / shipping / warranty / refunds
        context += f"\nExcerpt {i} (source: {src}, category: {cat}):\n{chunk['text']}\n"

    return f"""You are ShopKart customer support.
Use ONLY the excerpts below.
Rules:
1. Do not invent numbers, payment methods, or rules not in the excerpts.
2. Do not promise coupons, instant refunds, or extra benefits not in the excerpts.
3. If the excerpts do not contain enough information, say exactly: "{REFUSAL}"
4. Keep the answer short, polite, and faithful to the excerpts.

Excerpts:
{context}

Question: {user_query}

Answer:"""


def generate_strict_answer(
    client: Groq,
    user_query: str,
    retrieved_chunks: List[Dict[str, Any]],
) -> str:
    # Same Groq call as generate_grounded_answer, but driven by the STRICTER prompt
    prompt = build_strict_prompt(user_query, retrieved_chunks)  # Build strict prompt text
    response = client.chat.completions.create(
        model=GENERATION_MODEL_NAME,  # Same Groq Llama model as before
        messages=[
            {"role": "system", "content": "Follow excerpts exactly. Never guess missing policy details."},
            {"role": "user", "content": prompt},  # Grounded user message
        ],
    )
    return response.choices[0].message.content.strip()  # Final answer string


# ===========================================================================
# NEW — STEP 3: retrieval with an OPTIONAL metadata filter by policy type
# ===========================================================================
def guess_category(query: str):
    # Simple keyword router — enough for this lab; production bots use smarter intent detection
    q = query.lower()  # Lowercase for simple keyword matching
    if "return" in q or "opened" in q or "unopened" in q:
        return "returns"  # Returns-related wording
    if "ship" in q or "express" in q or "metro" in q or "dispatch" in q or "deliver" in q:
        return "shipping"  # Shipping-related wording
    if "warranty" in q or "water" in q or "repair" in q or "liquid" in q:
        return "warranty"  # Warranty-related wording
    if "refund" in q or "cod" in q or "upi" in q or "money back" in q:
        return "refunds"  # Refunds-related wording
    return None  # No filter — search all categories


def retrieve_filtered(
    collection,
    model: SentenceTransformer,
    user_query: str,
    top_k: int = 3,
    category: str = None,
) -> List[Dict[str, Any]]:
    # Mirrors retrieve_policy_chunks but adds an OPTIONAL Chroma where={"category": ...} filter
    embedding = model.encode(
        [user_query],
        convert_to_numpy=True,
        normalize_embeddings=True,  # Must match index-time setting
    ).tolist()  # Query vector

    args = {
        "query_embeddings": embedding,  # Vector input for similarity search
        "n_results": top_k,  # How many chunks to return
        "include": ["documents", "metadatas", "distances"],  # Text, labels, scores
    }
    if category:  # Only when filtering by policy type
        args["where"] = {"category": category}  # Chroma metadata filter — search one shelf only

    results = collection.query(**args)  # Run search

    chunks = []  # Output list — SAME structure retrieve_policy_chunks returns
    for doc, meta, dist in zip(
        results["documents"][0],  # Matched chunk texts
        results["metadatas"][0],  # Metadata per chunk
        results["distances"][0],  # Distance scores
    ):
        chunks.append({"text": doc, "metadata": meta, "distance": dist})  # One ranked hit
    return chunks


# ===========================================================================
# NEW — STEP 4: run one pass of TEST_QUERIES with a chosen set of levers
# ===========================================================================
def run_queries(
    client: Groq,
    collection,
    model: SentenceTransformer,
    queries: List[str],
    top_k: int,
    use_filter: bool,
    use_strict: bool,
) -> None:
    # One full pass over the test list with the chosen top_k / filter / prompt settings
    label = f"top_k={top_k} | filter={use_filter} | strict={use_strict}"  # Settings for this pass
    print("\n" + "=" * 72)
    print("RUN:", label)
    print("=" * 72)

    for user_query in queries:
        category = guess_category(user_query) if use_filter else None  # Filter on or off
        chunks = retrieve_filtered(collection, model, user_query, top_k, category)  # Retrieve evidence
        print_retrieved_chunks(user_query, chunks)  # Always read Rank 1 here FIRST

        if use_strict:
            answer = generate_strict_answer(client, user_query, chunks)  # Improved prompt path
        else:
            answer = generate_grounded_answer(client, user_query, chunks)  # Original prompt path

        print("\nAnswer:", answer)  # The reply to compare against Rank 1
        print("-" * 72)


# ===========================================================================
# MAIN — the BASELINE vs IMPROVED before/after experiment
# ===========================================================================
def main() -> None:
    # Load the embedding model, open Chroma, and (re)build the knowledge base once
    model = create_embedding_model()  # Local BGE encoder
    collection = setup_chroma_collection()  # shopkart_policy_kb_v2 collection
    build_knowledge_base(model, collection)  # Offline load -> chunk -> embed -> upsert

    # Create the Groq client once (key from .env) and reuse it for every generation call
    client = create_groq_client()  # Authenticated using GROQ_API_KEY from the environment

    # BASELINE — mirrors Session 21: original prompt, no filter, top_k=3
    print("\n--- BASELINE (original prompt, no filter, top_k=3) ---")
    run_queries(client, collection, model, TEST_QUERIES, top_k=3, use_filter=False, use_strict=False)

    # IMPROVED — three levers together: strict prompt + category filter + top_k=5
    print("\n--- IMPROVED (strict prompt + category filter + top_k=5) ---")
    run_queries(client, collection, model, TEST_QUERIES, top_k=5, use_filter=True, use_strict=True)


if __name__ == "__main__":
    main()  # Run ingestion, then the baseline and improved passes when executed directly
