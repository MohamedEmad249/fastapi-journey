# Section 1 — Field types
====================================================================
Why int for id?

Using `int` for the `id` field is a common design choice, especially in a project like this, for several reasons:

1. **Simplicity & Prototyping**: It's very easy to manage (e.g., `1`, `2`, `3`) when working with an in-memory dummy database (like your `books` list in `main.py`). It makes generating new IDs straightforward (just get the max ID and add 1).
2. **Database Alignment**: In traditional relational databases (like SQLite, PostgreSQL, MySQL), the standard practice for primary keys is to use auto-incrementing integers. Starting with `int` mimics real-world database behavior and makes it easier to migrate to an actual database later.
3. **URL Readability**: It creates clean, user-friendly API routes like `/books/1` instead of long strings, making manual testing via Swagger UI or browser much simpler.
4. **FastAPI Integration**: FastAPI easily automatically parses and validates path parameters like `/books/{id}` when you specify `id: int` in your endpoint function signatures.
5. **Performance**: Integer comparisons are generally faster and take up less memory than string (like UUID) comparisons, which is efficient for indexing and searching.
====================================================================
Why List for borrow_records?

Using a `list` for `borrow_records` is a natural fit for representing a one-to-many relationship in Python, especially when working with Pydantic and FastAPI. Here's why it's a good choice:

1. **One-to-Many Relationship**: A single book can be borrowed multiple times by different people over time. A list allows you to store an ordered sequence of all borrow records associated with that book.
2. **Flexibility**: Lists are dynamic and can grow or shrink as needed. As a book is borrowed and returned, you can easily append new `BorrowRecord` objects to the list or remove them when necessary.
3. **Data Structure Alignment**: Pydantic's `List` type hint directly maps to Python's built-in list, making it straightforward to define and work with this data structure.
4. **Serialization**: FastAPI and Pydantic can easily serialize and deserialize lists of objects to and from JSON, which is the standard format for API responses.
5. **Querying**: When you retrieve a book, you can easily iterate through the `borrow_records` list to check its borrowing history, find the current borrower, or perform any other operations on the records.
6. **Simplicity**: For a simple in-memory database, a list is a straightforward and efficient way to store and manage the borrow records without the need for more complex data structures.
====================================================================
# Section 2 — Validation
Why title has min_length?

Enforcing a minimum length (e.g., `min_length=2`) for a string like the book's `title` (and `borrower_name`) ensures basic data quality. It prevents API clients from creating useless entries with empty strings (`""`) or single-character titles. Pydantic handles this validation automatically before the request even reaches your endpoint logic, returning a clean 422 Unprocessable Entity error if the rule isn't met.
====================================================================
Why pages > 0?

A real book logically must have at least one page. A book with 0 or negative pages indicates invalid or corrupt data. By using `Field(gt=0)`, you express this business rule directly in the data model. Pydantic guarantees that whenever a `Book` object is instantiated via the API, the page count is strictly greater than zero, which completely eliminates the need to write manual `if pages <= 0:` checks inside your route handlers.
====================================================================
Why return_date is optional?

When a book is initially borrowed, the borrower takes the book but hasn't returned it yet. This means the `return_date` is unknown at the time the record is created. Defining `return_date: Optional[str] = None` perfectly models this real-world scenario. It allows new `BorrowRecord` entries to be saved with just the `borrower_name` and `borrow_date`, leaving the `return_date` empty (`None`) until the book is actually returned.
====================================================================
# Section 3 — Async
Which endpoint uses async delay?
The endpoint that uses async delay is the GET endpoint for a specific book id, i.e., /books/{id}.
If you look at 
main.py
 around line 34, the 
get_book
 function is defined as:

 @app.get("/books/{id}")
async def get_book(id: int):
    for book in books:
        if book["id"] == id:
            await asyncio.sleep(1) # <--- Async delay is used here
            return book
    raise HTTPException(status_code=404, detail="Book not found")

====================================================================
