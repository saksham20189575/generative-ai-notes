# Using SQL Databases with AI Applications

## Context of This Session

In the previous session, we built the entire foundation of working with databases. We understood why file-based storage fails at scale, explored the four major types of databases (Relational, NoSQL, Vector, and Time-Series), learned all the core SQL vocabulary (tables, rows, columns, keys, constraints, data types), set up Supabase, and wrote our first CRUD queries — `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, and `DELETE`. We also mastered the `WHERE` clause with filtering operators like `LIKE`, `BETWEEN`, and `IN`.

That session gave you the tools to work with a *single table*. But real-world AI applications — whether a recommendation engine, a customer support agent, or a booking system — never rely on just one table. Data is always spread across multiple related tables that work together. This session takes you from working with isolated tables to understanding *how tables talk to each other*, and how to query them together using one of the most powerful SQL concepts: **JOINs**.

**In this session, you will:**

- Quickly recap the CRUD operations from the previous session and bridge into advanced querying
- Use `ORDER BY`, `LIMIT`, and `OFFSET` to sort results, cap the output, and paginate data
- Understand why data is split across multiple tables and how **relationships** between tables work
- Learn the three types of relationships — one-to-one, one-to-many, and many-to-many
- Design and create related tables with **foreign key constraints** in Supabase
- Write your first **INNER JOIN** query to combine data from two related tables
- Perform CRUD operations across related tables while maintaining **referential integrity**

---

## Quick Recap — CRUD Operations from Session 14

Before we move forward, let's lock in the core SQL commands you learned last session. Every new concept in this session builds directly on top of these.

| SQL Command | What It Does | Quick Example |
|---|---|---|
| `CREATE TABLE` | Defines a new table with columns and constraints | `CREATE TABLE students (...)` |
| `INSERT INTO` | Adds a new row of data | `INSERT INTO students VALUES (...)` |
| `SELECT` | Reads data from a table | `SELECT * FROM students` |
| `UPDATE` | Modifies existing rows | `UPDATE students SET city = 'Delhi' WHERE student_id = 1` |
| `DELETE` | Removes rows permanently | `DELETE FROM students WHERE student_id = 1` |
| `WHERE` | Filters which rows are affected | `WHERE city = 'Mumbai' AND is_active = TRUE` |

- **The golden rule from last session:** Always use `WHERE` with `UPDATE` and `DELETE` — without it, the operation runs on every row in the table.
- **What we are building on today:** `SELECT` queries that do more than just retrieve data — they sort it, limit it, and pull it from multiple related tables at once.

---

## Sorting, Limiting, and Pagination — ORDER BY, LIMIT, OFFSET

When you run `SELECT * FROM students`, the database returns rows in whatever internal order it chooses — not necessarily the order you want. And when your table has thousands of rows, you do not want all of them returned at once. This is where `ORDER BY`, `LIMIT`, and `OFFSET` come in.

Think of these as the controls on a music streaming app — not only can you search for songs, you can also sort them by most played, show only the top 10, and skip to the next page of results.

### ORDER BY — Sorting Results

- **Official Definition:** `ORDER BY` is a SQL clause that sorts the result set of a query by one or more specified columns, in either ascending (`ASC`) or descending (`DESC`) order.
- **In Simple Words:** `ORDER BY` is the "sort by" button. It arranges the returned rows in the order you specify — alphabetically, by date, by number, etc.
- **Real-Life Example:** On Zomato, when you search for restaurants, you can sort by rating (highest first) or by delivery time (fastest first). That sorting is powered by `ORDER BY` behind the scenes.

**Full Code — Sorting Students:**

```sql
-- Sort all students alphabetically by their full name (A to Z)
SELECT * FROM students
ORDER BY full_name ASC;        -- ASC = Ascending (A to Z, 1 to 100, oldest to newest)

-- Sort students by enrollment date, most recent first
SELECT * FROM students
ORDER BY enrollment_date DESC; -- DESC = Descending (Z to A, 100 to 1, newest to oldest)

-- Sort students by city, then by name within the same city
SELECT full_name, city, course FROM students
ORDER BY city ASC, full_name ASC;  -- First sorts by city, then by name within each city
```

**How the code works:**

- `ORDER BY column_name ASC` — Sorts results in ascending order. For text, this is A → Z. For numbers, this is 1 → 100. For dates, this is oldest → newest.
- `ORDER BY column_name DESC` — Reverses the sort. Most recent dates come first, largest numbers come first.
- You can chain multiple columns after `ORDER BY` with commas — the database sorts by the first column, and when two rows are tied, it uses the second column as a tiebreaker.

### LIMIT — Capping the Number of Results

- **Official Definition:** `LIMIT` is a SQL clause that restricts the number of rows returned by a query to a specified maximum.
- **In Simple Words:** `LIMIT` is like saying "show me only the first 10 results." Even if the table has 10,000 rows, only the number you specify is returned.
- **Real-Life Example:** When you search for something on Google, you see 10 results per page — not all 2 billion results at once. That cap is `LIMIT` in action.

**Full Code — Limiting Results:**

```sql
-- Show only the first 5 students from the table
SELECT * FROM students
LIMIT 5;

-- Show the top 3 most recently enrolled students
SELECT full_name, enrollment_date FROM students
ORDER BY enrollment_date DESC
LIMIT 3;
```

**How the code works:**

- `LIMIT 5` — Returns at most 5 rows, regardless of how many rows exist in the table.
- Combining `ORDER BY` + `LIMIT` is extremely powerful — sort by a column, then take only the top N results. This is the pattern behind "top 10 charts," "most recent articles," and "highest scored entries."

### OFFSET — Skipping Rows for Pagination

- **Official Definition:** `OFFSET` is a SQL clause used together with `LIMIT` to skip a specified number of rows before starting to return results. This is used to implement **pagination** — showing data in pages.
- **In Simple Words:** `OFFSET` is like saying "skip the first 10 results and show me the next 5." Combined with `LIMIT`, it lets you show data page by page.
- **Real-Life Example:** On Flipkart, page 1 shows products 1–20, page 2 shows products 21–40, page 3 shows 41–60. Each page is the same `LIMIT` with a different `OFFSET`.

**Full Code — Implementing Pagination:**

```sql
-- Page 1: Show the first 3 students (rows 1 to 3)
SELECT full_name, city FROM students
ORDER BY student_id ASC
LIMIT 3 OFFSET 0;    -- Skip 0 rows, then show 3

-- Page 2: Show the next 3 students (rows 4 to 6)
SELECT full_name, city FROM students
ORDER BY student_id ASC
LIMIT 3 OFFSET 3;    -- Skip the first 3 rows, then show 3

-- Page 3: Show the next 3 students (rows 7 to 9)
SELECT full_name, city FROM students
ORDER BY student_id ASC
LIMIT 3 OFFSET 6;    -- Skip the first 6 rows, then show 3
```

**How the code works:**

- `OFFSET 0` — Start from the very beginning (no rows skipped). This is page 1.
- `OFFSET 3` — Skip the first 3 rows. This gives you page 2 when your page size is 3.
- The pattern is: `OFFSET = (page_number - 1) × page_size`. For page 4 with a page size of 3, `OFFSET = 9`.
- In AI applications, pagination is used to retrieve data in batches — for example, loading conversation history in chunks rather than all at once, which would be expensive and slow.

![ORDER BY sorts result rows, LIMIT caps how many rows you see, OFFSET skips ahead for paging through large slices of data](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session15/session15-01-order-limit-offset.png)

---

## Understanding Database Relationships — Why Single Tables Are Not Enough

You have been working with a single `students` table. Now imagine an AI system for a real university. You need to track students, the courses they enroll in, the teachers who teach those courses, and the marks each student gets in each course.

If you put everything in one table, you end up with a massive problem called **data redundancy** — the same teacher's name and details are repeated on every single row for every student who takes their course. If the teacher's phone number changes, you have to update hundreds of rows.

- **Official Definition:** **Data redundancy** means storing the same piece of information in multiple places in a database. It wastes storage, creates inconsistency, and makes updates error-prone.
- **In Simple Words:** If Rahul's phone number is written 500 times across 500 rows, and his number changes, you have to update 500 rows. Miss even one, and your data becomes inconsistent. The solution is to store Rahul's details *once* and just *reference* them from other tables.
- **Real-Life Example:** Instead of writing a student's full address on every exam paper, you write their roll number. The roll number points to the official address record stored in one place. If the address changes, only one record needs updating.

### What Is Normalization?

- **Official Definition:** **Normalization** is the process of organising a database to reduce redundancy and improve data integrity by dividing data into separate tables and defining relationships between them.
- **In Simple Words:** Normalization means "don't repeat yourself." Split your data into logical, focused tables — each table talks about one thing — and connect them with keys.
- **Real-Life Example:** A hospital doesn't write the doctor's full bio on every appointment record. It keeps a `doctors` table and an `appointments` table, and the appointment just stores the doctor's ID. That ID is the bridge between the two tables.

![Heavy redundancy in one wide table versus normalized tables linked by IDs — fewer repeated facts and simpler updates across related records](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session15/session15-02-normalization-redundancy.png)

---

## Types of Relationships Between Tables

There are three fundamental types of relationships in relational databases. Every database you encounter — from a banking system to an AI agent's memory store — uses one or more of these.

### One-to-One Relationship

- **Official Definition:** A **one-to-one relationship** exists when exactly one row in Table A corresponds to exactly one row in Table B — and vice versa.
- **In Simple Words:** Each record in one table has at most one matching record in the other table. Think of it as a direct 1:1 pairing.
- **Real-Life Example:** Every Indian citizen has exactly one Aadhaar card, and every Aadhaar card belongs to exactly one citizen. Citizen → Aadhaar is a one-to-one relationship.
- **Used in AI:** Separating sensitive user data (email, phone) from public profile data (username, bio) for security purposes.

### One-to-Many Relationship

- **Official Definition:** A **one-to-many relationship** exists when one row in Table A can be linked to multiple rows in Table B, but each row in Table B links back to only one row in Table A.
- **In Simple Words:** One thing can have many related things, but each of those related things belongs to only one parent. This is the most common relationship in databases.
- **Real-Life Example:** One customer can place many orders, but each order belongs to only one customer. That is one-to-many: `customers` (one) → `orders` (many).
- **Used in AI:** One user can have many conversation sessions with an agent; one agent can have many tool-use logs.

### Many-to-Many Relationship

- **Official Definition:** A **many-to-many relationship** exists when multiple rows in Table A can be associated with multiple rows in Table B — and vice versa. This requires a **junction table** (also called a bridge table) to store the associations.
- **In Simple Words:** Many things relate to many other things. You need a third table in the middle to track all the combinations.
- **Real-Life Example:** A student can enroll in many courses, and each course can have many students. Neither a single `students` table nor a single `courses` table can capture all the combinations — you need an `enrollments` junction table with `student_id` and `course_id`.
- **Used in AI:** Products and categories (one product can belong to multiple categories; one category can have multiple products); users and roles (one user can have multiple roles).

| Relationship Type | Real-Life Example | Database Pattern |
|---|---|---|
| **One-to-One** | Citizen ↔ Aadhaar | One row in A, one row in B |
| **One-to-Many** | Customer → Orders | One row in A, many rows in B |
| **Many-to-Many** | Students ↔ Courses | Junction table required |

![One-to-one, one-to-many, and many-to-many patterns — including a junction table when both sides need many matches](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session15/session15-03-relationship-types.png)

### Referential Integrity

- **Official Definition:** **Referential integrity** is a database rule that ensures a foreign key value in one table always corresponds to an existing primary key value in the referenced table. You cannot have an orphaned record that points to something that doesn't exist.
- **In Simple Words:** If an order in the `orders` table says it belongs to `customer_id = 99`, then customer number 99 must actually exist in the `customers` table. You cannot have an order that belongs to a ghost customer.
- **Real-Life Example:** If you delete a teacher from the `teachers` table, you cannot leave behind class records that still point to that deleted teacher ID. The database will either block the deletion or automatically clean up the related records.

![Referential integrity keeps foreign-key values pointing at real parent rows — bad inserts are rejected so related data cannot drift](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session15/session15-04-referential-integrity.png)

---

## Designing and Creating Related Tables in Supabase

Now let us move from theory to practice. We will build two related tables — `customers` and `orders` — linked by a foreign key. This models one of the most common real-world scenarios and is directly applicable to how AI systems manage user data and transaction histories.

### Step 1 — Create the `customers` Table (the "One" side)

```sql
-- Create a table to store customer information
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,     -- Auto-incrementing unique ID for each customer
    full_name VARCHAR(100) NOT NULL,    -- Customer's full name; required
    email VARCHAR(150) UNIQUE NOT NULL, -- Unique email per customer; required
    city VARCHAR(50),                   -- City of the customer (optional)
    created_at TIMESTAMP DEFAULT NOW()  -- Automatically records when the customer was added
);
```

**How the code works:**

- `SERIAL PRIMARY KEY` — Each customer gets a unique, auto-assigned ID (1, 2, 3...).
- `TIMESTAMP DEFAULT NOW()` — `NOW()` is a PostgreSQL function that inserts the current date and time automatically when a new row is added.
- This table is the "parent" table — orders will reference it.

### Step 2 — Create the `orders` Table (the "Many" side)

```sql
-- Create a table to store order information; each order belongs to one customer
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,             -- Auto-incrementing unique ID for each order
    customer_id INT NOT NULL,                -- Foreign key: references the customers table
    product_name VARCHAR(200) NOT NULL,      -- Name of the product ordered
    amount DECIMAL(10, 2) NOT NULL,          -- Price of the order (up to 10 digits, 2 decimal places)
    order_status VARCHAR(50) DEFAULT 'pending',  -- Order status: pending, shipped, delivered
    ordered_at TIMESTAMP DEFAULT NOW(),      -- Time the order was placed

    -- Define the foreign key constraint
    CONSTRAINT fk_customer                   -- Give the constraint a descriptive name
        FOREIGN KEY (customer_id)            -- This column in orders...
        REFERENCES customers (customer_id)   -- ...must match a customer_id in the customers table
        ON DELETE CASCADE                    -- If the customer is deleted, delete their orders too
);
```

**How the code works:**

- `customer_id INT NOT NULL` — Every order must have a customer. This column stores the ID of the customer who placed the order.
- `DECIMAL(10, 2)` — Stores a number with up to 10 total digits and exactly 2 decimal places — ideal for money values like `1299.99`.
- `CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)` — This is the relationship definition. It tells the database: "the `customer_id` in this table must exist in the `customers` table."
- `ON DELETE CASCADE` — If a customer record is deleted from `customers`, all their orders in `orders` are automatically deleted too. This prevents orphaned order records.
- **Without the foreign key constraint**, you could insert an order with `customer_id = 9999` even if that customer doesn't exist — your data would be meaningless.

### Step 3 — Visualise the Schema in Supabase

After creating both tables in the Supabase SQL Editor:

- Click **Database** in the left sidebar
- Select **Tables** — you will see both `customers` and `orders` listed
- The foreign key relationship is visible in the table inspector under the `orders` table
- In the **Table Editor**, when you open `orders`, Supabase shows the linked `customers` reference — making the relationship visible and clickable

---

## Inserting Data into Related Tables

When inserting data across related tables, the **order matters**. You must insert the parent record first, then the child record — because the child's foreign key must reference an existing parent.

**Full Code — Inserting Customers First:**

```sql
-- Insert customers into the parent table first
INSERT INTO customers (full_name, email, city)
VALUES
    ('Ananya Sharma', 'ananya@example.com', 'Bangalore'),  -- Gets customer_id = 1
    ('Rohan Mehta', 'rohan@example.com', 'Mumbai'),        -- Gets customer_id = 2
    ('Priya Nair', 'priya@example.com', 'Chennai'),        -- Gets customer_id = 3
    ('Karan Patel', 'karan@example.com', 'Ahmedabad');     -- Gets customer_id = 4
```

**Full Code — Inserting Orders That Reference Those Customers:**

```sql
-- Insert orders linked to existing customers via customer_id
INSERT INTO orders (customer_id, product_name, amount)
VALUES
    (1, 'Python for AI — Course Bundle', 2999.00),   -- Ananya's order
    (1, 'Supabase Pro Subscription', 499.00),         -- Ananya's second order
    (2, 'LangChain Masterclass', 1499.00),            -- Rohan's order
    (3, 'AI Agents Handbook (PDF)', 299.00),          -- Priya's order
    (3, 'Prompt Engineering Workshop', 799.00),       -- Priya's second order
    (4, 'Vector Database Course', 1999.00);           -- Karan's order
```

**How the code works:**

- Customers are inserted first — their `customer_id` values are auto-assigned (1, 2, 3, 4).
- Each order row's `customer_id` is manually set to match an existing customer (1 = Ananya, 2 = Rohan, etc.).
- Ananya and Priya each have two orders — this is the "many" side of the one-to-many relationship in action.
- If you tried to insert an order with `customer_id = 99` (which doesn't exist), the database would reject it immediately due to the foreign key constraint — referential integrity in action.

---

## Querying Relational Data with INNER JOIN

You now have two tables with related data. The fundamental question is: **how do you pull information from both tables in a single query?** This is what `JOIN` is for.

Without a JOIN, you would have to run two separate queries and manually connect the results — which is slow, error-prone, and not practical for AI systems that need combined data instantly.

- **Official Definition:** A **JOIN** is a SQL operation that combines rows from two or more tables based on a related column between them — typically a foreign key and its matching primary key.
- **In Simple Words:** A JOIN is like merging two spreadsheets. You tell the database "these two columns in the two tables are the same ID — use that to stitch the rows together."
- **Real-Life Example:** Imagine a report that shows "customer name + their total orders." The name lives in `customers`, the orders live in `orders`. A JOIN bridges them: for each order, attach the customer's name from the customers table using the matching `customer_id`.

![INNER JOIN stitches rows where the matching key columns line up across two tables — only pairs that exist on both sides appear in the result](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session15/session15-05-inner-join.png)

### INNER JOIN — The Most Common JOIN

- **Official Definition:** An **INNER JOIN** returns only the rows where there is a match in **both** tables based on the join condition. Rows from either table that have no matching row in the other table are excluded.
- **In Simple Words:** INNER JOIN says "show me only the records that exist in both tables." If a customer has no orders, they won't appear. If an order has no valid customer (which the foreign key prevents), it won't appear either.
- **Real-Life Example:** Think of two guest lists for two different parties. INNER JOIN gives you only the people who are on **both** lists — the common members.

### Anatomy of an INNER JOIN Query

```sql
SELECT columns_you_want
FROM first_table
INNER JOIN second_table
    ON first_table.shared_column = second_table.shared_column
WHERE optional_filter;
```

**Full Code — Show All Orders with Their Customer Names:**

```sql
-- Combine orders with customer details using INNER JOIN
SELECT 
    customers.full_name,          -- Customer's name from the customers table
    customers.city,               -- Customer's city from the customers table
    orders.product_name,          -- Product ordered from the orders table
    orders.amount,                -- Order amount from the orders table
    orders.order_status,          -- Current order status from the orders table
    orders.ordered_at             -- When the order was placed
FROM orders                       -- Start with the orders table
INNER JOIN customers              -- Bring in the customers table
    ON orders.customer_id = customers.customer_id;  -- Match on the shared customer_id column
```

**How the code works:**

- `FROM orders` — The query starts with the `orders` table as the base.
- `INNER JOIN customers ON orders.customer_id = customers.customer_id` — For each row in `orders`, find the matching row in `customers` where the `customer_id` values are equal. Stitch them together.
- `customers.full_name` — You prefix columns with their table name to avoid confusion when both tables have columns with the same name (e.g., both might have a `created_at` column).
- The result has one row per order, with the customer's name and city filled in from the customers table — no separate query needed.

**Full Code — Using Table Aliases to Make the Query Cleaner:**

```sql
-- Same query as above but using short aliases 'c' and 'o' for readability
SELECT 
    c.full_name,        -- c refers to the customers table
    c.city,
    o.product_name,     -- o refers to the orders table
    o.amount,
    o.order_status
FROM orders o                        -- 'o' is the alias for orders
INNER JOIN customers c               -- 'c' is the alias for customers
    ON o.customer_id = c.customer_id -- Use aliases in the JOIN condition too
ORDER BY c.full_name ASC;            -- Sort results alphabetically by customer name
```

**How the code works:**

- `FROM orders o` — The letter `o` is a short alias (nickname) for the `orders` table. You can use `o` instead of writing `orders` everywhere.
- `INNER JOIN customers c` — Similarly, `c` stands for `customers`.
- Aliases make long queries much easier to read and write — especially when joining three or more tables.
- `ORDER BY c.full_name ASC` — Sorts the combined result by customer name. This shows all of Ananya's orders together, then Karan's, then Priya's, then Rohan's.

**Full Code — Filter JOINed Results with WHERE:**

```sql
-- Show all orders placed by customers from Mumbai only
SELECT 
    c.full_name,
    c.city,
    o.product_name,
    o.amount
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.city = 'Mumbai';             -- Filter AFTER the JOIN, on the combined result

-- Show all orders with an amount above 1000 rupees
SELECT 
    c.full_name,
    o.product_name,
    o.amount
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.amount > 1000.00
ORDER BY o.amount DESC;              -- Most expensive orders first
```

**How the code works:**

- `WHERE c.city = 'Mumbai'` — The `WHERE` clause filters the already-joined result set. Only rows where the customer's city is Mumbai survive.
- You can filter on columns from either table — `c.city` (from customers) or `o.amount` (from orders) — because both are available after the JOIN.
- This is how an AI agent would retrieve "all high-value orders placed by users in a specific region" — a single JOIN query, not two separate lookups.

---

## CRUD on Related Data — Maintaining Referential Integrity

When your data lives in multiple related tables, CRUD operations need to be done carefully to preserve the relationships. The database's foreign key constraint is your guardian — it blocks operations that would break the data's consistency.

### Updating Records in Related Tables

**Full Code — Update an Order's Status:**

```sql
-- Mark Rohan's order as 'delivered'
UPDATE orders
SET order_status = 'delivered'          -- Change status to delivered
WHERE order_id = 3                      -- Target Rohan's specific order (order_id 3)
  AND customer_id = 2;                  -- Extra safety: confirm it belongs to Rohan (customer_id 2)
```

**Full Code — Update a Customer's Email:**

```sql
-- Update Priya's email address in the customers table
UPDATE customers
SET email = 'priya.nair@newemail.com'   -- New email value
WHERE customer_id = 3;                  -- Target Priya specifically using her unique ID
```

**How the code works:**

- Updates to `customers` automatically reflect anywhere `customer_id = 3` is used — because `orders` stores the ID, not the name or email. This is the power of normalization.
- Adding `AND customer_id = 2` to the order update is a safety practice — it ensures you are modifying the right order for the right customer.

### Deleting Records and Cascade Behavior

**Full Code — Delete a Specific Order:**

```sql
-- Delete one specific order (Ananya's Supabase subscription order)
DELETE FROM orders
WHERE order_id = 2;                     -- Only removes order_id 2, not all of Ananya's orders
```

**Full Code — Delete a Customer (Cascade in Action):**

```sql
-- Delete Karan from the customers table
-- Because orders table has ON DELETE CASCADE, Karan's orders are automatically deleted too
DELETE FROM customers
WHERE customer_id = 4;                  -- Deletes Karan's customer record

-- Verify: Karan's order (order_id 6) should also be gone
SELECT * FROM orders WHERE customer_id = 4;  -- Returns 0 rows because of CASCADE
```

**How the code works:**

- `ON DELETE CASCADE` — When you delete a row from the parent table (`customers`), the database automatically deletes all child rows in `orders` that referenced that parent. No manual cleanup needed.
- **What happens without CASCADE?** If you had used `ON DELETE RESTRICT` (the default behaviour), the database would *block* the deletion of the customer as long as any orders reference them. You would have to delete the orders first, then the customer.
- **When to use CASCADE:** Use it when child records have no meaning without their parent — an order without a customer is meaningless. Avoid it for critical audit trails where you want to preserve historical records even after a parent is deleted.

### Attempting to Break Referential Integrity (and What Happens)

```sql
-- This will FAIL because customer_id = 99 does not exist in the customers table
INSERT INTO orders (customer_id, product_name, amount)
VALUES (99, 'Some Product', 500.00);
-- Error: insert or update on table "orders" violates foreign key constraint "fk_customer"
-- Detail: Key (customer_id)=(99) is not present in table "customers"

-- This will also FAIL if Ananya still has orders (without CASCADE)
DELETE FROM customers WHERE customer_id = 1;
-- Error: update or delete on table "customers" violates foreign key constraint "fk_customer"
-- Detail: Key (customer_id)=(1) is still referenced from table "orders"
```

**How the code works:**

- These examples show the database actively enforcing referential integrity — it rejects data that would create inconsistency.
- In AI systems, this is extremely valuable — it means your agent's memory store, user profiles, and activity logs can never get into a corrupted state due to bad write operations.

---

## How This Applies to AI Applications

Everything you have learned in this session maps directly to how real AI systems store and retrieve data. Let us connect the dots.

### Sorting and Pagination in AI Systems

- An AI customer support agent retrieves the **most recent conversation** — `ORDER BY started_at DESC LIMIT 1`.
- A recommendation engine shows the **top 5 products** for a user based on purchase score — `ORDER BY score DESC LIMIT 5`.
- A dashboard loads user activity in **pages** — `LIMIT 20 OFFSET 0` for page 1, `LIMIT 20 OFFSET 20` for page 2.

### Relationships in AI Memory Systems

- An AI agent stores **user profiles** in one table and **conversation sessions** in another — a one-to-many relationship (one user → many sessions).
- A **tool-use log** for an agent connects to the session table (one session → many tool calls) — another one-to-many.
- A **recommendation system** maps users to products they have interacted with — a many-to-many relationship via a junction table.

### JOINs in AI Queries

- An agent retrieving context before responding: `SELECT u.name, s.summary FROM sessions s INNER JOIN users u ON s.user_id = u.user_id WHERE s.session_id = 'abc123'` — pulls the user's name and the session summary together in one query.
- A reporting system showing "which agent handled which ticket" — `INNER JOIN` between an `agents` table and a `tickets` table.
- All of this happens in **Supabase**, which you already have set up — making it immediately usable in your future AI projects.

![How sorting, paging, relational models, and JOIN queries show up behind agents, dashboards, and production Supabase backends](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session15/session15-06-sql-in-ai-apps.png)

---

## Key Takeaways

- **ORDER BY, LIMIT, and OFFSET** are the tools for controlling *how* results come back — sorted, capped, and paginated. These are not optional extras; they are standard in every production AI system that displays data.
- **Relationships between tables** are the backbone of real-world databases. By splitting data across focused tables and linking them with foreign keys, you eliminate redundancy, keep data consistent, and make updates effortless.
- **The three relationship types** cover every scenario — one-to-one for direct pairings, one-to-many for the most common parent-child patterns, and many-to-many via junction tables for complex associations.
- **INNER JOIN** is how you combine related tables in a single query — matching rows via the shared key column and producing a merged result set. It is one of the most frequently used SQL operations in any data-driven application.
- **Referential integrity is your safety net.** The foreign key constraint blocks bad writes (orphaned records), and `ON DELETE CASCADE` automates cleanup. In AI systems, this means your data store cannot corrupt itself through invalid operations.
- **What comes next:** In the next session, we will connect Python directly to Supabase — writing code that performs these queries programmatically, which is how AI agents interact with databases in real applications.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| `ORDER BY` | SQL Clause | Sorts query results by one or more columns; `ASC` = ascending, `DESC` = descending |
| `LIMIT` | SQL Clause | Restricts the number of rows returned by a query |
| `OFFSET` | SQL Clause | Skips a specified number of rows before returning results; used for pagination |
| `INNER JOIN` | SQL Clause | Combines rows from two tables where a matching value exists in both |
| `ON` | SQL Keyword | Specifies the condition used to match rows across tables in a JOIN |
| `ON DELETE CASCADE` | Constraint Behaviour | Automatically deletes child rows when the parent row is deleted |
| `ON DELETE RESTRICT` | Constraint Behaviour | Blocks deletion of a parent row if child rows still reference it |
| `NOW()` | SQL Function | Returns the current date and time; used as a default for timestamp columns |
| `DECIMAL(p, s)` | Data Type | Stores precise decimal numbers with `p` total digits and `s` decimal places |
| `CONSTRAINT` | SQL Keyword | Names and defines a rule (e.g., foreign key) applied to a table |
| **Relationship** | Concept | A defined link between two tables based on matching key columns |
| **One-to-One** | Relationship Type | One row in Table A matches exactly one row in Table B |
| **One-to-Many** | Relationship Type | One row in Table A matches many rows in Table B (most common type) |
| **Many-to-Many** | Relationship Type | Many rows in A match many rows in B; requires a junction table |
| **Junction Table** | Concept | A bridge table that resolves a many-to-many relationship |
| **Normalization** | Concept | Organising a database to reduce redundancy by splitting data into focused tables |
| **Data Redundancy** | Concept | Storing the same data in multiple places — causes inconsistency and update problems |
| **Referential Integrity** | Concept | A rule ensuring foreign key values always reference an existing primary key |
| **Foreign Key** | Constraint | Links a column in one table to the primary key of another table |
| **CASCADE** | Behaviour | Propagates a delete/update from the parent table to all related child rows |
| **Alias** | SQL Concept | A short nickname for a table name used within a query (`FROM orders o`) |
| **Pagination** | Concept | Breaking large data sets into smaller pages using `LIMIT` and `OFFSET` |
| **INNER JOIN** | Concept | Returns only rows with matching values in both joined tables |
| **Supabase Schema View** | Tool Feature | Visual display of table structure and foreign key relationships in the Supabase dashboard |
