from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', context={
        'items': items,
        'list': list_
    })


def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        new_item_text = request.POST['item_text']
        new_item = Item(text=new_item_text, list=list_)
        try:
            new_item.full_clean()
            new_item.save()
        except:
            list_.delete()
            return render(request, 'home.html', context={
                'error': 'You cannot enter an empty item'
            })
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    if request.method == 'POST':
        list_ = List.objects.get(id=list_id)
        Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_id}/')
