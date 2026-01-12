"""
Web Home Router - Redirects to login page
"""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(tags=['web-home'])


@router.get("/")
def get_home_page():
    """Redirect to login page"""
    return RedirectResponse(url="/login", status_code=302)