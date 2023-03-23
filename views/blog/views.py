from datetime import datetime
from math import ceil
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from core.models import Post
from core.schemas import ContactForm, PostSchema


def query_params(v, **kwargs: str):
    if kwargs:
        return str(v) + '?' + urlencode(kwargs)
    return v


def links(request: Request):
    return {'request': request, 'twitter': 'https://twitter.com'}


templates = Jinja2Templates(directory='templates', context_processors=[links])
templates.env.globals['now'] = datetime.now
templates.env.globals['utcnow'] = datetime.utcnow
templates.env.globals['datetime'] = datetime
templates.env.filters['query'] = query_params


blog_router = APIRouter()


# @blog_router.get('/', response_class=HTMLResponse, name='blog_index')
# async def index(
#         request: Request,
#         limit: int = Query(default=2, ge=1)
# ):
#     posts = await Post.select(
#         select(Post)
#         .order_by(Post.date_created)
#         .limit(limit)
#     )
#     page_count = ceil(await Post.count() / 2)
#     print(page_count)
#     return templates.TemplateResponse(
#         'blog/index.html',
#         context={
#             'request': request,
#             'posts': posts,
#             'limit': limit + 2
#         }
#     )

@blog_router.get('/', response_class=HTMLResponse, name='blog_index')
async def index(
        request: Request,
        page: int = Query(default=1, ge=1)
):
    posts = await Post.select(
        select(Post)
        .order_by(Post.date_created)
        .limit(2)
        .offset(page * 2 - 2)
    )
    page_count = ceil(await Post.count() / 2)
    return templates.TemplateResponse(
        'blog/index.html',
        context={
            'request': request,
            'posts': posts,
            'page_count': page_count,
            'current_page': page
        }
    )


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


@blog_router.get('/{post_slug}', response_class=HTMLResponse, name='post_detail')
async def post_detail(request: Request, post_slug: str = Path(max_length=150)):
    post = await Post.select(
        select(Post)
        .filter_by(slug=post_slug)
    )
    if post:
        return templates.TemplateResponse('blog/post.html', {'request': request, 'post': post[0]})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
