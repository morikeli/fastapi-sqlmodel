# 🚀 FastAPI + SQLModel Starter

![Screenshot from 2025-04-26 13-36-07](https://github.com/user-attachments/assets/c429fcc1-ef70-4aa9-a143-0571c3bcea66)


## 1. Overview

Welcome! 👋  
This project is a simple backend built with **FastAPI** and **SQLModel**.  
The primary goal was to **learn and demonstrate** how to integrate SQLModel (an ORM and Pydantic hybrid) with FastAPI to create clean, efficient APIs.  

🔹 **FastAPI** — Modern, fast (high-performance) web framework.  
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
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for a Swagger UI experience! ✨

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
- Create a new branch (`git checkout -b feature/your-feature`)
- Commit your changes (`git commit -m 'Add some feature'`)
- Push to the branch (`git push origin feature/your-feature`)
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
