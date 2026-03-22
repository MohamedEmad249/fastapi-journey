import asyncio
from fastapi import FastAPI, HTTPException
from models import Book, BorrowRecord

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "The Game Of Thrones",
        "author": "George R. R. Martin",
        "pages": 1052,
        "borrow_records": []
    },
    {"id": 2,
        "title": "Clash Of Kings",
        "author": "George R. R. Martin",
        "pages": 531,
        "borrow_records": []
    },
    {
        "id": 3,
        "title": "Feast Of Crows",
        "author": "George R. R. Martin",
        "pages": 1346,
        "borrow_records": []
    }
]

@app.get("/books/")
async def get_books():
    return books

@app.get("/books/{id}")
async def get_book(id: int):
    for book in books:
        if book["id"] == id:
            await asyncio.sleep(1)
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/")
async def create_book(book: Book):
    books.append(book.dict())
    return book.dict()

@app.put("/books/{id}")
async def update_book(id: int, book: Book):
    for i, existing_book in enumerate(books):
        if existing_book["id"] == id:
            books[i] = book.dict()
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}")
async def delete_book(id: int):
    for book in books:
        if book["id"] == id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
