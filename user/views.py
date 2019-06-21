from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def join(request):
    user = User()
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']
    user.save()

    return HttpResponseRedirect('joinsuccess')

def checkemail(request):
    try:
        user = User.objects.get(email=request.GET['email'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : "not exist" if user is None else "exist"
    }
    return JsonResponse(result)


# login
def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    results =  User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])

    # 로그인 실패
    if len(results)==0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 처리
    authUser = results[0]
    request.session['authUser'] = model_to_dict(authUser)

    return HttpResponseRedirect('/')

def logout(request):
    del request.session['authUser']
    return HttpResponseRedirect('/')

# 회원정보 수정
def updateform(request):
    user = User.objects.get(id=request.session['authUser']['id'])
    data = {
        'user':user
    }
    return render(request, 'user/updateform.html', data)

def update(request):
    user = User.objects.get(id=request.session['authUser']['id'])
    user.name = request.POST['name']
    user.gender = request.POST['gender']

    if request.POST['password'] is not '':
        user.password = request.POST['password']
    user.save()
    
    # 수정정보 다시 가져오기
    # request.session['authUser'] = model_to_dict(user)
    request.session['authUser']['name']=user.name
    return HttpResponseRedirect('/user/updateform?result=success')