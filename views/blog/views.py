from datetime import datetime

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from core.schemas import ContactForm


templates = Jinja2Templates(directory='templates')
templates.env.globals['now'] = datetime.now
templates.env.globals['utcnow'] = datetime.utcnow
templates.env.globals['datetime'] = datetime


blog_router = APIRouter()


@blog_router.get('/', response_class=HTMLResponse, name='blog_index')
async def index(request: Request):
    return templates.TemplateResponse('blog/index.html', context={'request': request})


@blog_router.get('/about', response_class=HTMLResponse, name='blog_about')
async def about(request: Request):
    return templates.TemplateResponse('blog/about.html', context={'request': request})


@blog_router.get('/contact', response_class=HTMLResponse, name='blog_contact')
async def contact(request: Request):
    return templates.TemplateResponse('blog/contact.html', context={'request': request})


@blog_router.post('/contact', response_class=HTMLResponse, name='blog_contact')
async def contact(
        request: Request,
        contact_form: ContactForm | str = Depends(ContactForm.as_form)
):
    if isinstance(contact_form, ContactForm):
        print(contact_form)
        error = None
        submit = True
    else:
        error = contact_form
        submit = False
    return templates.TemplateResponse(
        'blog/contact.html',
        context={
            'request': request,
            'error': error,
            'submit': submit
        }
    )
