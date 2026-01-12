"""
FastAPI Todo Application - Clean Architecture
Based on: TodoApp/main.py
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Database initialization
from src.data.config.database import engine, Base

# API Routers
from src.transportation.api.routers import (
    auth_router,
    todos_router,
    admin_router,
    users_router
)

# Web Routers
from src.transportation.web.routers import (
    home_router,
    web_auth_router,
    web_todos_router
)

# Middleware
from src.transportation.web.middleware import MethodOverrideMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="src/transportation/web/static"), name="static")

# Middleware override
app.add_middleware(MethodOverrideMiddleware)

# Include Web routers 
app.include_router(home_router)
app.include_router(web_auth_router)
app.include_router(web_todos_router)

# Include API routers
app.include_router(auth_router)  
app.include_router(todos_router)  
app.include_router(admin_router)  
app.include_router(users_router)

