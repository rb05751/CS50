from django.shortcuts import render
from django import forms
from django.template.loader import render_to_string

from . import util
import markdown2 as MD
import numpy as np

class CreatePageForm(forms.Form):
    title = forms.CharField(label = "title")
    content = forms.CharField(widget = forms.Textarea)

class EditPageForm(forms.Form):
    title = forms.CharField(label = "title")
    content = forms.CharField(widget = forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request, entry):
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "info": MD.markdown(util.get_entry(entry)),
            "entry": entry
        })


def search_results(request):
    q = request.GET.get('q').strip()
    if q in list(util.list_entries()):
        return render(request, "encyclopedia/search.html", {
            "info": MD.markdown(util.get_entry(q)),
            "entry": q
        })
    else:
        matching_entries = []
        for entry in list(util.list_entries()):
            if q[0].lower() == entry[0].lower():
                matching_entries.append(entry)
            else:
                continue
        if len(matching_entries) > 0:
            return render(request,
                          "encyclopedia/index.html",
                          {"entries": matching_entries})
        else:
            return render(request, "search_error.html")

def create(request):
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["title"]
            info = form.cleaned_data["content"]
            content = render_to_string("encyclopedia/entry.html", {
                "entry": entry,
                "info": MD.markdown(info)
            })

            ##Check if it already exists
            if util.get_entry(entry) != None:
                return render(request, "encyclopedia/create_error.html")

            
            ###Save entry
            util.save_entry(title = entry, content = info)
            return render(request, "encyclopedia/entry.html", {
                "entry": entry,
                "info": info
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "form" : CreatePageForm()})
    else:
        return render(request, "encyclopedia/create.html", {"form" : CreatePageForm()})

def build_page(request):
    title = request.GET.get('title').strip()
    content = request.GET.get('MD_content').strip()
    return render(request, "encyclopedia/entry.html", {
        "entry": title,
        "info" :content
    })

def edit(request, entry):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["title"]
            info = form.cleaned_data["content"]
            content = render_to_string("encyclopedia/entry.html", {
                "entry": entry,
                "info": MD.markdown(info)
            })
                        ###Save entry
            util.save_entry(title = entry, content = info)
            return render(request, "encyclopedia/entry.html", {
                "entry": entry,
                "info": MD.markdown(info)
            })
    else:
        content = {'title':entry, 'content': util.get_entry(entry)}
        form = EditPageForm(initial = content)
        return render(request, "encyclopedia/edit.html", {"form" : form , "entry": entry})

def random(request):
    entries = list(util.list_entries())
    idx = np.random.randint(len(entries))
    return get_entry(request, entry = entries[idx])
