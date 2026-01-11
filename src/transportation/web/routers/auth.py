"""
Web Authentication Router - Renders login/register pages
"""

from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated

from src.transportation.api.dependencies.container import (
    get_authenticate_user_use_case,
    get_register_user_use_case
)
from src.domain.use_cases.user.authenticate_user import AuthenticateUserUseCase
from src.domain.use_cases.user.register_user import RegisterUserUseCase
from src.domain.exceptions.domain_exceptions import (
    InvalidCredentialsError,
    InactiveUserError,
    DuplicateEntityError,
    PasswordStrengthError
)


router = APIRouter(tags=['web-auth'])

templates = Jinja2Templates(directory="src/transportation/web/templates")


@router.get("/login")
def get_login_page(request: Request):
    """Render login page"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.get("/register")
def get_register_page(request: Request):
    """Render registration page"""
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@router.post("/login")
async def login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    use_case: Annotated[AuthenticateUserUseCase, Depends(get_authenticate_user_use_case)]
):
    """Process login form and redirect to todos page"""
    try:
        # Authenticate user
        result = use_case.execute(
            username=username,
            password=password,
            token_expires_minutes=60
        )
        
        # Create redirect response
        response = RedirectResponse(url="/todos", status_code=302)
        
        # Set token as HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {result['access_token']}",
            httponly=True,
            max_age=3600,
            expires=3600
        )
        
        return response
    
    except Exception:
        # Any error = show simple message
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid username or password"
            },
            status_code=401
        )


@router.post("/register")
async def register(
    request: Request,
    email: Annotated[str, Form()],
    username: Annotated[str, Form()],
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password2: Annotated[str, Form()],
    phone_number: Annotated[str, Form()],
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)], 
    role: Annotated[str, Form()] = "user"
):
    """Process registration form"""
    try:
        # Validate passwords match
        if password != password2:
            raise ValueError("Passwords do not match")
        
        # Register user
        use_case.execute(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            phone_number=phone_number
        )
        
        # Redirect to login page after successful registration
        return RedirectResponse(url="/login", status_code=302)
    
    except ValueError as e:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(e)
            },
            status_code=400
        )
    except PasswordStrengthError as e:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(e)
            },
            status_code=400
        )
    except DuplicateEntityError as e:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": str(e)
            },
            status_code=400
        )


@router.get("/logout")
def logout():
    """Logout user and redirect to login page"""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response