from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, admin, users

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

#creates the database
models.Base.metadata.create_all(bind=engine)

#import frontend templates
app.mount("/static", StaticFiles(directory="static"), name="static")


#this serves the content of home.html 
'''
this will render the content of the home.html into localhost:8000 
and will redirect the users to the todos page
'''
@app.get("/")
def test(request: Request): 
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


#include routes from routers file
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

