from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    guestbooklist = Guestbook.objects.all().order_by('-reg_date')
    data = {'guestbooklist': guestbooklist}
    return render(request, 'guestbook/list.html', data)

def write(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']
    guestbook.save()

    return HttpResponseRedirect('list')

def delete(request, id):
    if request.method == 'GET':
        return render(request, 'guestbook/deleteform.html', {'id': id})
    elif request.method == 'POST':
        id = request.POST['no']
        password = request.POST['password']

        guestbook = Guestbook.objects.filter(id=id)
        if guestbook[0].password == password:
            guestbook.delete()

        return HttpResponseRedirect('/guestbook/list')