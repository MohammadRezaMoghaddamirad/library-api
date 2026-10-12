from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Library API", description="سیستم کتابداری ساده با FastAPI", version="1.0.0")


# ---------- مدل‌ها ----------
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, description="عنوان کتاب")
    author: str = Field(..., min_length=1, description="نویسنده")
    year: Optional[int] = Field(None, ge=0, description="سال انتشار")
    isbn: Optional[str] = Field(None, description="شابک")


class BookUpdate(BaseModel):
    # همه فیلدها اختیاری هستند (برای PATCH)
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=0)
    isbn: Optional[str] = None


class Book(BookCreate):
    id: int


# ---------- داده در حافظه (بدون دیتابیس) ----------
books: dict[int, dict] = {
    1: {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "isbn": "9780132350884"},
    2: {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999, "isbn": "9780201616224"},
}
next_id = 3


def get_book_or_404(book_id: int) -> dict:
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


# ---------- API ها ----------
@app.get("/books", response_model=list[Book])
def list_books():
    """دریافت لیست همه کتاب‌ها"""
    return list(books.values())


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate):
    """اضافه کردن کتاب جدید"""
    global next_id
    book = {"id": next_id, **payload.model_dump()}
    books[next_id] = book
    next_id += 1
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    """گرفتن اطلاعات یک کتاب خاص"""
    return get_book_or_404(book_id)


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate):
    """تغییر بخشی از اطلاعات یک کتاب"""
    book = get_book_or_404(book_id)
    book.update(payload.model_dump(exclude_unset=True))
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    """حذف یک کتاب خاص"""
    get_book_or_404(book_id)
    del books[book_id]
