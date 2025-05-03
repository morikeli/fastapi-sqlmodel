from app.models.user import User
from app.models.books import Book


# Resolve forward references
User.model_rebuild()
Book.model_rebuild()
