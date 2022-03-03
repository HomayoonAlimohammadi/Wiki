from http.client import HTTPResponse
from django.shortcuts import render
from matplotlib.pyplot import get
from django.http import Http404, HttpResponseRedirect
from markdown import Markdown
from django.urls import reverse
from .forms import (
    CreateForm,
)
from .util import (
    list_entries,
    get_entry,
    save_entry,
    edit_entry,
    delete_entry,
)
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry_view(request, title):
    page_content = get_entry(title)
    if page_content is None:
        raise Http404
    else:
        page_content = Markdown().convert(page_content)
    context = {
        'page_content' : page_content,
        'title': title,
    }
    return render(request, 'encyclopedia/entry.html', context = context)


def create_view(request):
    form = CreateForm(request.POST or None)
    error = False
    if request.method == 'POST':
        if form.is_valid():
            title, content = form.cleaned_data['title'], form.cleaned_data['content']
            all_articles = [article.lower() for article in list_entries()]
            if title.lower() in all_articles:
                error = True
            else:
                save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:index"))
    context = {
        'form': form,
        'state': 'CREATE',
        'error': error,
    }
    return render(request, 'encyclopedia/create-edit.html', context=context)


def random_view(request):
    result = choice(list_entries())
    return HttpResponseRedirect(f'../{result}/')

def edit_view(request, title):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            old_title = title
            title, content = form.cleaned_data['title'], form.cleaned_data['content']
            edit_entry(old_title=old_title, title=title, content=content)
            return HttpResponseRedirect(reverse('encyclopedia:index'))

    content = get_entry(title)
    form_context = {
        'title': title,
        'content': content,
    }
    form = CreateForm(form_context)
    context = {
        'form': form,
        'state': 'EDIT',
    }
    return render(request, 'encyclopedia/create-edit.html', context=context)
    
def search_view(request):
    if request.method == 'POST':
        q = request.POST['q'].lower()
    else:
        q = ''
    all_articles = list_entries()
    valid_articles = [article for article in all_articles if q in article.lower()]
    context = {
        'entries': valid_articles,
    }
    return render(request, 'encyclopedia/search.html', context=context)


def delete_view(request, title):
    delete_entry(title)
    return HttpResponseRedirect(reverse('encyclopedia:index'))