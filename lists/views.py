from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', context={
        'items': items,
    })


def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/unique-list/')
