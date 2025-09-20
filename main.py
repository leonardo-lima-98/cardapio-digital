## 12. Main Application (app/main.py)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import engine, Base
from src.routes.admin import auth, restaurants, categories, items
from src.routes import menu

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin routes (protected)
app.include_router(auth.router, prefix="/admin/auth", tags=["admin-auth"])
app.include_router(restaurants.router, prefix="/admin/restaurants", tags=["admin-restaurants"])
app.include_router(categories.router, prefix="/admin", tags=["admin-categories"])
app.include_router(items.router, prefix="/admin", tags=["admin-items"])

# Public routes
app.include_router(menu.router, prefix="/menu", tags=["menu"])

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
