# Building a RAG Pipeline

## Context of This Session

In the previous session, you built a **minimal RAG loop** for **ShopKart** — four policy strings in code, **BGE** embeddings, **Chroma** retrieval, **Groq** generation.

Today you replace those hardcoded strings with **real policy files**. You add **document loaders** and **chunking**, then plug the result into the **same retrieve → generate loop**.

**In this session, you will:**

- Load **TXT** and **PDF** policy files from a folder
- **Clean** and **chunk** documents into searchable units
- **Index** multiple policy sources in Chroma with metadata
- Run the **full ShopKart assistant** end-to-end on support questions

The lab **is** the session — you build and run **`rag_pipeline.py`**, then read retrieval output in the terminal.

---

## ShopKart — From Four Strings to Four Files

| Policy area | File | Minimal lab | Today |
|---|---|---|---|
| **Returns** | `returns_policy.txt` | One string in code | Multi-paragraph file → many chunks |
| **Shipping** | `shipping_policy.txt` | One string in code | Loaded + chunked |
| **Warranty** | `warranty_policy.txt` | One string in code | Loaded + chunked |
| **Refunds** | `refunds_policy.txt` | One string in code | Loaded + chunked |

| Stage | Previous lab | Today |
|---|---|---|
| **Input** | `POLICY_RECORDS` list | `policy_documents/` folder |
| **Ingestion** | Manual copy-paste | **Loaders** + light **cleaning** |
| **Chunks** | 4 rows (one per area) | Many rows via **overlap chunking** |
| **Online loop** | BGE + Chroma + Groq | **Unchanged** |

![ShopKart evolution from four in-code policy strings to four real files in policy_documents — many chunks per file feed shopkart_policy_kb_v2 while the online BGE + Chroma + Groq loop stays unchanged](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-01-four-strings-to-files.png)

- **Document loader**
  - **Official Definition:** A component that reads content from an external source (file, URL) and returns text for processing.
  - **In Simple Words:** The **file opener** that brings policy PDFs and TXT files into Python.
  - **Real-Life Example:** A receptionist collecting fee-refund notices from a cupboard before counsellors answer queries.

- **Chunking**
  - **Official Definition:** Splitting a large document into smaller segments stored and retrieved independently.
  - **In Simple Words:** Cutting a policy booklet into **revision cards** — one main rule per card.
  - **Real-Life Example:** Splitting a train timetable by station so *"Kanpur arrivals"* does not pull the whole national schedule.

- **Ingestion**
  - **Official Definition:** The offline pipeline that loads documents, prepares text, embeds chunks, and stores them in a vector index.
  - **In Simple Words:** The **filing step** before anyone asks a question.
  - **Real-Life Example:** Pinning typed hostel rules behind the desk before opening for admissions.

**Why files must be prepared first:** Whole documents are too large for precise search, too noisy from PDF extraction, and too costly to send to the LLM. **Ingestion** runs **offline** once; customer questions use the **online** loop you already know.

**Chunk boundary note:** A bad split can separate *"not eligible"* from *"unless defective"* into different chunks — **overlap** reduces that risk. Swap any `.txt` for a text-based `.pdf`; the same loader path handles both.

![Offline ingestion pipeline — policy files go through load, clean, chunk, BGE embed, and Chroma store once; each customer question then runs retrieve → Groq → answer on the indexed chunks](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-02-ingestion-pipeline.png)

### Loaders and Chunking — Quick Rules

- **TXT:** read file with `open()` — simplest loader for this lab.
- **PDF:** use **`pypdf`** / **`PdfReader`** — one page at a time. Scanned image PDFs need OCR; today use text-based files.
- **Metadata:** infer **`category`** from file name (`returns_policy.txt` → **returns**). Labels like **`source`** and **`category`** are stored with each chunk so you can trace which policy file supplied an excerpt.
- **Chunk defaults:** **100 words** per chunk, **20 words** overlap — keeps split rules from losing context (e.g. *"not eligible unless defective"*).
- **Too large / too small chunks** hurt retrieval; systematic tuning comes in a **later** session. Today you use a sensible default and **inspect Rank 1 text** in the terminal.

![Document loaders for TXT and PDF — open() for text files, pypdf PdfReader for PDF pages, with category metadata inferred from filenames like returns_policy.txt](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-03-document-loaders.png)

![Overlap chunking with 100 words per chunk and 20-word tail repeat — shared overlap keeps split rules like eligibility exceptions from losing context across boundaries](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-04-overlap-chunking.png)

---

## Project Setup

```bash
mkdir shopkart_rag_pipeline
cd shopkart_rag_pipeline
pip install chromadb sentence-transformers groq python-dotenv pypdf
```

```text
shopkart_rag_pipeline/
├── policy_documents/     # four policy txt files
├── .env                  # GROQ_API_KEY
├── rag_pipeline.py
└── chroma_store/         # auto-created
```

![shopkart_rag_pipeline project layout — policy_documents folder with four txt files, rag_pipeline.py, .env for GROQ_API_KEY, and auto-created chroma_store](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-05-project-structure.png)

**`.env`:** `GROQ_API_KEY=your-key-here` — never commit to Git.

### Policy Files (create these four)

Short multi-paragraph files — enough to require chunking, same ShopKart rules as the minimal lab.

**`returns_policy.txt`**

```text
ShopKart Returns Policy. Unopened items in original packaging may be returned within 7 calendar days of delivery. Return requests must be raised on the app before the window closes.
Opened or used items are not eligible unless defective or damaged on arrival. Defect claims need photos within 48 hours of delivery. Electronics must pass warehouse quality check. Personal care and opened software keys cannot be returned unless defective.
```

**`shipping_policy.txt`**

```text
ShopKart Shipping Policy. Standard delivery takes 3 to 5 business days after dispatch on business days only.
Express delivery is paid and arrives in 1 to 2 business days in metro cities only. Non-metro pin codes are not eligible for express timelines.
Orders after 6 PM dispatch next business day. Customers receive tracking links once the courier picks up the package.
```

**`warranty_policy.txt`**

```text
ShopKart Warranty Policy. Electronics carry a 12-month manufacturer warranty from delivery date for manufacturing defects under normal use.
Warranty does not cover physical damage, liquid exposure, unauthorised repair, or misuse. Claims need invoice, serial number, and photos within the warranty period.
```

**`refunds_policy.txt`**

```text
ShopKart Refund Policy. Refunds are credited within 5 to 7 business days after the returned item passes warehouse verification.
Cash-on-delivery orders are refunded to the original UPI or bank account only. Partial refunds may apply for missing packaging or accessories. Track status in the ShopKart app under Orders.
```

---

## Build `rag_pipeline.py`

Create one file in order: **loaders → chunking → index → RAG loop**.

### Imports, Loaders, and Chunking

```python
# rag_pipeline.py — ShopKart multi-document RAG

import os  # File paths and folder listing
import re  # Collapse extra whitespace in cleaned text
from typing import List, Dict, Any  # Type hints for function signatures
import chromadb  # Vector database for chunked policy storage
from sentence_transformers import SentenceTransformer  # Local BGE embedding model
from groq import Groq  # Hosted LLM client for generation
from dotenv import load_dotenv  # Load GROQ_API_KEY from .env safely
from pypdf import PdfReader  # Extract text from PDF files page by page

load_dotenv()  # Read API key before any Groq call

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"  # Same BGE model for index and query
GENERATION_MODEL_NAME = "llama-3.1-8b-instant"  # Groq Llama model for grounded replies
POLICY_FOLDER = "./policy_documents"  # Folder with ShopKart policy txt/pdf files
CHROMA_PATH = "./chroma_store"  # On-disk Chroma persistence path
COLLECTION_NAME = "shopkart_policy_kb_v2"  # Collection for chunked policies
DEFAULT_CHUNK_SIZE = 100  # Words per chunk
DEFAULT_CHUNK_OVERLAP = 20  # Overlapping words between consecutive chunks


def infer_policy_category(filename: str) -> str:
    name = filename.lower()  # Case-insensitive file name match
    if "return" in name: return "returns"  # Returns policy label
    if "shipping" in name: return "shipping"  # Shipping policy label
    if "warranty" in name: return "warranty"  # Warranty policy label
    if "refund" in name: return "refunds"  # Refunds policy label
    return "general"  # Fallback when name pattern does not match


def clean_text(raw_text: str) -> str:
    text = raw_text.replace("\n", " ")  # Replace line breaks with spaces
    text = re.sub(r"\s+", " ", text)  # Collapse repeated spaces to one
    return text.strip()  # Remove leading and trailing whitespace


def load_txt_file(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as handle:  # Open TXT as UTF-8
        raw_text = handle.read()  # Read entire file into one string
    cleaned = clean_text(raw_text)  # Normalize whitespace before chunking
    filename = os.path.basename(file_path)  # File name only for metadata
    return [{
        "text": cleaned,  # Full cleaned policy text from this file
        "metadata": {
            "source": filename,  # Which file this text came from
            "category": infer_policy_category(filename),  # returns/shipping/warranty/refunds
            "file_type": "txt",  # Loader type used
        },
    }]


def load_pdf_file(file_path: str) -> List[Dict[str, Any]]:
    documents: List[Dict[str, Any]] = []  # One dict per non-empty PDF page
    filename = os.path.basename(file_path)  # PDF file name for metadata
    category = infer_policy_category(filename)  # Policy area from file name
    reader = PdfReader(file_path)  # Open PDF for page-wise text extraction
    for page_number, page in enumerate(reader.pages, start=1):  # Loop from page 1
        cleaned = clean_text(page.extract_text() or "")  # Extract and clean page text
        if not cleaned:  # Skip blank pages
            continue
        documents.append({
            "text": cleaned,  # Cleaned text for this page
            "metadata": {
                "source": filename,  # Source PDF file name
                "category": category,  # Policy area label
                "file_type": "pdf",  # Loader type used
                "page": page_number,  # Page number inside the PDF
            },
        })
    return documents  # All page-documents from this PDF


def load_all_policy_documents(folder_path: str) -> List[Dict[str, Any]]:
    all_documents: List[Dict[str, Any]] = []  # Master list across all policy files
    for filename in sorted(os.listdir(folder_path)):  # Sorted for predictable console logs
        full_path = os.path.join(folder_path, filename)  # Build full path to each file
        if filename.endswith(".txt"):  # TXT loader branch
            docs = load_txt_file(full_path)
        elif filename.endswith(".pdf"):  # PDF loader branch
            docs = load_pdf_file(full_path)
        else:  # Ignore unsupported files
            continue
        all_documents.extend(docs)  # Add this file's documents to master list
        print(f"Loaded {len(docs)} document(s) from {filename}")  # Loader trace per file
    print(f"Total loaded documents: {len(all_documents)}")  # Summary after folder scan
    return all_documents  # Loaded documents ready for chunking


def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_CHUNK_OVERLAP) -> List[str]:
    words = text.split()  # Split text into words on whitespace
    if not words:  # Empty input produces no chunks
        return []
    chunks: List[str] = []  # Output chunk strings
    start = 0  # Start index in the words list
    while start < len(words):  # Loop until all words are chunked
        end = start + chunk_size  # Exclusive end index for this chunk
        chunks.append(" ".join(words[start:end]))  # Join word slice into one chunk
        if end >= len(words):  # Stop after the final chunk
            break
        start += chunk_size - overlap  # Move forward with overlap stride
    return chunks  # Overlapping word-based chunks from one document


def create_chunks_from_documents(
    documents: List[Dict[str, Any]],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[Dict[str, Any]]:
    all_chunks: List[Dict[str, Any]] = []  # Flat list of chunk records for Chroma
    for doc_index, document in enumerate(documents):  # Each loaded file or PDF page
        for chunk_index, chunk_body in enumerate(chunk_text(document["text"], chunk_size, overlap)):
            category = document["metadata"].get("category", "general")  # Policy area tag
            chunk_metadata = dict(document["metadata"])  # Copy parent metadata
            chunk_metadata["chunk_index"] = chunk_index  # Position within parent document
            all_chunks.append({
                "id": f"{category}_{doc_index}_{chunk_index}",  # Stable unique chunk id
                "text": chunk_body,  # Searchable chunk text
                "metadata": chunk_metadata,  # source, category, file_type, chunk_index
            })
    print(f"Total chunks created: {len(all_chunks)}")  # Should be greater than 4 in this lab
    return all_chunks  # Ready for embedding and upsert
```

**How the code works:**

- **`load_all_policy_documents`** scans **`policy_documents`** for `.txt` and `.pdf`.
- **`clean_text`** normalizes PDF/TXT noise before chunking.
- **`chunk_text`** uses fixed-size **overlap** chunking — change **`DEFAULT_CHUNK_SIZE`** only if you want to experiment after the first successful run.

![build_knowledge_base offline index — load_all_policy_documents, create_chunks_from_documents, BGE encode, and upsert into shopkart_policy_kb_v2 with category_doc_chunk ids](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-06-build-knowledge-base.png)

### Index, Retriever, and Generator

```python
def create_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)  # Load BGE once for all encode calls


def setup_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)  # Persistent on-disk vector store
    return client.get_or_create_collection(
        name=COLLECTION_NAME,  # Named bucket for chunked ShopKart policies
        embedding_function=None,  # We pass embeddings manually with SentenceTransformer
    )


def index_policy_chunks(collection, model: SentenceTransformer, chunks: List[Dict[str, Any]]) -> None:
    if not chunks:  # Guard against empty ingestion result
        print("No chunks to index.")
        return
    ids = [row["id"] for row in chunks]  # Unique id per chunk
    documents = [row["text"] for row in chunks]  # Plain text stored and returned in search
    metadatas = [row["metadata"] for row in chunks]  # category, source, chunk_index per row
    embeddings = model.encode(documents, convert_to_numpy=True).tolist()  # BGE vectors
    collection.upsert(
        ids=ids,  # Primary keys
        documents=documents,  # Human-readable chunk bodies
        metadatas=metadatas,  # Policy labels per chunk
        embeddings=embeddings,  # Meaning vectors for similarity search
    )
    print(f"Indexed {collection.count()} chunks into {COLLECTION_NAME}.")  # Post-upsert count


def build_knowledge_base(model, collection, folder_path: str = POLICY_FOLDER) -> None:
    documents = load_all_policy_documents(folder_path)  # Document loader stage
    chunks = create_chunks_from_documents(documents)  # Chunking stage
    index_policy_chunks(collection, model, chunks)  # Embed and store stage
    print("Knowledge base build complete.")  # Offline ingestion finished


def retrieve_policy_chunks(collection, model, user_query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    query_embedding = model.encode([user_query], convert_to_numpy=True).tolist()  # Query vector
    results = collection.query(
        query_embeddings=query_embedding,  # Vector search input
        n_results=top_k,  # Number of nearest chunks to return
        include=["documents", "metadatas", "distances"],  # Text, labels, and scores
    )
    retrieved = []  # Clean evidence list for the generator
    for doc, meta, dist in zip(
        results["documents"][0],  # Matched chunk texts
        results["metadatas"][0],  # Metadata aligned with each match
        results["distances"][0],  # Similarity distances for inspection
    ):
        retrieved.append({"text": doc, "metadata": meta, "distance": dist})  # One ranked hit
    return retrieved  # Top-k policy excerpts for this question


def build_grounded_prompt(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_block = ""  # Accumulate labeled policy excerpts
    for index, chunk in enumerate(retrieved_chunks, start=1):  # Number excerpts for clarity
        src = chunk["metadata"].get("source", "unknown")  # Source file name
        cat = chunk["metadata"].get("category", "unknown")  # Policy area label
        context_block += f"\nExcerpt {index} (source: {src}, category: {cat}):\n{chunk['text']}\n"
    return f"""You are ShopKart customer support.
Answer using ONLY the policy excerpts below.
Rules:
1. Do not invent numbers or rules not in the excerpts.
2. If information is missing, say: "I do not have enough information in the provided policy excerpts."
3. Keep the answer short and polite.

Policy excerpts:
{context_block}

Customer question:
{user_query}

Final answer:"""  # Grounded prompt with evidence and strict rules


def generate_grounded_answer(client: Groq, user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    prompt = build_grounded_prompt(user_query, retrieved_chunks)  # Build evidence-backed prompt
    response = client.chat.completions.create(
        model=GENERATION_MODEL_NAME,  # Groq-hosted Llama generator
        messages=[
            {"role": "system", "content": "You are a precise ShopKart support assistant. Follow the excerpts exactly."},
            {"role": "user", "content": prompt},  # Grounded user message with excerpts
        ],
    )
    return response.choices[0].message.content.strip()  # Final grounded answer text


def print_retrieved_chunks(user_query: str, retrieved_chunks: List[Dict[str, Any]]) -> None:
    print("\n" + "=" * 72)  # Visual divider in terminal output
    print(f"Customer question: {user_query}")  # Echo the query under inspection
    print("=" * 72)  # Closing divider line
    for rank, chunk in enumerate(retrieved_chunks, start=1):  # Rank 1 is best match
        print(f"\nRank {rank}")  # Human-friendly rank label
        print(f"  Category : {chunk['metadata'].get('category')}")  # returns/shipping/etc.
        print(f"  Source   : {chunk['metadata'].get('source')}")  # File name
        print(f"  Distance : {chunk['distance']:.4f}")  # Lower usually means closer match
        print(f"  Text     : {chunk['text']}")  # Retrieved chunk body


def answer_with_rag(client, collection, model, user_query: str, top_k: int = 3) -> str:
    retrieved = retrieve_policy_chunks(collection, model, user_query, top_k)  # Retrieve evidence
    print_retrieved_chunks(user_query, retrieved)  # Inspect retrieval before trusting answer
    return generate_grounded_answer(client, user_query, retrieved)  # Generate grounded reply
```

**How the code works:**

- **`build_knowledge_base`** = offline **load → chunk → embed → upsert**.
- **`top_k=3`** because each policy file now produces **multiple chunks**.
- **`print_retrieved_chunks`** is your quality check — read **category** and **text** before trusting the answer.

![Four policy files indexed as many Chroma chunks in shopkart_policy_kb_v2 — top_k=3 retrieval surfaces the best excerpts; wrong Rank 1 category points to ingestion or chunking, not the generator](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-07-many-chunks-chroma.png)

![answer_with_rag loop — retrieve top_k=3 chunks, print ranks for inspection, then generate a grounded Groq answer on demo queries covering returns, shipping, warranty, and refunds](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-08-answer-with-rag.png)

### Run the Full Pipeline

```python
def main():
    client = Groq()  # Generator client — GROQ_API_KEY from .env
    model = create_embedding_model()  # BGE model for retriever
    collection = setup_chroma_collection()  # Open or create Chroma collection
    build_knowledge_base(model, collection)  # Offline load, chunk, embed, upsert

    demo_queries = [  # Questions spanning returns, shipping, warranty, refunds
        "I received my phone case yesterday unopened. How many days do I have to return it?",
        "Will express shipping reach my address in a metro city by tomorrow?",
        "My wireless earphones stopped working after 10 months. Is repair covered?",
        "I returned a defective kettle on COD last week. When will the refund reach my UPI?",
    ]

    for user_query in demo_queries:  # Run each support question through full RAG loop
        print("\n\n" + "#" * 72)  # Section header per question
        print("QUESTION:", user_query)  # Show current customer line
        answer = answer_with_rag(client, collection, model, user_query)  # Retrieve then generate
        print("\nFinal grounded answer:")  # Label final output
        print(answer)  # Print grounded ShopKart reply


if __name__ == "__main__":
    main()  # Run ingestion then demo queries when script executed directly
```

```bash
cd shopkart_rag_pipeline
python rag_pipeline.py
```

**What to verify in the terminal (your implementation checklist):**

| Step | Expected |
|---|---|
| Load | `Loaded 1 document(s)` × 4 files |
| Chunk | `Total chunks created` > 4 |
| Index | `Indexed N chunks into shopkart_policy_kb_v2` |
| Retrieve | Rank 1 **category** matches question area (returns / shipping / warranty / refunds) |
| Answer | Numbers match policy (7 days, 3–5 days, 12 months, 5–7 days, metro express, COD → UPI) |

![Terminal verification checklist — confirm four files loaded, chunk count above four, index into shopkart_policy_kb_v2, Rank 1 category matches the question, and grounded answers cite correct policy numbers](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session21/session21-09-verification-checklist.png)

If Rank 1 **category** is wrong, the bug is usually **ingestion or chunking** — not the generator. Policy refresh workflows and deep retrieval tuning come in a **later** session.

---

## Key Takeaways

- **Ingestion is new today; the RAG loop is not** — loaders and chunking feed the same BGE + Chroma + Groq pipeline.
- **Chunk size and overlap** control which rules retrieval surfaces; inspect retrieved text every run.
- **Metadata** (`category`, `source`) helps you trace which policy file supplied each excerpt.
- **Next:** evaluate and improve this assistant — diagnose retrieval vs generation failures and apply targeted fixes.

---

## Important Commands, Libraries, and Terminologies used

| Term / Command | Meaning in one line |
|---|---|
| **Document loader** | Reads PDF/TXT files into cleaned text for the pipeline |
| **`pypdf` / `PdfReader`** | PDF text extraction page by page |
| **`clean_text`** | Collapse newlines and extra spaces |
| **Chunking / overlap** | Split text into ~100-word units with 20-word tail repeat |
| **`build_knowledge_base`** | Offline load → chunk → embed → upsert |
| **`shopkart_policy_kb_v2`** | Chroma collection for chunked policies |
| **`top_k=3`** | Retrieve three excerpts per question |
| **`answer_with_rag`** | Retrieve → print ranks → generate grounded answer |
| **BGE / Groq / `.env`** | Same stack as the minimal RAG lab |
