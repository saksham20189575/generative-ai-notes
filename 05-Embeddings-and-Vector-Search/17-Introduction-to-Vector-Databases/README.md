# Introduction to Vector Databases

## Context of This Session

In the previous session, you learned how **embeddings** turn text into vectors so that similar meaning sits close together in **vector space**. You traced how text becomes embeddings, why the **same embedding model** must be used for documents and queries, and walked through the **semantic search workflow**: store content → embed documents → embed the query → compare vectors → return the closest matches.

That workflow answers *what* to do with meaning. Today’s question is *where* and *how fast* you do it when the data grows from ten classroom chunks to thousands of company documents or millions of stored chunks.

**In this session, you will:**

- Briefly recall how **embeddings** power similarity-based retrieval (without re-teaching full embedding theory)
- See why **traditional relational databases** struggle with efficient vector similarity search at scale
- Define **vector databases** and their role in storing, indexing, and retrieving embeddings
- Build intuition for **similarity-based retrieval**, **similarity measurement**, and the **similarity search process** end to end
- Understand why **brute-force** comparison fails at scale and how **vector indexing** and **ANN** search fix that
- Differentiate **exact match** vs **similarity search** in one short recap
- Prepare for the **next** session, where you will implement embed → store → query → top-k in code with **Chroma**

This session is **conceptual only** — no Chroma setup or live coding lab today. You will still see small code sketches and solo notebook activities so the ideas stay concrete.

---

## Bridge — Embeddings and Semantic Search

Before vector databases, confirm the foundation you already have. This section is a **short** recap, not a repeat of the full embedding lesson.

### What You Already Know

- **Embeddings** are fixed-size lists of numbers that represent the **meaning** of text (word, sentence, or document chunk).
- **Semantic search** does not look for the exact same words; it looks for the **nearest vectors** in embedding space.
- The **same embedding model** must embed both your stored documents and every new user query — otherwise “closeness” scores are meaningless.

### The Semantic Search Workflow (Story Level)

Picture a support bot for an online course platform:

1. **Store** — Split policy PDFs and FAQs into chunks; keep the original text and metadata (source file, page).
2. **Embed documents** — Run each chunk through the embedding model; save the vector with the text.
3. **Embed the query** — When a student asks “I cannot log in,” embed that question with the **same** model.
4. **Compare** — Find which stored vectors are **closest** to the query vector.
5. **Return** — Send the top matches to the user or into an LLM for a grounded answer (RAG).

![Semantic search workflow — store chunks, embed documents and the query with the same model, compare vectors, return the nearest matches for RAG](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-01-semantic-search-workflow.png)

You already drew this pipeline. Today we ask: *what happens when step 4 must search across 500,000 chunks in under a second?*

### Readiness Check — Quick Self-Test

Answer in your notebook (no formulas needed):

- Why must document and query vectors come from the **same model**?
- In one sentence, what does “**nearest** vector” mean in plain language?
- Name one case where **SQL** is still the right tool (exact ID or status filter).

If those three feel clear, you are ready for vector database concepts.

### Simple Activity — Trace One Query

On three sticky notes (or slips of paper), write Chunk A, B, and C with one different topic on each. Read this user question aloud: “refund for cancelled workshop.” Pick the chunk that **sounds closest in meaning** without matching exact words. In your notebook, write one sentence: that human “nearest meaning” step is what vector search automates with numbers.

---

## Recall the Role of Embeddings in AI Systems

Embeddings are not a separate product feature — they are the **bridge** between human language and machine-scale retrieval.

- **Official Definition:** An **embedding** is a dense vector representation of data (often text) produced by a trained model, such that semantically similar inputs map to nearby points in a high-dimensional space.
- **In Simple Words:** Embeddings are a **coordinate system for meaning** — similar sentences get similar coordinates.
- **Real-Life Example:** On Google Maps, “MG Road, Bangalore” and “Mahatma Gandhi Road, Bengaluru” may be the same place even if the spelling differs. Embeddings do something similar for **wording**, not street addresses.

### How Embeddings Enable Similarity-Based Retrieval

Traditional search asks: “Does this row **contain** this word?” Embedding-based retrieval asks: “Which stored items are **closest in meaning** to this question?”

- The model turns text → vector.
- The system compares the query vector to many stored vectors.
- The **closest** matches are returned as candidates for display or for a downstream application to use.

![Embeddings as a meaning map — semantically similar chunks sit close together; retrieval finds the nearest neighbours to the query vector](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-04-embeddings-meaning-map.png)

- **Common doubt:** “Does the embedding *understand* like a human?” No — it learned statistical patterns from huge training data. In practice, that is enough for strong retrieval if chunks and models are chosen well.
- **Why this matters for vector DBs:** A vector database’s job is to store those coordinates and find **nearest neighbours** quickly — not to replace the embedding model.

### Connecting Sentence

You understand **what** embeddings are. The next sections explain **why ordinary SQL tables are the wrong primary home** for millions of vectors and **what specialised stores add instead**.

---

## Limitations of Traditional Databases for Vector Data

Relational databases (PostgreSQL, MySQL, Supabase tables) are excellent at **exact, structured** facts. They are not built, by default, for “find the five sentences **most like** this paragraph in meaning” across huge text collections.

### Exact-Key Lookup vs Nearest-Meaning Search

| Idea | Relational / SQL style | Vector / semantic style |
|---|---|---|
| **Question** | “Give me `user_id = 7`” | “What passages are **like** this question?” |
| **Match rule** | Equality on keys and filters | **Closeness** between vectors |
| **Index use** | B-tree on IDs, dates, statuses | Special structures for **similarity** |
| **Typical strength** | Orders, users, payments, statuses | Docs, chats, policies, memories |

- **Official Definition:** **Exact-key lookup** retrieves rows where a column equals a specified value (or satisfies explicit predicates); **nearest-neighbour search** retrieves items whose vectors are closest to a query vector under a similarity measure.
- **In Simple Words:** SQL answers “**which row is this ID?**” Vector search answers “**which chunks feel most related?**”
- **Real-Life Example:** Finding your train ticket by **PNR number** is exact lookup. Finding a **similar previous complaint** from lakhs of old tickets is nearest-meaning search.

![SQL exact-key lookup versus vector similarity search — equality on IDs and filters vs nearest meaning in embedding space](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-02-sql-vs-vector-search.png)

### Why SQL Alone Struggles at Scale for Vectors

- **High dimensionality** — Each embedding might have 384, 768, or 1536 numbers. Storing them in a normal row is fine; **comparing every row to every query** is not.
- **No native “nearest” index** — Classic indexes speed up `WHERE city = 'Mumbai'`, not “smallest angle to this 768-number list.”
- **Brute force in application code** — Pulling all vectors into Python and looping works for demos, not for production traffic.

Extensions like **pgvector** add vector types and similarity operators **inside** PostgreSQL — useful when you already live in SQL land. Dedicated **vector databases** (Chroma, Pinecone, etc.) optimise the full embed-store-search loop. You will meet **Chroma** hands-on in the **next** session; today we stay conceptual.

- **Common mistake:** “We put embeddings in a JSON column, so we are done.” Storage without a **similarity index** still means slow scans as data grows.
- **They work together:** SQL for **who** the customer is and **what** they bought; vector search for **what they are asking** in free text.

### Simple Activity — Two Questions, Two Tools

For each business question, write **SQL**, **vector similarity**, or **both**:

1. Total revenue from orders in March 2025.  
2. Find internal wiki pages related to “reset two-factor authentication” when articles say “MFA recovery.”  
3. List all orders with `status = 'shipped'`.

(Answers: 1 → SQL; 2 → vector similarity; 3 → SQL.)

---

## Introduce Vector Databases

Once embeddings become your retrieval currency, you need a system designed to **hold** them and **find neighbours** fast.

- **Official Definition:** A **vector database** is a storage and retrieval system optimised for embedding vectors, supporting similarity search, metadata filtering, and scalable indexing for nearest-neighbour queries.
- **In Simple Words:** It is a **library catalogue sorted by meaning**, not by alphabetical title — and the librarian can find “books like this one” in milliseconds even with millions of entries.
- **Real-Life Example:** Imagine every FAQ answer in your coaching centre is pinned on a giant map by topic. A student asks a new question; you walk to the **nearest pins**, not the pins whose titles share the same spelling.

### What Vector Databases Do (Three Jobs)

1. **Store** — Persist vectors with their original text and metadata (source, date, user id, tags).
2. **Index** — Organise vectors so search does not scan every point every time.
3. **Retrieve** — Given a query vector, return **top-k** nearest matches (and optionally filter by metadata).

![A vector database’s three jobs — store embeddings with text and metadata, index for fast search, retrieve top-k nearest neighbours](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-03-vector-database-three-jobs.png)

### Example Tools (High Level Only — No Setup Today)

| Tool | One-line role |
|---|---|
| **Chroma** | Lightweight, developer-friendly; great for learning and prototypes (your **next** session lab) |
| **Pinecone** | Managed cloud service; scales without you running servers |
| **pgvector** | Extension inside PostgreSQL; vectors live next to your existing SQL tables |
| **Weaviate, Qdrant, Milvus** | Other production-grade options teams use at scale |

You do not need to memorise vendors today. You need the **pattern**: embed → store in vector DB → query by vector → use results in your application.

### Metadata Alongside Vectors

Real systems rarely store “only numbers.” Each vector usually carries:

- **Document text** or chunk text  
- **Source** (filename, URL, ticket id)  
- **Timestamps**, **user id**, **product category** for filtered search  

Example: “Search support articles **similar** to this question, but **only** from the Billing category.” Vector DBs combine **similarity** + **metadata filters**.

### Connecting Sentence

A vector database is the **specialised warehouse** for embedding coordinates. Next, we make **similarity-based retrieval** intuitive before touching indexing maths.

---

## Understand Similarity-Based Retrieval

- **Official Definition:** **Similarity-based retrieval** returns items whose embedding vectors are closest to a query embedding under a chosen similarity or distance measure, rather than matching exact strings or primary keys.
- **In Simple Words:** You throw a dart at the “meaning map”; the system returns whatever landmarks landed **nearest** to where the dart stuck.
- **Real-Life Example:** Spotify’s “songs like this” flow — not because the title contains the same words, but because audio/features (and sometimes lyrics embeddings) sit nearby in feature space.

### How Results Differ from Keyword Search

- **Keyword:** “password” must appear (or stemmed variants in advanced engines).  
- **Similarity:** “I forgot my login” can match “account recovery steps” with **no shared words**.  

- **Trade-off:** Similarity can occasionally pull **loosely related** chunks if your data is noisy or chunks are too large. Mitigations: better chunking, metadata filters, re-ranking, and asking the LLM to cite only retrieved text.

### Top-k Retrieval

- **Official Definition:** **Top-k retrieval** returns the **k** vectors with the highest similarity (or lowest distance) to the query vector.
- **In Simple Words:** “Give me the **five best** matches, not the whole database ranked.”
- **Real-Life Example:** Google shows one page of ten results — you rarely need rank 10,000; you need the **top few** good enough for the user or the LLM.

- **Common doubt:** “What if the true answer is rank 50?” Then improve embeddings, chunking, or filters — or increase k slightly and let a re-ranker trim. Production is tuning, not magic.

---

## Develop Intuition for Similarity Search in Production

Production systems repeat the same story millions of times per day: **embed query → search collection → return nearest items → downstream app uses them.**

### Analogy — The Coaching Centre Notice Board

Imagine thousands of sticky notes on a wall — each note is one FAQ chunk. Notes about **fees** cluster on the left; **placements** on the right; **hostel** at the back.

A student walks in and asks aloud: “Can I pay fees in instalments?” You do not read every note word by word. You walk to the **fee cluster** and read the **nearest** notes. Vector search automates that “walk to the right neighbourhood” step using numbers.

### Another Analogy — Amazon “Customers Also Bought”

Product descriptions and reviews are embedded. Your current product is a query vector. Items with **nearby** vectors become recommendations — even if category names differ slightly.

### What Happens After Retrieval?

Similarity search **finds**; it does not always **answer** by itself. A common next step is **direct display** — show the FAQ text to the user — or hand the top chunks to another part of your system (for example, an LLM prompt) for a fuller reply.

- **Failure mode:** Returning chunks that are **similar in topic but wrong in policy version** — fix with metadata (e.g. `policy_year = 2025`) and good chunk boundaries.

### Simple Activity — Human Top-k

- Write 20 short sentences on mixed topics in your notebook.
- Choose one query sentence and read it aloud.
- In 60 seconds, pick the **top 3** sentences closest in meaning.
- Write your top 3 and one sentence on why your third pick might be debatable — the same ambiguity appears when real vector search has close tie scores.

---

## Understand Similarity Measurement (Conceptual)

You already met the idea that **closer vectors ≈ more similar meaning**. This section is a **short reinforcement** — no heavy formulas.

- **Official Definition:** **Similarity measurement** quantifies how alike two vectors are, commonly via **distance** (smaller = closer) or **cosine similarity** (angle between vectors; focuses on direction of meaning).
- **In Simple Words:** Distance asks “how far apart are the points?” Cosine asks “are they pointing the **same direction** on the map?”
- **Real-Life Example:** Two friends walk **the same direction** from college gate (cosine cares about direction). One friend stops sooner (distance also cares how far they walked).

### Distance vs Angle — Intuition Only

- **Euclidean distance** — Straight-line gap between two points in space.  
- **Cosine similarity** — Very common for text embeddings; two texts can be similar even if one vector is “longer” in magnitude.  

Systems pick one measure and use it **consistently** for indexing and querying. You do not calculate by hand — the database or library does.

- **Common mistake:** Mixing similarity definitions between indexing and query time — always follow your tool’s documented default.
- **Do not confuse:** High “cosine similarity” = more alike; some APIs return **distance** where **lower** = better. Read the docs for your stack in the **next** session.

### Full Code — Toy Vectors (Direction Intuition)

```python
# Three tiny 3-number vectors standing in for real embeddings (normally hundreds of dims)
vec_refund_policy = [0.9, 0.1, 0.0]   # Mostly about money/refunds
vec_cancel_course = [0.85, 0.15, 0.0] # Similar direction → similar topic
vec_hostel_rules    = [0.1, 0.1, 0.9] # Points a different way → different topic

def simple_dot(a, b):  # Define a tiny helper to score how two vectors align
    # Toy score: larger when numbers line up (NOT production cosine — demo only)
    return sum(x * y for x, y in zip(a, b))  # Multiply matching positions and add them up

score_near = simple_dot(vec_refund_policy, vec_cancel_course)  # Compare two similar topics
score_far  = simple_dot(vec_refund_policy, vec_hostel_rules)   # Compare refund vs hostel topic

print("Refund vs cancel (expect higher):", score_near)  # Show the similar-topic score
print("Refund vs hostel (expect lower):", score_far)    # Show the different-topic score
```

**How the code works:**

- Real embeddings have hundreds of dimensions; we use 3 so you can see the pattern.
- `vec_refund_policy` and `vec_cancel_course` align on the first dimensions → higher dot score in this toy.
- Production tools use optimised **cosine** or **inner product** on GPU/CPU — you call their API instead of hand loops.

---

## Understand the Need for Scalable Search

Brute force means: for **every** query, compare the query vector to **every** stored vector, then sort. That is correct but slow.

### Why Brute Force Breaks

| Collection size | Rough feel (conceptual) |
|---|---|
| 1,000 vectors | Fine for class demos |
| 100,000 vectors | Noticeable delay if done naïvely every request |
| 10,000,000 vectors | Unacceptable for real-time apps without indexing |

- **Official Definition:** **Brute-force nearest neighbour search** computes the similarity between a query vector and all vectors in a collection before selecting the top results.
- **In Simple Words:** Reading **every book** in the library before picking five — works when the library is a cupboard; fails when it is a national archive.
- **Real-Life Example:** Finding your friend in a stadium by checking **every seat** one by one vs reading a **section map** first.

![Brute-force compares the query to every vector; indexing and ANN skip large regions so search stays fast at millions of vectors](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-05-brute-force-vs-indexing.png)

### What Systems Need

- **Low latency** — Users expect answers in sub-second to a few seconds.  
- **High throughput** — Many concurrent queries during peak traffic.  
- **Growing data** — New documents and memories arrive daily; indexes must update incrementally.  

That pressure drives **vector indexing** and **approximate** search — trading a little perfect accuracy for large speed gains.

### Full Code — Brute Force vs “Stop Early” Story (Pedagogical)

```python
# Pretend we have 5 stored vectors and 1 query vector (each just 2 numbers for clarity)
stored = {  # Dictionary of chunk names → toy embedding vectors
    "chunk_A": [1.0, 0.0],   # Stored vector A
    "chunk_B": [0.9, 0.1],   # Stored vector B (close to query direction)
    "chunk_C": [0.0, 1.0],   # Stored vector C (different direction)
    "chunk_D": [0.2, 0.8],   # Stored vector D
    "chunk_E": [0.95, 0.05], # Stored vector E (very close to query direction)
}
query = [0.92, 0.08]  # The user question as a toy query vector

def l2_distance(a, b):  # Define straight-line distance between two vectors
    # Straight-line distance: smaller means closer in this toy demo
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5  # Square differences, sum, square root

# BRUTE FORCE: compare query to EVERY stored vector
scores = []  # Empty list to collect (chunk name, distance) pairs
for name, vec in stored.items():  # Loop over every stored chunk
    dist = l2_distance(query, vec)  # One comparison per chunk
    scores.append((name, dist))  # Save this chunk’s distance score

scores.sort(key=lambda item: item[1])  # Sort all results by distance (smallest first)
top_k = scores[:2]  # Take best 2 nearest chunks
print("Brute-force top-2:", top_k)  # Print the two closest matches

# In a real vector DB, an INDEX avoids touching every vector — coming next section
```

**How the code works:**

- The loop visits **all** entries — that is O(n) comparisons per query.
- `scores.sort` picks the smallest distances — correct but does not scale.
- Vector databases replace the naked loop with **index structures** that skip huge regions of the space.

### Simple Activity — Stadium Sections

In your notebook, draw a stadium with 8 sections (label them 1–8). Privately pick one section as the hidden “target.” Write three yes/no questions you could ask to narrow down the section — using **sections** only, not individual seats. Below your questions, write one sentence: good questions **eliminate** large areas quickly — the same idea as ANN indexes skipping unlikely regions.

---

## Introduce Vector Indexing

- **Official Definition:** **Vector indexing** builds auxiliary data structures over embeddings so nearest-neighbour queries can skip large portions of the collection without examining every vector.
- **In Simple Words:** Instead of checking every sticky note on the wall, you build a **map of neighbourhoods** so you run to the right corner first.
- **Real-Life Example:** A post office sorts PIN codes by region — you do not open every bag in India to find one letter for 560001.

### What an Index Does

- **Organises** vectors in space (clusters, graphs, hash buckets — details vary by algorithm).  
- **Guides** the search toward promising regions first.  
- **Updates** as new vectors are inserted (rebuild or incremental strategies depend on the product).  

You will not implement indexes by hand. You **choose** a vector database and often an **index type** from its docs (e.g. HNSW, IVF — names only today).

- **Trade-off:** Indexes consume **extra memory** and need **tuning** (parameters affect speed vs accuracy).
- **Common doubt:** “Do I index in SQL tables?” Not with normal B-tree indexes on text IDs — you need vector-specific index support (inside pgvector or a dedicated vector DB).

### Connecting Sentence

Indexing makes search **feasible**. Because perfect exhaustive search is still expensive at huge scale, production often uses **approximate** nearest neighbours — explained next.

---

## Understand Approximate Nearest Neighbor (ANN) Search

- **Official Definition:** **Approximate Nearest Neighbor (ANN) search** returns vectors that are **very likely** among the true nearest neighbours, without guaranteeing the mathematically exact top-k, in exchange for much faster query time on large datasets.
- **In Simple Words:** You might miss the **absolute best** sticky note, but you get a **very good** one in 1% of the time — and users cannot tell the difference most days.
- **Real-Life Example:** Ola shows **nearby** drivers, not every driver in India ranked by exact road distance to the millimetre — “good enough, fast enough.”

![Approximate nearest neighbour (ANN) search uses an index to reach very good top-k matches quickly instead of scanning the entire collection](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-06-ann-search.png)

### Speed vs Accuracy

| Approach | Accuracy | Speed at huge n |
|---|---|---|
| **Exact** brute force | Perfect ranking | Slow |
| **ANN** with index | Usually excellent top-k | Fast |

- Teams tune ANN when latency budgets are tight (chatbots, high-traffic search bars, high-QPS APIs).
- For tiny collections, exact search is fine — your **next** session lab may be small enough that brute force and indexed search **feel** similar; the concepts still matter for jobs and scale.

- **Common mistake:** Assuming ANN is “wrong search.” In practice, retrieval quality depends more on **chunking, model choice, and metadata** than on missing rank-47 vs rank-48.
- **Evaluation habit:** Measure **answer quality** on a test set of real questions, not only theoretical perfect neighbour rank.

### Simple Activity — Good Enough Match

Using a list of 15 cities, find the city you think is **closest** to Pune by road distance — without calculators. You will likely pick **nearby** cities quickly, even if you are not sure of the mathematically exact #1. In your notebook, write when “good enough fast” beats “perfect slow” in product design.

---

## Understand the Similarity Search Process (End to End)

This is the full **conceptual pipeline** you will implement in the **next** session. Treat it as a story with five acts.

### Diagram in Words

```
[Documents] → chunk → embed → store in Vector DB (with index)
                                      ↑
[User question] → embed (same model) ─┘
                                      ↓
                         ANN / similarity search → top-k chunks
                                      ↓
                         Application uses returned text + metadata
```

![End-to-end similarity search — chunk and embed documents, store in a vector DB, embed each query with the same model, ANN search returns top-k matches for your application](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session17/session17-07-end-to-end-pipeline.png)

### Step-by-Step (Conceptual)

1. **Ingest** — Collect sources (PDFs, tickets, wiki pages).  
2. **Chunk** — Split long files into retrieval-sized pieces (**chunking** = breaking one big document into smaller passages so search returns the right paragraph, not the whole PDF).  
3. **Embed** — Each chunk → vector via embedding model.  
4. **Upsert into vector DB** — Save vector + text + metadata; build or refresh index.  
5. **Query time** — Embed user question → vector DB returns top-k neighbours.  
6. **Use results** — Display to the user or pass chunks to the next step in your pipeline.  

- **Official Definition:** **Upsert** means insert a new record or update it if the id already exists — common when documents change.
- **In Simple Words:** “Save or refresh this chunk” without duplicating the same id twice.

### Full Code — Pseudocode Pipeline (No Chroma Yet)

```python
# ============ OFFLINE: BUILD THE COLLECTION (runs when docs change) ============
chunks = [  # Sample FAQ chunks before they go into the vector database
    {"id": "faq_1", "text": "How to reset your password", "topic": "account"},  # First chunk
    {"id": "faq_2", "text": "Track your shipment status", "topic": "shipping"},  # Second chunk
]

for chunk in chunks:  # Process each chunk once when documents are added or updated
    vector = embedding_model.encode(chunk["text"])  # Same model always — turn text into numbers
    vector_db.upsert(  # Save or update this chunk in the collection
        id=chunk["id"],           # Unique key for this chunk
        embedding=vector,         # Numbers stored for similarity search
        document=chunk["text"],   # Original text returned to users/LLM
        metadata={"topic": chunk["topic"]},  # Optional filters later (e.g. topic = account)
    )

vector_db.build_index()  # Many libraries index automatically or on first query

# ============ ONLINE: EACH USER QUESTION ============
user_question = "I forgot my login password"  # What the user typed in the app
query_vector = embedding_model.encode(user_question)  # MUST be same model as above

results = vector_db.query(  # Ask the vector DB for nearest neighbours
    embedding=query_vector,  # Search by vector, not raw string
    top_k=2,                 # Return two nearest chunks
    filter={"topic": "account"},  # Optional: only search account FAQs
)

for hit in results:  # Loop through each match the database returned
    print(hit.id, hit.document, hit.score)  # score = similarity or distance per tool
```

**How the code works:**

- **Offline loop** prepares the knowledge base once (or on a schedule).
- `embedding_model.encode` is the same function for chunks and queries — non-negotiable.
- `vector_db.query` is where indexing/ANN happens inside the product — you do not write the loop over millions of rows.
- `filter` shows how SQL-like constraints combine with semantic search.
- In the **next** session, `vector_db` becomes a real **Chroma** client with runnable scripts.

### Simple Activity — Draw Your Pipeline

On one A4 sheet, draw the six steps above for a scenario you care about (college notices, internship handbook, or favourite app). Label where **SQL** still fits (user profile) vs where the **vector DB** fits (meaning search).

---

## Differentiate Exact Match vs Similarity Search (Brief Recap)

You compared these ideas in depth earlier. Here is a **brief** consolidation — not a full re-teach.

| When to use | Exact match (SQL / keyword) | Similarity (vector DB) |
|---|---|---|
| **Data type** | Structured tables, IDs, enums | Unstructured or semi-structured text |
| **Question style** | “Status = shipped”, “email = x” | “Something **like** this meaning” |
| **Risk** | Wrong row if key typo | Loosely related chunk if data messy |

- **Win together:** SQL fetches **order history** by exact keys; vector search fetches **policy paragraphs** about refunds by meaning; your application combines both.
- **Do not replace SQL** with vectors for money totals, inventory counts, or compliance reports that require exact aggregates.

### Simple Activity — Traffic Light

- Write ten user questions on topics you care about (course portal, shopping app, travel booking, etc.).
- Classify each as **green** (SQL/exact), **amber** (both), or **red** (semantic/vector).
- For any label you are unsure about, write one sentence explaining your reasoning.

---

## Bridge to the Next Session — From Concepts to Chroma

Today you built the **mental model**:

- Embeddings turn language into points on a meaning map.  
- Relational databases excel at **exact** facts; vector databases excel at **nearest meaning** at scale.  
- **Indexing** and **ANN** make large-scale search practical.  
- The end-to-end story is: **chunk → embed → store → query → top-k → use in your application.**

In the **next** session, you will **implement** that pipeline in code with **Chroma**: create a collection, embed sample documents, run queries, set **top-k**, and run a minimal end-to-end script. Conceptual clarity today makes the lab feel like assembly, not magic.

**Come prepared with:**

- Python environment ready (as used in earlier course labs).  
- Confidence on **same embedding model** for ingest and query.  
- This session’s diagram drawn once in your notebook — you will map each box to a line of code.

---

## Key Takeaways

- **Embeddings** enable **similarity-based retrieval** — find stored content whose vectors are nearest to the query vector, using the **same embedding model** for both sides.
- **Traditional SQL** is ideal for **exact keys and structured filters**; it is not designed for fast **nearest-meaning** search over millions of high-dimensional vectors without specialised extensions or a dedicated vector store.
- A **vector database** **stores**, **indexes**, and **retrieves** embeddings (often with metadata filters), using **vector indexing** and **ANN** to avoid brute-force scans as data grows.
- The **similarity search process** is: ingest and chunk → embed documents → upsert into the vector DB → embed each query → return **top-k** neighbours → use the returned text and metadata downstream.
- **Exact match** and **semantic search** complement each other — use SQL (or keyword search) for precise facts and vector search for nearest-meaning retrieval.

In the **next** session, you will turn this diagram into runnable **Chroma** code — embed, store, query, and inspect top-k results — completing the path from meaning vectors to a working retrieval pipeline you can extend in real projects.

---

## Important Commands, Libraries, and Terminologies

| Term / Tool | Type | Meaning |
|---|---|---|
| Embedding | Concept | Vector representation of text (or other data) capturing semantic meaning |
| Semantic search | Concept | Retrieval by nearest embedding vectors, not exact string match |
| Vector database | System | Store optimised for embeddings + fast similarity search |
| Similarity-based retrieval | Concept | Return items closest to query vector in embedding space |
| Top-k | Concept | Return the k best matches by similarity or distance |
| Brute-force search | Concept | Compare query to every vector; correct but slow at scale |
| Vector indexing | Concept | Data structures that speed up nearest-neighbour search |
| ANN (Approximate Nearest Neighbor) | Concept | Fast, near-optimal neighbour search for large collections |
| Cosine similarity | Concept | Similarity based on angle between vectors (common for text) |
| Euclidean distance | Concept | Straight-line distance between two points in vector space |
| Metadata filter | Concept | Restrict vector search by tags (topic, year, user id, etc.) |
| Upsert | Concept | Insert or update a record by id in the collection |
| Chunking | Concept | Split long documents before embedding for better retrieval |
| Chroma | Tool (next session) | Lightweight vector database for learning and prototypes |
| Pinecone | Tool | Managed cloud vector database service |
| pgvector | Extension | Vector similarity inside PostgreSQL |
| HNSW / IVF | Index types | Common ANN index families (names only; configured in tools) |
| Exact-key lookup | Concept | SQL-style match on ids, keys, and explicit predicates |
| `embedding_model.encode()` | API pattern | Converts text to vector (same model for docs and queries) |
| `vector_db.query()` | API pattern | Accepts query vector + top_k (+ optional filters) |
