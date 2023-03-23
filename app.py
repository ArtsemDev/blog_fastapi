from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from views.blog import blog_router


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')
app.include_router(router=blog_router)
