"""
HTTP Method Override Middleware

Allows HTML forms to simulate PUT, PATCH, DELETE methods
by including a hidden _method field in POST requests.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import json


class MethodOverrideMiddleware(BaseHTTPMiddleware):
    """
    Middleware to support HTTP method override via _method form field.
    
    This allows HTML forms (which only support GET/POST) to simulate
    PUT, PATCH, DELETE methods.
    
    Usage in HTML form:
        <form method="POST" action="/resource/1">
            <input type="hidden" name="_method" value="DELETE">
            <button type="submit">Delete</button>
        </form>
    """
    
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            # Check content type
            content_type = request.headers.get("content-type", "")
            
            if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
                try:
                    # Read and cache the body
                    body = await request.body()
                    
                    # Parse form data to check for _method
                    from urllib.parse import parse_qs
                    
                    # Decode body
                    body_str = body.decode('utf-8')
                    
                    # Parse form data
                    form_data = parse_qs(body_str)
                    
                    # Check for _method field
                    if '_method' in form_data:
                        method_override = form_data['_method'][0]
                        
                        if method_override.upper() in ["PUT", "PATCH", "DELETE"]:
                            # Override the request method
                            request.scope["method"] = method_override.upper()
                    
                    # Important: Create a new receive function that returns the cached body
                    async def receive():
                        return {"type": "http.request", "body": body}
                    
                    # Replace the request's receive with our cached version
                    request._receive = receive
                
                except Exception as e:
                    # If anything fails, continue with original request
                    print(f"Method override middleware error: {e}")
                    pass
        
        response = await call_next(request)
        return response