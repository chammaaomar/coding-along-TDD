from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    error = None
    if request.method == 'POST':
        new_item = Item(text=request.POST['item_text'], list=list_)
        try:
            new_item.full_clean()
            new_item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            error = 'You cannot enter an empty item'
    return render(request, 'list.html', context={
        'list': list_,
        'items': items,
        'error': error
    })


def new_list(request):
    if request.method == 'POST':
        list_ = List.objects.create()
        new_item_text = request.POST['item_text']
        new_item = Item(text=new_item_text, list=list_)
        try:
            new_item.full_clean()
            new_item.save()
        except ValidationError:
            list_.delete()
            return render(request, 'home.html', context={
                'error': 'You cannot enter an empty item'
            })
    return redirect(f'/lists/{list_.id}/')
