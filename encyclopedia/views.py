from django.shortcuts import render
import random
from . import util
from markdown2 import markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class updateWiki(forms.Form):
    textArea = forms.CharField(widget=forms.Textarea, label="")
    
class titleWiki(forms.Form): 
    title = forms.CharField(label="TITLE ")

def index(request):
    titleSearched = request.GET.get('q')
    subStringResults = []

    if titleSearched and titleExistsFor(titleSearched):
        return HttpResponseRedirect(titleSearched)
    elif titleSearched:
        subStringResults = listOfSubString(titleSearched)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "subStringResult": subStringResults
    })

def title(request, titleName):
    if request.method == "POST":
        form = updateWiki(request.POST)
        if form.is_valid():
            updatedMarkdownContent = form.cleaned_data["textArea"]
            util.save_entry(titleName, updatedMarkdownContent)

    wikiTitle = util.get_entry(titleName)
    
    if wikiTitle is None :
        return render(request, "encyclopedia/error.html", {
            "errorMsg": "Error: Your Requested WIKI title page cannot be found"
        })
    else:
        article = markdown(wikiTitle)
        return render(request, "encyclopedia/entry.html", {
            "title": titleName,
            "body": article
        })

def randomPage(request):
    listOfEntry = util.list_entries()
    numberOfEntry = len(listOfEntry)
    n = random.randint(0,numberOfEntry) -1
    return title(request, listOfEntry[n])

def editPage(request):
    message = request.GET.get('title')
    wikiTitle = util.get_entry(message)
    return render(request, "encyclopedia/edit.html", {
        "textToBeEdited": updateWiki(initial={"textArea": wikiTitle}).textArea,
        "title": message
    })

def newPage(request):
    if request.method == "POST":
        formTitle = titleWiki(request.POST)
        formBody = updateWiki(request.POST)
        if formTitle.is_valid() and formBody.is_valid():
            createdTitle = formTitle.cleaned_data["title"]
            createdMarkup = formBody.cleaned_data["textArea"]
            if not titleExistsFor(createdTitle):
                util.save_entry(createdTitle, createdMarkup)
                return HttpResponseRedirect(createdTitle)
            else:
                return render(request, "encyclopedia/error.html", {
                    "errorMsg": "Error: This Page already exist"
                })
    
    return render(request, "encyclopedia/new.html", {
        "title": titleWiki(),
        "textArea": updateWiki()
    })

def titleExistsFor(currTitle):
        titleList = util.list_entries()
        for title in titleList:
            if(title.upper() == currTitle.upper()):
                return True
        
        return False


def listOfSubString(subString):
        titleList = util.list_entries()
        listOfSubString = []

        for title in titleList:
            if(subString.upper() in title.upper()):
                listOfSubString.append(title)
        
        return listOfSubString