# Introduction to Databases for AI Systems

## Context of This Session

In the previous session, we went deep into how AI agents handle memory — both short-term memory that lives within a conversation, and long-term memory that persists across sessions. We explored strategies like Buffer Memory, Window Memory, and Summary Memory for managing short-term context, and we understood the three types of long-term memory: Episodic, Semantic, and Procedural. Towards the end, we touched on the idea that long-term memory must be stored somewhere — a file, a database, or a vector store.

That "somewhere" is exactly what this session is all about. Think of the previous session as understanding *why* agents need to remember things over time. This session answers *where* and *how* that data is actually stored, organised, and retrieved — which is the foundation of every intelligent AI system.

**In this session, you will:**

- Understand why simple file-based storage (like CSV or Excel) breaks down at scale and why databases were invented
- Explore the four main types of databases and when each is used in AI systems
- Learn core SQL vocabulary — tables, rows, columns, keys, schemas, and data types
- Set up and explore **Supabase**, a browser-based database tool that requires zero installation
- Write your first SQL queries to create tables, insert data, read records, update values, and delete rows
- Use the powerful `WHERE` clause to filter and retrieve exactly the data you need
- Understand the difference between structured and unstructured data and why it matters for AI

---

## Why Data Storage Matters — The Problem with Files

Every AI system, at its core, works with data. Whether it is a chatbot remembering user preferences, a recommendation engine suggesting products, or an agent recalling past decisions — all of it needs to be stored somewhere and retrieved quickly.

Most beginners start storing data in Excel files or CSVs. This feels natural because everyone has used a spreadsheet. But as the system grows, file-based storage starts causing very serious problems.

### The Breakdown of File-Based Storage

- **Official Definition:** **File-based storage** refers to saving data in flat files such as `.csv`, `.xlsx`, or plain text files on a computer or server — without any built-in mechanism for querying, enforcing structure, or handling simultaneous access.
- **In Simple Words:** You are basically saving your data the same way you save a Word document. It works fine when you are alone, but falls apart when many people or systems try to use it at the same time.
- **Real-Life Example:** Imagine a school that keeps all student records in a single Excel file. One teacher opens it, another tries to edit it at the same time — the file gets corrupted. Now imagine 10,000 students across 100 schools. The file becomes unmanageable.

**Problems that file-based storage cannot solve:**

- **Scalability** — A CSV file with 10 million rows becomes extremely slow to open, search, or update.
- **Consistency** — Two people editing the same file at the same time can overwrite each other's changes.
- **Concurrent Access** — Files are not designed to be accessed by multiple systems or users simultaneously.
- **Queryability** — Finding "all students who scored above 80 in Mathematics" in a CSV requires reading the whole file line by line — there is no built-in way to filter smartly.
- **Relationships** — If student data is in one file and marks data is in another, linking them is messy and error-prone.

![File-based spreadsheets versus a managed database — scale, clashes, and why teams outgrow CSV and Excel alone](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session14/session14-01-file-vs-database.png)

### What a Database Solves

- **Official Definition:** A **database** is an organised collection of structured data, managed by a software called a **Database Management System (DBMS)**, which provides tools to store, retrieve, update, and delete data efficiently and reliably.
- **In Simple Words:** A database is like a very intelligent filing cabinet with a trained librarian who can find any record in seconds, let multiple people access it at once, and make sure no one's data gets overwritten by accident.
- **Real-Life Example:** Think of a bank. Thousands of customers are checking balances, making transfers, and withdrawing cash — all at the same time. This only works because a database is handling every transaction with precision, not an Excel sheet.

**What databases give you:**

- **Speed** — Databases use special internal structures (called indexes) to find records instantly, even in millions of rows.
- **Concurrent Access** — Multiple users and systems can read and write data at the same time without conflicts.
- **Data Integrity** — Rules can be enforced — for example, a student's age cannot be stored as "apple."
- **Relationships** — Data across multiple tables can be linked, so you do not duplicate information.
- **Security** — Access can be controlled — some users can only read, others can write.

---

## Types of Databases — Choosing the Right Tool for AI

Not all databases are the same. Just like you would not use a hammer to cut wood, different types of databases are built for different problems. In AI systems, you will encounter four major types.

### Relational Databases (SQL)

- **Official Definition:** A **relational database** stores data in structured **tables** made up of rows and columns. Tables can be linked to each other using **keys**. You interact with them using **SQL** (Structured Query Language).
- **In Simple Words:** Think of it like a very organised set of spreadsheets where all the sheets are connected. You define strict rules about what kind of data goes where, and SQL lets you ask questions across all the sheets at once.
- **Real-Life Example:** A hospital database — one table for patients, another for doctors, another for appointments. They are all linked so you can ask "Show me all appointments for Dr. Sharma next week."
- **When used in AI:** Storing structured training data, logging model outputs, managing user records in AI-powered apps, transaction history for financial AI systems.
- **Examples:** MySQL, PostgreSQL, Supabase (PostgreSQL-based), SQLite.

### NoSQL Databases (Document / Key-Value)

- **Official Definition:** **NoSQL databases** store data in formats other than relational tables — such as JSON documents, key-value pairs, graphs, or wide columns. They are flexible and do not require a fixed schema.
- **In Simple Words:** If a relational database is a filing cabinet with strict labelled folders, a NoSQL database is a box where you can throw in papers of any shape or size. It is more flexible but harder to keep organised.
- **Real-Life Example:** Think of a user profile in an app. One user has a phone number, another doesn't. One has 3 addresses, another has none. NoSQL can handle this irregular structure easily.
- **When used in AI:** Storing user conversation histories, session logs, flexible agent memory, product catalogs in e-commerce AI.
- **Examples:** MongoDB (document), Redis (key-value), DynamoDB (AWS).

### Vector Databases

- **Official Definition:** A **vector database** stores data as **mathematical vectors** — numerical representations of content like text, images, or audio — and is optimised to find similar items quickly using mathematical distance calculations.
- **In Simple Words:** When an AI reads a sentence, it converts it into a long list of numbers (a vector). A vector database stores these number lists and can instantly find "which stored sentence is most similar to this new query?" This is the engine behind AI memory retrieval and semantic search.
- **Real-Life Example:** Imagine you hum a tune and an app identifies the song. The hummed tune is converted to a vector, compared against millions of stored song vectors, and the nearest match is returned. That is vector search.
- **When used in AI:** Long-term memory for agents (retrieving relevant past conversations), semantic search, recommendation engines, RAG (Retrieval Augmented Generation) systems.
- **Examples:** Pinecone, Weaviate, ChromaDB, pgvector (inside PostgreSQL/Supabase).

### Time-Series Databases

- **Official Definition:** A **time-series database** is optimised to store and query data that is indexed by time — where every record has a timestamp and queries typically involve ranges of time.
- **In Simple Words:** These databases are designed for data that changes constantly over time — like a heart rate monitor or a stock price ticker. They make it very fast to ask "show me all readings from the last 30 minutes."
- **Real-Life Example:** Think of a smartwatch that records your heart rate every second. A regular database would struggle to store and retrieve 86,400 entries per day per user efficiently. A time-series database handles this without breaking a sweat.
- **When used in AI:** Monitoring AI model performance over time, IoT sensor data in industrial AI, financial market analysis, anomaly detection systems.
- **Examples:** InfluxDB, TimescaleDB, Amazon Timestream.

| Database Type | Format | Best For in AI | Example Tools |
|---|---|---|---|
| **Relational (SQL)** | Tables with rows & columns | Structured data, logs, user records | MySQL, PostgreSQL, Supabase |
| **NoSQL** | Documents, key-value, graphs | Flexible data, chat histories | MongoDB, Redis |
| **Vector** | Numerical vectors | Semantic search, agent memory | Pinecone, ChromaDB |
| **Time-Series** | Time-stamped records | Monitoring, sensor data, anomaly detection | InfluxDB, TimescaleDB |

![The four database families used in AI — relational tables, flexible NoSQL, vector search, and time-stamped streams](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session14/session14-02-four-database-types.png)

---

## Core SQL Terminologies — The Vocabulary You Must Know

Now that you know relational databases are the foundation of most AI-powered applications, let's learn the language they speak. Before writing a single query, you need to understand the building blocks.

Think of a relational database as a well-organised **office building**. The building is the database, each **floor is a table**, each **row is one employee's file**, and each **column is a field** on that form (name, ID, department, etc.).

![Office-building analogy — database as the building, tables as floors, rows as records, and columns as labelled fields](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session14/session14-03-sql-office-building.png)

### Table

- **Official Definition:** A **table** is the primary structure in a relational database where data is stored in a grid of rows and columns, similar to a spreadsheet tab.
- **In Simple Words:** One table = one category of data. You have a `students` table, a `courses` table, an `orders` table — each dedicated to one type of thing.
- **Real-Life Example:** In a school, the attendance register is a table — one row per student per day, with columns for date, name, and present/absent.

### Row (Record)

- **Official Definition:** A **row** (also called a **record** or **tuple**) represents a single entry in a table — one complete set of information about one item.
- **In Simple Words:** One row = one thing. In a `students` table, each row is one student.
- **Real-Life Example:** In a hospital patient table, each row is one patient — their ID, name, age, and blood group.

### Column (Field / Attribute)

- **Official Definition:** A **column** (also called a **field** or **attribute**) represents one specific property or characteristic of the data stored in a table. All values in a column must be of the same data type.
- **In Simple Words:** Columns are the "categories" of information. In a `students` table, you might have columns: `student_id`, `name`, `age`, `email`.
- **Real-Life Example:** On an Aadhaar card form, each box you fill (name, DOB, address) is a column in the database table.

### Schema

- **Official Definition:** A **schema** is the formal structure or blueprint of a database — it defines all the tables, what columns each table has, the data types of those columns, and the relationships between tables.
- **In Simple Words:** A schema is like the architecture plan of a building — before construction starts, it defines where every room goes, how big each room is, and how the rooms are connected.
- **Real-Life Example:** Before building a hotel booking app, you define: "We will have a `hotels` table, a `rooms` table, and a `bookings` table, and here is exactly what each table looks like." That plan is the schema.

### Primary Key

- **Official Definition:** A **primary key** is a column (or combination of columns) in a table whose value is **unique for every row** and **cannot be null**. It is used to uniquely identify each record.
- **In Simple Words:** The primary key is the unique ID for every row — no two rows can have the same primary key value. It is how the database knows exactly which record you are talking about.
- **Real-Life Example:** Your **Aadhaar number** is a primary key in the government's database. Every Indian citizen has a different one, and no one is allowed to have the same number. The system uses it to pull up your exact record.
- **Common mistake to avoid:** Never use a person's name as a primary key — two students can have the same name. Always use a unique ID.

### Foreign Key

- **Official Definition:** A **foreign key** is a column in one table that **references the primary key** of another table. It is used to establish and enforce a link (relationship) between two tables.
- **In Simple Words:** A foreign key is how tables talk to each other. It says "this value in my table corresponds to a row in another table."
- **Real-Life Example:** In a school database, the `marks` table has a column `student_id`. That `student_id` is a foreign key — it points to the `student_id` (primary key) in the `students` table. This connection tells you whose marks they are without repeating all student details.

![Primary keys uniquely identify a row in one table; foreign keys safely reference rows in another table](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session14/session14-04-primary-foreign-keys.png)

### Constraints

- **Official Definition:** **Constraints** are rules applied to columns to control what kind of data can be entered. They enforce data integrity at the database level.
- **In Simple Words:** Constraints are like the validation rules on a form — they prevent bad data from entering the database.
- **Common constraints:**
  - `NOT NULL` — The column cannot be left empty. Example: `name NOT NULL` means every student must have a name.
  - `UNIQUE` — Every value in this column must be different. Example: email addresses.
  - `PRIMARY KEY` — Combines NOT NULL + UNIQUE for the identifier column.
  - `FOREIGN KEY` — Ensures the value exists in the referenced table.
  - `DEFAULT` — Sets a default value if none is provided.
  - `CHECK` — Validates that a value meets a condition. Example: `age > 0`.

### Data Types

- **Official Definition:** A **data type** defines the kind of value a column can store — numbers, text, dates, booleans, etc. The database enforces that only the correct type of data is inserted.
- **In Simple Words:** Data types are like labels on jars in a kitchen — the jar labelled "Sugar" should only contain sugar. If you try to put salt in it, the system rejects it.
- **Commonly used data types in SQL:**

| Data Type | What It Stores | Example |
|---|---|---|
| `INT` / `INTEGER` | Whole numbers | 1, 42, 1000 |
| `FLOAT` / `DECIMAL` | Numbers with decimals | 3.14, 99.99 |
| `VARCHAR(n)` | Variable-length text up to n characters | "Rahul", "Delhi" |
| `TEXT` | Long text with no size limit | Paragraph, descriptions |
| `BOOLEAN` | True or False | TRUE, FALSE |
| `DATE` | Date only | 2024-01-15 |
| `TIMESTAMP` | Date + Time | 2024-01-15 10:30:00 |
| `SERIAL` / `UUID` | Auto-incrementing ID or unique identifier | 1, 2, 3… or unique code |

---

## Where SQL Can Be Written — MySQL vs Supabase

You now know the vocabulary. Before writing queries, let us understand *where* you write them. There are several platforms available.

### MySQL (Traditional Setup)

- **Official Definition:** **MySQL** is one of the most widely used open-source relational database systems. It requires installation on your computer or server and is managed through a local interface or terminal.
- **In Simple Words:** MySQL is powerful and widely used in production systems, but it requires you to install software, configure settings, and manage the database locally.
- **Limitation for beginners:** The setup process can be tricky — port conflicts, permission issues, and command-line usage can be a barrier for those new to tech.

### Supabase — Our Go-To Tool

- **Official Definition:** **Supabase** is an open-source Backend-as-a-Service (BaaS) platform built on top of **PostgreSQL** (one of the most powerful SQL databases). It provides a browser-based dashboard, a SQL editor, and auto-generated APIs — all without any installation.
- **In Simple Words:** Supabase is like having a full-featured database that runs in your browser. You go to the website, create a project, and immediately start writing SQL — no installation, no configuration, no terminal commands.
- **Why Supabase for this course:**
  - **Zero installation** — works entirely in the browser
  - **Visual table UI** — you can see your data in a clean spreadsheet-like view
  - **Built-in SQL editor** — write and run queries directly in the browser
  - **Future-ready** — Supabase connects directly to AI systems, Python backends, and automation tools we will use in upcoming sessions
  - **Free tier available** — no cost to get started

> **Instructor Note:** The rest of this session will be conducted entirely inside Supabase. All SQL queries will be executed in the Supabase SQL editor.

---

## Setting Up and Exploring Supabase

Let's walk through setting up your Supabase workspace step by step.

### Step 1 — Create a Supabase Account

- Go to [https://supabase.com](https://supabase.com) and click **Start your project**
- Sign in with your GitHub account (recommended) or email
- Once logged in, you will land on the **Supabase Dashboard**

### Step 2 — Create a New Project

- Click **New Project**
- Choose your **organisation** (Supabase creates one by default with your account name)
- Give your project a name — for example: `ai_systems_db`
- Set a **Database Password** — save this somewhere; you will need it later
- Choose a **Region** closest to you (e.g., Southeast Asia — Singapore)
- Click **Create New Project** and wait about 60 seconds for setup

### Step 3 — Explore the Dashboard

Once your project is ready, familiarise yourself with the left sidebar:

| Section | What It Does |
|---|---|
| **Table Editor** | View and manage your tables visually — like a spreadsheet |
| **SQL Editor** | Write and run SQL queries directly |
| **Database** | View table schemas, functions, and extensions |
| **Authentication** | Manage users and login methods |
| **Storage** | Store files (images, PDFs, etc.) |
| **Edge Functions** | Run server-side code |
| **API Docs** | Auto-generated API documentation for your tables |

**For this session, you will primarily use:** the **Table Editor** and the **SQL Editor**.

---

## Creating Tables and Inserting Data — CREATE & INSERT

Now that Supabase is ready, let's create our first table. We will use a relatable real-world example: a **student management system** for an AI course.

### The CREATE TABLE Statement

- **Official Definition:** `CREATE TABLE` is a SQL command used to define and create a new table in the database, specifying its columns, data types, and constraints.
- **In Simple Words:** `CREATE TABLE` is like designing a new registration form — you decide what fields exist, what type of data goes in each field, and what rules apply.

**Full Code — Creating the `students` Table:**

```sql
-- Create a table called 'students' to store student information
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,      -- Auto-incrementing unique ID for each student
    full_name VARCHAR(100) NOT NULL,     -- Student's full name; cannot be empty
    email VARCHAR(150) UNIQUE NOT NULL,  -- Email must be unique and cannot be empty
    course VARCHAR(100) NOT NULL,        -- The course the student is enrolled in
    city VARCHAR(50),                    -- City where the student is from (optional)
    enrollment_date DATE DEFAULT CURRENT_DATE,  -- Defaults to today's date if not provided
    is_active BOOLEAN DEFAULT TRUE       -- Whether the student is currently enrolled
);
```

**How the code works:**

- `SERIAL PRIMARY KEY` — `SERIAL` means the database automatically assigns the next number (1, 2, 3...) to `student_id` for every new row. `PRIMARY KEY` means it uniquely identifies each student.
- `VARCHAR(100) NOT NULL` — Stores text up to 100 characters; the field cannot be left blank.
- `UNIQUE NOT NULL` on `email` — Every student must have an email, and no two students can share the same email.
- `DEFAULT CURRENT_DATE` — If you do not provide an enrollment date, today's date is filled in automatically.
- `BOOLEAN DEFAULT TRUE` — The `is_active` column starts as `TRUE` for every new student unless you say otherwise.

### The INSERT INTO Statement

- **Official Definition:** `INSERT INTO` is a SQL command used to add new rows (records) of data into an existing table.
- **In Simple Words:** `INSERT INTO` is like filling in a registration form and submitting it. Each `INSERT` adds one (or more) complete records to the table.

**Full Code — Inserting Multiple Students:**

```sql
-- Insert the first student record
INSERT INTO students (full_name, email, course, city)
VALUES ('Ananya Sharma', 'ananya@example.com', 'Agentic Systems and Design', 'Bangalore');

-- Insert a second student
INSERT INTO students (full_name, email, course, city)
VALUES ('Rohan Mehta', 'rohan@example.com', 'Agentic Systems and Design', 'Mumbai');

-- Insert a third student with no city provided
INSERT INTO students (full_name, email, course)
VALUES ('Priya Nair', 'priya@example.com', 'Agentic Systems and Design');

-- Insert multiple students in a single INSERT statement
INSERT INTO students (full_name, email, course, city)
VALUES 
    ('Karan Patel', 'karan@example.com', 'Agentic Systems and Design', 'Ahmedabad'),
    ('Sana Mirza', 'sana@example.com', 'Agentic Systems and Design', 'Hyderabad'),
    ('Dev Joshi', 'dev@example.com', 'Agentic Systems and Design', 'Pune');
```

**How the code works:**

- `INSERT INTO students (column1, column2, ...)` — You name which columns you are providing values for.
- `VALUES (...)` — You provide the actual data in the same order as the column names listed above.
- `student_id` is not mentioned because `SERIAL` fills it automatically — the database handles it.
- `enrollment_date` and `is_active` are also not mentioned because they have `DEFAULT` values.
- Priya's row has no `city` — that column allows `NULL` (no `NOT NULL` constraint), so it is stored as empty.

---

## Reading Data with SELECT Queries

You have created a table and inserted data. Now let's read it back. The `SELECT` statement is the most frequently used SQL command — you will write it in almost every query.

- **Official Definition:** `SELECT` is a SQL command used to retrieve data from one or more tables. You specify which columns to return and from which table.
- **In Simple Words:** `SELECT` is your question to the database. "Hey database, show me this data." The database finds it and returns it to you.
- **Real-Life Example:** Think of `SELECT` as using the search bar in your email inbox. You are asking "show me all emails from Rahul" — the system retrieves exactly those and displays them.

![How SELECT, FROM, and WHERE fit together — choose the table, filter rows, then project the columns you need](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session14/session14-05-select-from-where-flow.png)

### Anatomy of a SELECT Query

```sql
SELECT column1, column2    -- Which columns to show
FROM table_name            -- Which table to look in
WHERE condition;           -- (Optional) Which rows to include
```

**Full Code — Reading All Students:**

```sql
-- Retrieve every column and every row from the students table
SELECT * FROM students;
```

**How the code works:**

- `SELECT *` — The `*` (asterisk) means "all columns." Show me every piece of information.
- `FROM students` — Tells the database to look in the `students` table.
- This returns every row that has been inserted — like opening the full attendance register.

**Full Code — Retrieving Specific Columns Only:**

```sql
-- Retrieve only the name and email of all students
SELECT full_name, email FROM students;

-- Retrieve only name, city, and course of all students
SELECT full_name, city, course FROM students;
```

**How the code works:**

- Instead of `*`, you list exactly which columns you need.
- The database returns only those columns, even though the table has more. This is more efficient, especially with large tables.

---

## Updating and Deleting Records — UPDATE & DELETE

Data changes over time. Students move cities, update emails, or leave courses. The `UPDATE` and `DELETE` commands handle these changes.

### The UPDATE Statement

- **Official Definition:** `UPDATE` is a SQL command used to modify existing values in one or more rows of a table.
- **In Simple Words:** `UPDATE` is like editing a record in a form that has already been submitted. You find the row and change specific values in it.
- **Critical rule:** **Always use a `WHERE` clause with UPDATE.** Without `WHERE`, you will update every single row in the table — a mistake that is very hard to undo.

**Full Code — Updating a Student's City:**

```sql
-- Update Ananya's city from Bangalore to Chennai
UPDATE students
SET city = 'Chennai'            -- The column to change and its new value
WHERE email = 'ananya@example.com';  -- Find ONLY the row with this email
```

**Full Code — Marking a Student as Inactive:**

```sql
-- Mark Rohan as no longer active in the course
UPDATE students
SET is_active = FALSE           -- Change is_active to FALSE
WHERE full_name = 'Rohan Mehta'; -- Only update Rohan's row
```

**Full Code — Updating Multiple Columns at Once:**

```sql
-- Update Karan's city and course together
UPDATE students
SET city = 'Delhi',
    course = 'AI Product Design'
WHERE student_id = 4;           -- Using student_id is the safest way to target one row
```

**How the code works:**

- `SET column = new_value` — Specify which column to change and what value to put in.
- `WHERE condition` — Tells the database exactly which row(s) to update.
- Using `student_id` in the `WHERE` clause is the safest approach because it uniquely identifies one row.

### The DELETE Statement

- **Official Definition:** `DELETE` is a SQL command used to remove one or more rows from a table permanently.
- **In Simple Words:** `DELETE` is like shredding a file in the filing cabinet. Once deleted, the row is gone from the database permanently (unless you have a backup).
- **Critical warning:** Just like `UPDATE`, **always use `WHERE` with DELETE.** `DELETE FROM students;` without a `WHERE` clause will erase every single student record instantly.

**Full Code — Deleting a Specific Student:**

```sql
-- Remove the record of the student with student_id = 6
DELETE FROM students
WHERE student_id = 6;           -- Only delete Dev Joshi's record (student_id 6)
```

**Full Code — Deleting Based on a Condition:**

```sql
-- Remove all students who are marked as inactive
DELETE FROM students
WHERE is_active = FALSE;
```

**How the code works:**

- `DELETE FROM students` — Targets the `students` table for deletion.
- `WHERE student_id = 6` — The `WHERE` clause limits which row gets deleted. Only the row where `student_id` equals 6 is removed.
- Without `WHERE`, this would delete all rows — treat this like a live wire; always attach the `WHERE` clause.

---

## Filtering Data with the WHERE Clause

The `WHERE` clause is arguably the most important part of SQL. It lets you retrieve, update, or delete *exactly the rows you care about*. A query without `WHERE` is like searching your entire house for your keys — `WHERE` is like knowing they are in the kitchen.

- **Official Definition:** The `WHERE` clause is a conditional filter applied in `SELECT`, `UPDATE`, and `DELETE` statements that restricts which rows are affected based on a specified condition.
- **In Simple Words:** `WHERE` is the "only if" part of your query. "Show me students *only if* they are from Bangalore." "Delete records *only if* they are inactive."

### Comparison Operators

```sql
-- Students from Mumbai
SELECT * FROM students WHERE city = 'Mumbai';

-- Students whose student_id is greater than 2
SELECT * FROM students WHERE student_id > 2;

-- Students who enrolled before 2025
SELECT * FROM students WHERE enrollment_date < '2025-01-01';

-- Students who are NOT from Bangalore
SELECT * FROM students WHERE city != 'Bangalore';
```

### Logical Operators — AND, OR, NOT

**Full Code — Using AND (both conditions must be true):**

```sql
-- Students from Bangalore AND currently active
SELECT * FROM students
WHERE city = 'Bangalore' AND is_active = TRUE;
```

**Full Code — Using OR (at least one condition must be true):**

```sql
-- Students from either Mumbai or Pune
SELECT * FROM students
WHERE city = 'Mumbai' OR city = 'Pune';
```

**Full Code — Using NOT (reverse a condition):**

```sql
-- All students who are NOT from Delhi
SELECT * FROM students
WHERE NOT city = 'Delhi';
```

### Pattern Matching — LIKE

- **Official Definition:** `LIKE` is a SQL operator used for pattern matching in text columns. It uses `%` as a wildcard for any sequence of characters and `_` for exactly one character.
- **In Simple Words:** `LIKE` is SQL's version of a Google search with wildcard characters. The `%` symbol means "anything can go here."

```sql
-- Find all students whose name starts with 'A'
SELECT * FROM students WHERE full_name LIKE 'A%';

-- Find all students whose email ends with '@example.com'
SELECT * FROM students WHERE email LIKE '%@example.com';

-- Find all students whose name contains 'an' anywhere
SELECT * FROM students WHERE full_name LIKE '%an%';
```

### Range Matching — BETWEEN

```sql
-- Find students with student_id between 2 and 5 (inclusive)
SELECT * FROM students WHERE student_id BETWEEN 2 AND 5;

-- Find students enrolled in the year 2024
SELECT * FROM students 
WHERE enrollment_date BETWEEN '2024-01-01' AND '2024-12-31';
```

### List Matching — IN

```sql
-- Find students from a specific list of cities
SELECT * FROM students 
WHERE city IN ('Mumbai', 'Bangalore', 'Hyderabad');

-- Find students NOT in these cities
SELECT * FROM students 
WHERE city NOT IN ('Delhi', 'Pune');
```

**How all the filtering works — summary:**

- **Comparison operators** (`=`, `>`, `<`, `!=`, `>=`, `<=`) compare a column's value to a given value.
- **AND** requires *all* conditions to be true for a row to be returned.
- **OR** requires *at least one* condition to be true.
- **NOT** flips the condition — includes rows that would have been excluded.
- **LIKE** searches for text patterns; `%` is "anything," `_` is exactly one character.
- **BETWEEN** checks if a value falls within a range (both ends inclusive).
- **IN** checks if a value is in a list of options.

---

## Structured vs Unstructured Data — What It Means for AI

We have been working with **structured data** — data that fits neatly into rows and columns with defined types. But most of the world's data is actually **unstructured**. Understanding this difference is essential for anyone building AI systems.

### Structured Data

- **Official Definition:** **Structured data** is data that is organised into a predefined format — typically rows and columns with specific data types — that can be easily stored, searched, and analysed using SQL.
- **In Simple Words:** Structured data is data that fits into a table. Every value knows exactly which box it belongs in.
- **Examples in AI:** Student records, transaction histories, sensor readings, user click logs, product inventory.
- **Stored in:** Relational databases (MySQL, PostgreSQL, Supabase), spreadsheets.

### Unstructured Data

- **Official Definition:** **Unstructured data** is data that does not have a predefined format or schema. It includes text documents, images, audio files, videos, emails, and social media posts.
- **In Simple Words:** Unstructured data is anything that cannot naturally fit into a neat table. A WhatsApp message, a photo, a voice recording — these are unstructured.
- **Examples in AI:** Training data for language models (raw text), images for computer vision, audio for speech recognition, customer reviews for sentiment analysis.
- **Stored in:** File systems, object storage (like AWS S3), NoSQL databases, or converted into vectors and stored in vector databases.

![Structured data fits cleanly into relational tables queried with SQL; rich media and free text stay unstructured until models or embeddings reshape them](https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/iitr-as-260313/module2/session14/session14-06-structured-vs-unstructured.png)

### Why This Distinction Matters in AI

| Aspect | Structured Data | Unstructured Data |
|---|---|---|
| **Format** | Tables, rows, columns | Text, images, audio, video |
| **Query Method** | SQL | AI models, NLP, Computer Vision |
| **Storage** | Relational databases | File systems, NoSQL, Vector DBs |
| **Volume** | Typically smaller, well-defined | Huge — 80%+ of all data in the world |
| **AI Use** | Feature engineering, logs, rules | Training data, embeddings, inputs |

- When an AI agent retrieves a user's past purchase history — that is **structured data** from a relational database.
- When an AI reads a customer review and decides the sentiment is "positive" — that is processing **unstructured text**.
- When an AI searches its memory for "what did this user talk about 3 sessions ago?" — it converts the old conversations (unstructured) into vectors and searches a **vector database**.

Understanding which type of data you are working with directly determines which database type to use — and this is why we started this session by learning all four database types.

---

## Key Takeaways

- **Databases solve real problems** that file-based storage cannot handle at scale — concurrent access, speed, data integrity, and queryability. For any AI system that handles real users and real data, a database is non-negotiable.
- **Four database types serve four different needs:** Relational (SQL) for structured records, NoSQL for flexible data, Vector databases for AI memory and semantic search, and Time-Series for timestamped data streams.
- **SQL is the language of relational databases.** You learned the core commands: `CREATE TABLE` to define structure, `INSERT` to add data, `SELECT` to read, `UPDATE` to modify, and `DELETE` to remove — and the `WHERE` clause to apply precision to any of them.
- **Supabase makes database work accessible.** No installation, a visual interface, and a browser-based SQL editor lower the barrier to working with real databases — and it connects directly to AI systems we will build in upcoming sessions.
- **Structured data lives in tables; unstructured data lives everywhere else.** As we move deeper into AI agents, you will see how both types of data are used together — structured data to manage agent state and logs, unstructured data as input to AI models.
- **What comes next:** In the upcoming sessions, we will connect this database knowledge directly to Python and AI workflows — writing code that reads from and writes to Supabase, and eventually building agents that use databases as their persistent memory layer.

---

## Important Commands, Libraries, and Terminologies

| Term / Command | Type | Meaning |
|---|---|---|
| `CREATE TABLE` | SQL Command | Defines and creates a new table with columns and constraints |
| `INSERT INTO` | SQL Command | Adds new rows of data into a table |
| `SELECT` | SQL Command | Retrieves data from a table |
| `UPDATE` | SQL Command | Modifies existing values in one or more rows |
| `DELETE` | SQL Command | Permanently removes rows from a table |
| `WHERE` | SQL Clause | Filters rows based on a condition |
| `AND` / `OR` / `NOT` | Logical Operators | Combine multiple conditions in a WHERE clause |
| `LIKE` | SQL Operator | Pattern matching for text — `%` = any sequence, `_` = one character |
| `BETWEEN` | SQL Operator | Checks if a value is within a range (inclusive) |
| `IN` | SQL Operator | Checks if a value exists in a provided list |
| `PRIMARY KEY` | Constraint | Unique, non-null identifier for each row in a table |
| `FOREIGN KEY` | Constraint | Links a column to the primary key of another table |
| `NOT NULL` | Constraint | Column must always have a value; cannot be empty |
| `UNIQUE` | Constraint | All values in the column must be different |
| `DEFAULT` | Constraint | Sets an automatic value if no value is provided |
| `SERIAL` | Data Type | Auto-incrementing integer, commonly used for primary keys |
| `VARCHAR(n)` | Data Type | Variable-length text with a maximum of n characters |
| `BOOLEAN` | Data Type | Stores TRUE or FALSE |
| `TIMESTAMP` | Data Type | Stores both date and time |
| **Relational Database** | Concept | Database that stores data in structured tables linked by keys |
| **NoSQL Database** | Concept | Database for flexible, non-tabular data formats |
| **Vector Database** | Concept | Database optimised for storing and searching mathematical embeddings |
| **Time-Series Database** | Concept | Database optimised for time-stamped sequential data |
| **Schema** | Concept | The structural blueprint of a database — tables, columns, types, and relationships |
| **Structured Data** | Concept | Data organised in tables with a fixed format and data types |
| **Unstructured Data** | Concept | Data without a fixed format — text, images, audio, video |
| **Supabase** | Tool | Browser-based PostgreSQL database with a visual interface and SQL editor |
| **MySQL** | Tool | Widely-used open-source relational database system |
| **PostgreSQL** | Tool | Powerful open-source SQL database; the engine behind Supabase |
| **SQL** | Language | Structured Query Language — used to interact with relational databases |
| **DBMS** | Concept | Database Management System — software that manages a database |
