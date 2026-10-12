# Library API

سیستم کتابداری ساده با FastAPI. داده‌ها در حافظه (یک متغیر در کد) نگه‌داری می‌شوند و با ری‌استارت سرور ریست می‌شوند.

## اجرا

```bash
python -m venv .venv
source .venv/bin/activate      # ویندوز: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

مستندات تعاملی: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path | توضیح |
|---|---|---|
| GET | /books | لیست کتاب‌ها |
| POST | /books | افزودن کتاب |
| GET | /books/{id} | اطلاعات یک کتاب |
| PATCH | /books/{id} | ویرایش بخشی از اطلاعات |
| DELETE | /books/{id} | حذف کتاب |
