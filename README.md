# **📚 Bookly**

![image](https://github.com/user-attachments/assets/fe640d5f-0759-4947-967e-7be155f22505)


## 1. Overview

**Bookly** is a high performance FastAPI-based Book API, RESTful web service designed for managing book-related data efficiently and securely. Built using **FastAPI**, this API enables developers to perform full **CRUD operations (Create, Read, Update, Delete)** on books and related entities such as authors, genres, and publishers.

**Key Features:**

- 🚀 **Fast & Asynchronous:** Powered by FastAPI’s async capabilities for high performance and scalability.
- 🔐 **Secure Authentication:** Optional JWT-based authentication for protected endpoints.
- 🧾 **CRUD Functionality:** Endpoints for adding, retrieving, updating, and deleting books.
- 🔍 **Search & Filtering:** Easily filter books by title, author, genre, or publication year.
- 📦 **Modular Design:** Clean, modular project structure following best practices for scalability and maintainability.
- 📄 **Interactive Docs:** Automatically generated Swagger UI and ReDoc for easy API exploration and testing.

**Use Cases:**

- Digital library systems
- Online bookstores
- Educational apps needing book data
- Inventory tracking for physical book collections

This API serves as a solid foundation for any book-related application, whether you're building a lightweight catalog app or a robust online library system.

### Tech stack

🔹 **FastAPI** — Modern, fast (high-performance) web framework.  
🔹 **Pydantic** - Pydantic is a Python library used for data validation and settings management using Python type annotations.  
🔹 **SQLModel** — Designed to combine the best of SQLAlchemy and Pydantic.

---

## 2. User Instruction

Getting started as a user is easy! 🧑‍💻

1. **Clone the repository:**
   ```bash
   git clone https://github.com/morikeli/fastapi-sqlmodel.git
   cd fastapi-sqlmodel
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   uvicorn app:app --reload
   ```

4. **Explore the API docs:**
   To access API documentation, visit the following endpoints:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for a Swagger UI experience! ✨
   - [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for a Redoc UI experience! ✨
---

## 3. Developer Instruction

If you're interested in building on top of this or just exploring, here’s how things are set up:

- **Project Structure:**
  ```
  📦project-root
  │
  ├── 📄 app
  |   ├── 📄 core
  |   │   └── 📄 __init__.py
  |   │   └── 📄 config.py       # project configuration - get environment variables
  |   ├── 📄 db
  |   │   └── 📄 __init__.py
  |   │   └── 📄 database.py     # database configuratiion and connection
  |   ├── 📄 models
  |   │   └── 📄 __init__.py
  |   │   └── 📄 models.py       # book model 
  |   ├── 📄 routes
  |   │   └── 📄 __init__.py
  |   │   └── 📄 routes.py       # routes
  |   ├── 📄 schemas
  |   │   └── 📄 __init__.py
  |   │   └── 📄 book_schemas.py
  |   ├── 📄 services
  |   │   └── 📄 __init__.py
  |   │   └── 📄 book_service.py
  |   ├── 📄 __init__.py        # App entry point
  |
  ├── 📄 .gitignore
  ├── 📄 db.sqlite3             # Develpoment database
  ├── 📄 LICENSE                # MIT license
  ├── 📄 README.md
  ├── 📄 requirements.txt
  ```

- **Environment Variables:**
  Create a `.env` file for settings like the database URL if you plan to expand!

  To use sqlite provided, create a `.env` file and add this environment variable.

  ```env
  DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
  ```
---

## 4. Contribution

Contributions are warmly welcome! 🌟

- Fork the repository
- Create a new branch (`git checkout -b you-branch-name`)
- Commit your changes (`git commit -m 'feature: Added a cool feature'`)
- Push to the branch (`git push origin your-branch-name`)
- Open a Pull Request

Please ensure your code is clean and follows FastAPI's and Pydantic’s best practices.  
Let’s learn and build together! 🤝

---

## 5. License

📝 Licensed under the **MIT License**.  
Feel free to use, modify, and distribute!

---

> _Made with ❤️ while learning FastAPI + SQLModel._

---
