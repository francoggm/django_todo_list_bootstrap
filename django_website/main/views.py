from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.

def home(response):
    return render(response, "main/home.html", {})

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == 'POST':
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get(f"c{item.id}") == "clicked":
                    item.complete=True
                else:
                    item.complete=False
                item.save()
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid input")
    return render(response, "main/list.html", {"ls": ls})

def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            t = ToDoList(name=name)
            t.save()
            return HttpResponseRedirect(f"/{t.id}")
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})


