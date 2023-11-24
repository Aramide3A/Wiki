from django.shortcuts import render
from .util import *
from . import util
import markdown2 
from django.http import HttpResponseNotFound
from django import forms
import random

class form(forms.Form):
    title  = forms.CharField( label= 'Title')
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))

def index(request):
    if request.method == 'POST':
        title = request.POST['title']
        entry = get_entry(title)
        if entry == None:
            others= []
            entries = util.list_entries()
            for i in entries:
                if title in i:
                    others.append(i)
            context = {
                'result' : others,
            }
            return render(request, "encyclopedia/search.html", context)
        html = markdown2.markdown(entry)
        context = {
            'html'  : html,
            'title' : title,
        }
        return render(request, "encyclopedia/entry.html", context)
    
    context = {
       "entries": util.list_entries(),
    }
    return render(request, "encyclopedia/index.html", context)

def entry(request, title):
    entry = get_entry(title)
    if entry == None:
        return HttpResponseNotFound
    html = markdown2.markdown(entry)
    context = {
       'html'  : html,
       'title' : title,
    }
    return render(request, "encyclopedia/entry.html", context)

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if title in util.list_entries():
            error_message = "An entry with this title already exists."
            return render(request, 'encyclopedia/new_page.html', { 'error_message': error_message})
        else:
            util.save_entry(title, content)
            entry = get_entry(title)
            html = markdown2.markdown(entry)
            context = {
                'html'  : html,
            }
            return render(request, "encyclopedia/entry.html", context)
    return render(request, "encyclopedia/new_page.html")

def edit(request,  title):
    if request.method == 'POST':
        title = title
        content = request.POST['content']
        util.save_entry(title, content)
        entry = get_entry(title)
        html = markdown2.markdown(entry)
        context = {
            'html'  : html,
        }
        return render(request, "encyclopedia/entry.html", context)
    entry = get_entry(title)
    context = {
        'entry'  : entry,
    }
    return render(request, "encyclopedia/edit.html", context)

def random_page(request):
    i = []
    entries= util.list_entries()
    choice = random.choice(entries)
    entry = get_entry(choice)
    html = markdown2.markdown(entry)
    context = {
       'html'  : html,
    }
    return render(request, "encyclopedia/entry.html", context)