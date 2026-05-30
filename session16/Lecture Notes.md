# Embeddings and Semantic Representation

## Context of This Session

In the previous session, you moved beyond single-table SQL. You learned how to sort and paginate results with `ORDER BY`, `LIMIT`, and `OFFSET`, why real data is split across multiple related tables, and how **primary keys** and **foreign keys** keep those tables linked without repeating the same information everywhere. You also designed related tables in Supabase and started connecting data from two tables at once.

This session first completes that relational-database journey: you will write a full **INNER JOIN** on a `users` and `orders` example, then practice **insert, update, and delete** across related tables while the database enforces **referential integrity**. After that, the course pivots to one of the most important ideas in modern AI — how machines represent **meaning**, not just words.

**In this session, you will:**

- Write **INNER JOIN** queries on two related tables (`users` and `orders`) and understand what a JOIN does before you type it
- Perform **CRUD** on related tables and see how **cascade** behaviour protects (or cleans up) linked data
- Recap why **meaning-based search** matters for AI, RAG, and agents
- Define **vectors** and **embeddings** at word, sentence, and document level
- Trace how **text becomes embeddings**, including the role of **tokenization**
- Build intuition for **semantic similarity** and **vector space**
- Compare **keyword search** vs **semantic search** and walk through the **semantic search workflow**
- See where embeddings fit in **agentic systems** and what comes in the **next** session on vector databases

---

## Setting Up Related Tables — Users and Orders

Before we JOIN, we need two tables that mirror a pattern you already understand: one parent, many children. Here we use **users** (one person) and **orders** (many purchases per person).

- **Official Definition:** A **one-to-many relationship** links one row in a parent table to many rows in a child table; the child stores a **foreign key** pointing to the parent's **primary key**.
- **In Simple Words:** One user can place many orders, but each order belongs to exactly one user.
- **Real-Life Example:** On Swiggy, one account can have dozens of past orders; each order receipt still shows one customer ID tied to that account.

![One-to-many relationship — one user row in the parent table links to many order rows in the child table via a foreign key on user_id](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-01-users-orders-one-to-many.png)

**Full Code — Create the `users` Table:**

```sql
-- Create the parent table: one row per registered user
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,        -- Unique auto-increment ID for each user
    full_name VARCHAR(100) NOT NULL,   -- User's display name; cannot be empty
    email VARCHAR(150) UNIQUE NOT NULL, -- Each email appears only once in the system
    city VARCHAR(50),                  -- Optional city for filtering reports later
    joined_at TIMESTAMP DEFAULT NOW()  -- When the user signed up; filled automatically
);
```

**How the code works:**

- `SERIAL PRIMARY KEY` assigns `user_id` values 1, 2, 3… automatically.
- `UNIQUE` on `email` stops two accounts from sharing the same email — a common rule in real apps.
- This table is the **parent**; every order will reference a valid `user_id` from here.

**Full Code — Create the `orders` Table with Foreign Key:**

```sql
-- Create the child table: many orders can point to one user
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,       -- Unique ID for each order
    user_id INT NOT NULL,              -- Must match a real user_id in users
    item_name VARCHAR(200) NOT NULL,   -- What was purchased
    amount DECIMAL(10, 2) NOT NULL,    -- Price with two decimal places (e.g. 499.00)
    status VARCHAR(50) DEFAULT 'pending', -- Order state: pending, shipped, delivered
    ordered_at TIMESTAMP DEFAULT NOW(), -- When the order was placed

    CONSTRAINT fk_user                 -- Named rule so error messages are clear
        FOREIGN KEY (user_id)         -- This column in orders...
        REFERENCES users (user_id)    -- ...must exist in users.user_id
        ON DELETE CASCADE             -- Delete user's orders if the user is removed
);
```

**How the code works:**

- `user_id INT NOT NULL` — Every order must belong to someone; NULL is not allowed.
- `FOREIGN KEY ... REFERENCES users(user_id)` — The database rejects any `user_id` that does not exist in `users`.
- `ON DELETE CASCADE` — If a user row is deleted, all their orders disappear too, so you never have orders pointing at a deleted user.

**Full Code — Insert Sample Data (Parent First, Then Child):**

```sql
-- Step 1: Insert users first (parent rows must exist before children reference them)
INSERT INTO users (full_name, email, city)
VALUES
    ('Ananya Sharma', 'ananya@example.com', 'Bangalore'),
    ('Rohan Mehta', 'rohan@example.com', 'Mumbai'),
    ('Priya Nair', 'priya@example.com', 'Chennai');

-- Step 2: Insert orders that reference existing user_id values (1, 2, 3)
INSERT INTO orders (user_id, item_name, amount)
VALUES
    (1, 'Agentic AI Course Bundle', 2999.00),
    (1, 'Supabase Pro Plan', 499.00),
    (2, 'LangChain Workshop', 1499.00),
    (3, 'RAG Starter Kit (PDF)', 299.00);
```

**How the code works:**

- Insert order matters: **users first**, then **orders**, because the foreign key checks the parent table.
- Ananya (`user_id = 1`) has two orders — that is the "many" side of one-to-many in action.
- Trying `user_id = 99` before user 99 exists would fail with a foreign-key error — that is **referential integrity** protecting your data.

---

## Querying Relational Data with INNER JOIN

You now have related data in two tables. The business question is natural: **"Which user placed which order?"** Running two separate `SELECT` queries and matching IDs by hand is slow and error-prone. **JOIN** solves this in one step.

- **Official Definition:** A **JOIN** is a SQL operation that combines rows from two tables when values in specified columns match — usually a foreign key and its parent primary key.
- **In Simple Words:** JOIN is like stitching two spreadsheets on a shared ID column so each order row carries the user's name and city in the same result.
- **Real-Life Example:** A college office merges a "students" sheet and a "exam marks" sheet on roll number so every mark row shows the student's name without retyping it.

### What INNER JOIN Does Conceptually

Before writing SQL, picture two lists:

- **List A (orders):** order_id, user_id, item_name, amount  
- **List B (users):** user_id, full_name, city  

**INNER JOIN** walks through each order, finds the user with the **same** `user_id`, and outputs **one combined row** only when a match exists on **both** sides.

- If a user has **no** orders, they do not appear in an order-driven INNER JOIN (you would need a different join type for that — not covered here; we stay on **two-table INNER JOIN only**).
- If an order pointed to a missing user, the foreign key would already have blocked that insert.

![INNER JOIN stitches orders and users on matching user_id — each combined row shows who placed which order in one result set](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-02-inner-join-users-orders.png)

**Full Code — See Every Order with the User Who Placed It:**

```sql
-- Combine orders with user details in a single result set
SELECT
    u.full_name,           -- User name from the users table
    u.city,                -- User city from the users table
    o.item_name,           -- Product name from the orders table
    o.amount,              -- Order amount from the orders table
    o.status,              -- Order status from the orders table
    o.ordered_at           -- When the order was placed
FROM orders o              -- Start from orders (alias 'o' = short name for orders)
INNER JOIN users u         -- Bring in users (alias 'u') only where IDs match
    ON o.user_id = u.user_id;  -- Match condition: same user_id in both tables
```

**How the code works:**

- `FROM orders o` — Base table is `orders`; alias `o` keeps the query shorter.
- `INNER JOIN users u ON o.user_id = u.user_id` — For each order row, find the user row with equal `user_id`.
- Prefix columns with `u.` or `o.` when names could clash (both tables could have a `status`-like column in other designs).
- Result: one row per order, with the buyer's name and city filled in — no manual ID matching.

**Full Code — Filter JOINed Results with WHERE and ORDER BY:**

```sql
-- Show only orders from users in Mumbai, cheapest first
SELECT
    u.full_name,
    o.item_name,
    o.amount
FROM orders o
INNER JOIN users u
    ON o.user_id = u.user_id
WHERE u.city = 'Mumbai'      -- Filter after the join: city lives on users
ORDER BY o.amount ASC;       -- Sort combined rows by amount, low to high
```

**How the code works:**

- `WHERE` runs on the **already joined** result — you can filter on columns from either table.
- This pattern is how an AI dashboard might answer: "Show all high-value orders from users in a given city" in one query.
- **Common doubt:** "Can I JOIN more than two tables?" Yes, later in your career — this session limits you to **two tables** so the mental model stays clear.

### Simple Activity — Predict the JOIN Output

1. Run `SELECT * FROM users;` and `SELECT * FROM orders;` separately and note each `user_id`.
2. On paper, draw lines from each order's `user_id` to the matching user.
3. Run the INNER JOIN query above and check: do you get exactly one combined row per order?
4. Add `WHERE u.full_name = 'Ananya Sharma'` — you should see only Ananya's two orders.

---

## CRUD on Related Data — Maintaining Referential Integrity

When tables are linked, **create, read, update, delete** must respect the relationship. The database acts as a strict supervisor — not as a suggestion box.

### Insert Across Related Tables

- Always insert the **parent** (`users`) before the **child** (`orders`).
- The child's `user_id` must already exist — otherwise the insert fails immediately.

**Full Code — Add a New User and Their First Order:**

```sql
-- Add a new user and capture their new ID (PostgreSQL example pattern)
INSERT INTO users (full_name, email, city)
VALUES ('Karan Patel', 'karan@example.com', 'Ahmedabad');

-- Suppose Karan received user_id = 4; now add his order
INSERT INTO orders (user_id, item_name, amount)
VALUES (4, 'Vector DB Concepts Course', 1999.00);
```

**How the code works:**

- The second insert succeeds only because `user_id = 4` now exists in `users`.
- **Common mistake:** Inserting the order first — the database returns a foreign-key violation because the parent row is missing.

### Update Across Related Tables

**Full Code — Update an Order Status:**

```sql
-- Mark a specific order as delivered (target by order_id for precision)
UPDATE orders
SET status = 'delivered'           -- New status value
WHERE order_id = 2                 -- Only this order row changes
  AND user_id = 1;                 -- Extra safety: confirm it belongs to user 1
```

**Full Code — Update a User's Email:**

```sql
-- Change Priya's email in one place; all her orders still use user_id = 3
UPDATE users
SET email = 'priya.nair@newemail.com'
WHERE user_id = 3;
```

**How the code works:**

- Updating `users.email` does **not** require touching `orders` — orders store `user_id`, not the email string. That is the payoff of normalization.
- Adding `AND user_id = 1` on the order update prevents accidentally updating the wrong row if IDs were mistyped.

### Delete and Cascade Behaviour

**Full Code — Delete One Order Only:**

```sql
-- Remove a single order without affecting the user account
DELETE FROM orders
WHERE order_id = 2;
```

**Full Code — Delete a User (Cascade Removes Their Orders):**

```sql
-- Delete user_id 4; CASCADE removes all orders where user_id = 4
DELETE FROM users
WHERE user_id = 4;

-- Confirm: no orphaned orders should remain for that user
SELECT * FROM orders WHERE user_id = 4;
```

**How the code works:**

- `ON DELETE CASCADE` — Deleting the parent triggers automatic deletion of dependent child rows.
- Without CASCADE (e.g. `ON DELETE RESTRICT`), the database **blocks** deleting a user who still has orders — you must delete children first.
- **When CASCADE makes sense:** Child rows are meaningless without the parent (orders without a user). **When to avoid it:** Audit logs you must keep even if a user account is closed.

![Referential integrity and ON DELETE CASCADE — deleting a parent user removes linked child orders; RESTRICT blocks the delete while children still exist](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-03-referential-integrity-cascade.png)

**Full Code — Operations That Fail (On Purpose):**

```sql
-- FAILS: user_id 99 does not exist in users
INSERT INTO orders (user_id, item_name, amount)
VALUES (99, 'Ghost Order', 100.00);

-- FAILS (with RESTRICT instead of CASCADE): cannot delete user who still has orders
-- DELETE FROM users WHERE user_id = 1;
```

**How the code works:**

- These errors are **features**, not bugs — they stop AI-facing databases from storing inconsistent user–activity links.
- In agent systems, the same idea applies: you should not log an action for a `user_id` that was never created.

---

## Bridge — From Structured Data to Meaning-Based Search

You have spent several sessions learning how AI systems **store facts** in tables: who bought what, which city they live in, which order is still pending. SQL answers questions like "show orders where `city = 'Mumbai'`" perfectly — when the question is about **exact values** in **known columns**.

But much of what AI works with is **unstructured text**: support tickets, PDFs, chat history, product reviews. You also previewed **vector databases** when learning the four database types — stores built to find content by **similar meaning**, not by matching keywords in a `WHERE` clause.

Today's focus is the middle layer: **embeddings** — the numerical representations that let a computer say "these two sentences mean almost the same thing" even when they use different words. This is the foundation under semantic search, RAG retrieval, recommendations, and long-term agent memory.

![From structured SQL facts in tables to meaning-based search over unstructured text — embeddings bridge relational data and AI retrieval](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-04-sql-to-embeddings-bridge.png)

---

## Why Meaning-Based Search Matters

- **Official Definition:** **Semantic search** retrieves information based on **meaning and intent**, not only on exact character or keyword matches in stored text.
- **In Simple Words:** The system understands *what you are asking for*, not just *whether the same words appear*.
- **Real-Life Example:** You search a government portal for "how to change address on Aadhaar" — a good semantic system still finds a page titled "Update your residential details" even though the word "Aadhaar" never appears in your query.

### Where Keyword and Exact Match Break Down

| Situation | Keyword / SQL exact match | Meaning-based search |
|---|---|---|
| User writes "login problem" | May miss "reset your password" | Likely finds password-recovery docs |
| Synonyms ("cheap flights" vs "affordable tickets") | Treats as unrelated | Treats as similar intent |
| Typos or informal Hindi-English mix | Fragile | More forgiving when embeddings are trained well |
| "Refund my money" vs "I want payment back" | Different words → no match | Same intent → close vectors |

![Keyword search matches exact words; semantic search finds similar meaning even when phrasing differs — paraphrases and synonyms sit close in vector space](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-05-keyword-vs-semantic-search.png)

- **Why AI needs this:** Large language models are powerful, but they should not hallucinate facts about your company's policies. In **RAG**, the model first **retrieves** real documents by meaning, then **generates** an answer grounded in those documents.
- **Common doubt:** "If semantic search is so good, do we drop SQL?" No — structured queries (inventory, user IDs, payments) stay in relational databases; unstructured knowledge uses embeddings. Production systems use **both**.

### Simple Activity — Keyword vs Meaning (Paper Exercise)

Write three pairs of sentences that mean the same thing but share almost no words (e.g. "book a cab" / "arrange a ride for me"). Circle how many shared keywords each pair has. Discuss: would `WHERE text LIKE '%cab%'` find the second sentence? Would a human still treat them as the same request?

---

## Define Vectors and Embeddings

### Vectors — Ordered Lists of Numbers

- **Official Definition:** A **vector** is an ordered list of numbers, often written as `[x₁, x₂, …, xₙ]`, representing a point in **n-dimensional space**.
- **In Simple Words:** A vector is a fixed-length row of numbers — like coordinates that describe something in a multi-number "map."
- **Real-Life Example:** GPS uses two numbers (latitude, longitude) to place you on a map. A text embedding might use 384 or 768 numbers — many more dimensions, same idea: position in a space.

**Full Code — Simple Vector in Python (Concept Demo):**

```python
# A tiny 4-number vector — real embeddings have hundreds or thousands of numbers
sentence_a_vector = [0.12, -0.84, 1.35, 0.67]  # Stand-in for "I love dogs"

# Another vector for a similar-meaning sentence (numbers are illustrative only)
sentence_b_vector = [0.15, -0.80, 1.30, 0.70]  # Stand-in for "I like puppies"

# A vector for a different topic should look less alike in practice
sentence_c_vector = [-1.20, 0.55, 0.10, -0.90]  # Stand-in for "Stock market crashed today"
```

**How the code works:**

- Each position is one **dimension**; four numbers → 4-dimensional vector.
- Real embedding models output 384, 768, or more dimensions — you rarely interpret each number by hand.
- The list is what gets stored and compared in vector search systems.

### Embeddings — Semantic Vector Representations of Text

- **Official Definition:** An **embedding** is a dense vector produced by a model such that texts with **similar meaning** are mapped to **nearby** points in vector space.
- **In Simple Words:** Embeddings turn words, sentences, or documents into "meaning coordinates" the computer can compare mathematically.
- **Real-Life Example:** In a music app, every song is converted to a fingerprint vector; humming a tune creates another vector; the app finds the closest stored song vector — same logic as finding the closest FAQ to a user's question.

### Granularity — Word, Sentence, and Document Level

| Level | What gets embedded | Typical use |
|---|---|---|
| **Word** | Single token or word | Legacy word2vec-style tasks; less common alone in modern LLM apps |
| **Sentence** | One question or utterance | Chatbots, FAQ matching, query embedding |
| **Document** | Paragraph, page, or full article | Knowledge bases, policy PDFs, RAG document chunks |

- **Important rule for this course:** In RAG and semantic search, **documents and queries should use the same embedding model** so they live in the **same vector space**. Mixing models is like comparing addresses from two different cities using one map — distances become meaningless.
- **Common doubt:** "Do I embed the whole PDF as one vector?" Often you **split** long documents into **chunks** (smaller pieces), embed each chunk, and retrieve the most relevant chunks — not always the entire book at once.

---

## How Text Becomes Embeddings

Embeddings are not magic — they follow a pipeline. You do not need to train models yourself; you need to understand the steps so you can debug "why did search return the wrong paragraph?"

### High-Level Pipeline

1. **Raw text** — A sentence, paragraph, or document chunk enters the system.  
2. **Tokenization** — Text is split into **tokens** (subword pieces the model was trained on).  
3. **Neural encoding** — An **embedding model** reads those tokens and outputs one vector (or one vector per token, then pooled into one for the whole input).  
4. **Storage or comparison** — Vectors are saved in a database or compared directly to a query vector.

![How text becomes embeddings — raw text is tokenized, passed through an embedding model, and stored or compared as a fixed-size vector](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-06-text-to-embedding-pipeline.png)

### Tokenization — Connecting to What You Already Know

- **Official Definition:** **Tokenization** is the process of breaking text into tokens and mapping each token to a numeric ID the model can process.
- **In Simple Words:** The model does not read "Hello" as letters; it reads a sequence of token IDs — like a secret codebook shared between your text and the model.
- **Real-Life Example:** You already met **tokens** when learning about **context windows** — how much text fits in one model call. Tokenization is the step that decides how many tokens a sentence costs.

- Longer sentences → more tokens → more compute. That is why chunking long documents matters before embedding.
- Different models use different tokenizers — another reason to keep **one embedding model** for both indexing and querying.

### Embedding Models (High Level)

- **Official Definition:** An **embedding model** is a trained neural network that maps input text to a fixed-size vector capturing semantic information.
- **In Simple Words:** It is a specialised "meaning printer" — text goes in, a list of numbers comes out.
- **Real-Life Example:** OpenAI, Cohere, Google, and open-source libraries (e.g. sentence-transformers) all offer embedding APIs or downloadable models — you call the same model for every document and every user question.

**Full Code — Conceptual End-to-End (Pseudocode with Real Shape):**

```python
# Step 1: Raw text from a knowledge base chunk
document_text = "Steps to reset your account password"

# Step 2: Tokenization happens inside the model/API (you usually do not hand-split)
# tokens = tokenizer.encode(document_text)  # Hidden inside the library

# Step 3: Call the embedding model — same model name for documents AND queries later
document_vector = embed_model.encode(document_text)
# document_vector might be length 384, e.g. [0.02, -0.11, 0.45, ...]

# Step 4: Store document_vector with metadata (source file, page number, etc.)
# database.save(id="doc_42", vector=document_vector, text=document_text)

# When a user asks a question, embed the query with the SAME model
query_text = "I forgot my login password"
query_vector = embed_model.encode(query_text)

# Step 5: Compare query_vector to all stored document_vectors; return closest matches
# results = database.find_nearest(query_vector, top_k=3)
```

**How the code works:**

- `embed_model.encode(...)` stands for whatever API or library you use — the important idea is **same model, same vector length, same space**.
- Document and query vectors are compared by **closeness** (next section), not by string equality.
- **Common mistake:** Embedding documents with Model A and queries with Model B — similarity scores become unreliable.

---

## Semantic Similarity and Vector Space

- **Official Definition:** **Semantic similarity** measures how close two pieces of text are in **meaning**, often approximated by the distance or angle between their embedding vectors.
- **In Simple Words:** If two sentences mean nearly the same thing, their vectors sit close together in the embedding "map."
- **Real-Life Example:** On a real map, Indiranagar and Koramangala in Bangalore are close; Mumbai is far. In vector space, "reset password" and "recover account access" are close; "weather forecast" is far from both.

### Vector Space Intuition

Imagine a room where every sentence is a balloon floating at a position determined by its meaning:

- Balloons about **food delivery** cluster in one corner.  
- Balloons about **banking** cluster in another.  
- A new user question floats in as a new balloon; you look for the **nearest** stored balloons — those are your best document matches.

![Vector space intuition — similar meanings cluster together; a new query finds the nearest stored vectors as the best document matches](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-07-vector-space-similarity.png)

You do **not** need the full maths today. Systems typically use ideas like:

- **Distance** — How far apart two points are (closer = more similar).  
- **Angle / cosine similarity** — Whether two vectors point in the same direction, even if one is longer — common for text because it focuses on meaning direction.

- **Common doubt:** "Can similarity be 100% perfect?" In practice, scores are relative — you retrieve the **top-k closest** results, then optionally let the LLM read only those passages.

**Full Code — Toy Similarity Idea in Python (No Heavy Maths):**

```python
# Two short vectors standing in for embeddings (in reality, hundreds of dimensions)
vec_password_help = [1.0, 0.2, 0.1]
vec_forgot_login   = [0.9, 0.25, 0.05]   # Similar direction → similar meaning
vec_weather        = [0.1, 0.9, 0.8]     # Different direction → different topic

def dot_similarity(a, b):
    # Simple score: higher when corresponding numbers align (toy demo only)
    return sum(x * y for x, y in zip(a, b))

score_close = dot_similarity(vec_password_help, vec_forgot_login)
score_far   = dot_similarity(vec_password_help, vec_weather)

print(score_close)  # Expect a larger number than score_far for this toy example
print(score_far)
```

**How the code works:**

- Production systems use optimised similarity (often **cosine similarity**), not this tiny hand-written dot product — but the intuition is the same: **compare numbers, pick the closest**.
- Never compare vectors from different models or different dimensions — that is like measuring distance between addresses in India and the US using one ruler with mixed units.

### Simple Activity — Cluster by Meaning

List ten short phrases (mix of travel, food, and tech support). In groups, sort them into meaning clusters without looking at shared keywords. Then ask: "If each phrase were a vector, which clusters should sit near each other on the map?"

---

## Keyword Search vs Semantic Search

| Aspect | Keyword search | Semantic search |
|---|---|---|
| **Core idea** | Match exact words or patterns | Match meaning via embeddings |
| **Tools** | SQL `LIKE`, search engines with inverted indexes | Embedding model + vector comparison |
| **Strength** | Fast, precise filters on known fields | Handles paraphrases, intent, informal language |
| **Weakness** | Misses synonyms and rephrasing | Can occasionally retrieve loosely related text; needs good chunks |
| **Best when** | IDs, dates, statuses, regulated exact rules | Docs, chats, policies, recommendations, RAG retrieval |

- **Official Definition:** **Keyword search** finds records whose stored text contains specified terms or satisfies explicit string conditions.
- **In Simple Words:** Ctrl+F at scale — great when you know the exact word appears in the data.
- **Real-Life Example:** Finding all orders with `status = 'pending'` in SQL is keyword/field-exact logic, not semantic embedding search.

- **They work together:** "Orders from Mumbai over ₹1000" → SQL JOIN + `WHERE`. "What is our refund policy for cancelled flights?" → embed the question, retrieve policy chunks, then optionally call an LLM.

### Simple Activity — Pick the Right Tool

For each question below, write **SQL**, **keyword text search**, or **semantic search**:

1. List all users who joined in 2025.  
2. Find help articles related to "unable to sign in" when articles say "account recovery."  
3. Get `order_id` 7's current status.  

(Answers: 1 → SQL; 2 → semantic; 3 → SQL.)

---

## Semantic Search Workflow (End to End)

This is the standard pipeline you will implement in code in upcoming sessions. Today you learn the **story**; the **next** session introduces **vector databases** that store and search millions of vectors efficiently.

### Step-by-Step Workflow

1. **Store content** — Collect FAQs, PDFs, tickets, or agent memory notes; split long files into **chunks** if needed.  
2. **Embed documents** — Run each chunk through the embedding model; save vector + original text + metadata.  
3. **Embed the user query** — Same model, same settings, on the live question.  
4. **Compare vectors** — Find the **nearest** document vectors (top-k).  
5. **Return matches** — Pass retrieved text to the user directly, or into an LLM as context (RAG).

![Semantic search workflow — store chunks, embed documents and the query with the same model, compare vectors, return the nearest matches for RAG](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-08-semantic-search-workflow.png)

- **What we defer to the next session:** **Indexing**, **approximate nearest neighbour (ANN)** search, and hands-on **vector database** tools — comparing every query to every vector in a huge collection is too slow without specialised storage.
- **Common doubt:** "Is semantic search the same as ChatGPT?" No — search **finds** existing content; the LLM **generates** new language. RAG combines both: search first, generate second.

### Walkthrough Example — Support Bot

**Stored chunks (simplified):**

- Chunk A: "Steps to reset your password"  
- Chunk B: "Track your shipment"  
- Chunk C: "Request a refund for digital products"  

**User query:** "I forgot my login password"

- Keyword search might hunt for the word "forgot" or "login" and miss Chunk A if wording differs.  
- Semantic search embeds the query, finds Chunk A closest in vector space, returns it.  
- The agent or RAG layer reads Chunk A and drafts a helpful reply in natural language.

### Simple Activity — Draw the Pipeline

On one page, draw five boxes labelled: Store → Embed docs → Embed query → Compare → Return. Add one example sentence at each stage using your own college or internship scenario.

---

## Embeddings in Agentic Systems and AI Applications

Embeddings are not a standalone feature — they are infrastructure behind several patterns you will keep meeting.

![Agentic systems combine SQL for exact structured facts with vector search for semantic documents and memory before the LLM synthesises an answer](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session16/session16-09-embeddings-agentic-systems.png)

### Semantic Search and RAG

- **Semantic search** — Any system that must find "the right paragraph" by meaning: internal wikis, course portals, legal discovery.  
- **RAG (Retrieval Augmented Generation)** — Retrieve relevant chunks with embeddings, inject them into the prompt, then let the LLM answer using that evidence. Reduces fabricated policy answers.

### Recommendations and Conversational AI

- **Recommendations** — "Users who liked vectors similar to yours also bought…" — item and user descriptions are embedded, then nearest neighbours suggest the next click.  
- **Conversational AI** — Past turns or long-term memories are embedded so the agent pulls back **relevant** history, not the entire chat log every time.

### Agent Memory and Context by Meaning

- **Episodic memory** — "What did we decide last Tuesday?"  
- **Semantic memory** — Facts and concepts the agent should know.  

When memory is large, agents embed memories and retrieve by **similarity to the current goal** — e.g. current user question: "debug my API key error" → pull past troubleshooting notes about authentication, even if the word "API key" was never stored verbatim.

| Application | Role of embeddings |
|---|---|
| Support / FAQ bots | Match user intent to the right article |
| RAG knowledge assistants | Ground answers in company documents |
| E-commerce | Similar products and search by description |
| Long-running agents | Fetch relevant memories instead of full logs |

- **Structured + unstructured together:** SQL tells you **who** the user is and **what** they bought; embeddings tell you **what they are asking about** in free text. Agentic systems combine both.

---

## Bridge to Vector Databases and What Comes Next

You now know **what** embeddings are and **how** semantic search works conceptually. The open engineering question is scale: what happens when you have **millions** of chunks?

- Comparing one query vector to every stored vector by brute force works for small demos only.  
- **Vector databases** (and extensions like pgvector inside PostgreSQL) are built to **store**, **index**, and **retrieve** embeddings quickly at scale.  
- In the **next** session, you will connect this theory to **vector databases**, similarity search at scale, and indexing ideas — still conceptual first, then hands-on implementation in later labs.

For now, hold this split clearly in your mind:

- **Relational SQL** → exact facts in tables (users, orders, statuses).  
- **Embeddings** → meaning of unstructured text.  
- **Vector databases** → fast home for millions of embedding vectors (coming next).

---

## Key Takeaways

- **INNER JOIN** on two related tables answers "who did what" in one query by matching foreign keys to primary keys; always insert parent rows before child rows and let foreign keys enforce consistency.
- **CRUD on related data** must respect referential integrity; **ON DELETE CASCADE** automatically removes child rows when a parent is deleted, while **RESTRICT** forces you to delete children first.
- **Embeddings** convert text into vectors so that similar meaning → nearby points in vector space; use the **same embedding model** for documents and queries.
- **Semantic search** retrieves by meaning (workflow: store → embed docs → embed query → compare → return top matches); **keyword/SQL search** remains essential for exact structured filters.
- Embeddings power **RAG**, **recommendations**, **conversational AI**, and **agent memory retrieval** — they sit between raw text and the systems that need trustworthy, context-aware answers.

In the **next** session, you will see how **vector databases** store and search these embeddings efficiently when your data grows beyond small classroom examples — completing the path from SQL tables to meaning-based AI retrieval.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| `INNER JOIN` | SQL | Returns rows where a match exists in **both** tables on the join condition |
| `ON table.column = other.column` | SQL | Specifies which columns link the two tables |
| `FOREIGN KEY ... REFERENCES` | SQL | Child column must point to an existing parent primary key |
| `ON DELETE CASCADE` | SQL | Deletes child rows when the referenced parent row is deleted |
| `ON DELETE RESTRICT` | SQL | Blocks parent delete while child rows still reference it |
| Referential integrity | Concept | Database rule that foreign keys always reference real parent rows |
| Vector | Concept | Ordered list of numbers representing a point in multi-dimensional space |
| Embedding | Concept | Vector produced from text (or other data) that encodes semantic meaning |
| Token / Tokenization | Concept | Subword units and the process of converting text to token IDs for models |
| Embedding model | Tool / API | Neural model that maps text to a fixed-size semantic vector |
| Semantic similarity | Concept | Closeness of meaning, approximated by vector distance or angle |
| Vector space | Concept | Abstract map where each embedding is a point; similar texts sit near each other |
| Keyword search | Concept | Retrieval based on exact terms or field matches |
| Semantic search | Concept | Retrieval based on embedding similarity and meaning |
| Top-k retrieval | Concept | Return the k closest vectors to the query vector |
| Chunking | Concept | Splitting long documents into smaller pieces before embedding |
| RAG | Concept | Retrieve relevant documents by embedding, then generate an answer with an LLM |
| Vector database | Concept | Specialised store for embeddings and fast similarity search at scale |
| Cosine similarity | Concept | Common similarity measure based on angle between vectors (name only today) |
