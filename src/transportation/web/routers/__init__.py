"""
Web Routers - HTML page rendering
"""

from .home import router as home_router
from .auth import router as web_auth_router
from .todos import router as web_todos_router

__all__ = ['home_router', 'web_auth_router', 'web_todos_router']