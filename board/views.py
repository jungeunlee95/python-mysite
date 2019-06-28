import datetime

from django.db.models import F, Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User
import json

PAGESIZE=10
def list(request, page=1):
    kwd = request.GET.get('kwd')
    if kwd is None or kwd is '' or kwd == 'null':
        start = (page - 1) * PAGESIZE
        board_count = Board.objects.count()
        boardlist = Board.objects.all().order_by('-groupno','orderno')[start:start+PAGESIZE]
    else:
        start = (page - 1) * PAGESIZE
        board_count = Board.objects.filter(title__contains=kwd).count()
        boardlist = Board.objects.filter(title__contains=kwd).order_by('-groupno', 'orderno')[start:start + PAGESIZE]

    data = {
        'boardlist': boardlist,
        'board_count': board_count,
        'current_page': page,
        'page':page,
    }

    # 검색어
    kwd = request.GET.get('kwd')
    if kwd is None:
        data['kwd'] = json.dumps(kwd)
    else:
        data['kwd'] = kwd

    return render(request, '_bs/board/list.html', data)

def writeform(request, no=-1, page=1):
    # 인증
    authuser = request.session.get('authUser')
    if authuser is None:
        return HttpResponseRedirect('/board/list')

    if no == -1:
        return render(request, 'board/write.html',{"page":page})
    else:
        data = {"no":no, "page":page}
        # 검색어
        kwd = request.GET.get('kwd')
        if kwd is None:
            data['kwd'] = json.dumps(kwd)
        else:
            data['kwd'] = kwd
        return render(request, 'board/write.html', data)

def write(request, page=1):
    # 인증
    authuser = request.session.get('authUser')
    if authuser is None:
        return HttpResponseRedirect('/board/list')
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.user = User.objects.get(id=request.session['authUser']['id'])

    # 새글 작성
    if request.POST['no'] == '-1':
        value = Board.objects.aggregate(max_groupno=Max('groupno'))
        board.groupno = value["max_groupno"]+1
        board.save()
    # 답글 작성
    else:
        board2 = Board.objects.get(id=request.POST['no'])
        Board.objects.filter(orderno__gte=board2.orderno+1).update(orderno=F('orderno') + 1)
        board.groupno = board2.groupno
        board.orderno = board2.orderno+1
        board.depth = board2.depth+1
        board.save()
    data= {
        'page':1
    }
    # 검색어
    kwd = request.GET.get('kwd')
    print(kwd,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    if kwd is None:
        data['kwd'] = json.dumps(kwd)
    else:
        data['kwd'] = kwd
    return HttpResponseRedirect(f'/board/list/{page}?kwd={kwd}')

def view(request, no=0, page=1):
    # 존재하는 게시글이 없을 경우 return
    if no == 0:
        return HttpResponseRedirect('list')

    board = Board.objects.filter(id=no)

    data = {
        'board':board[0],
        'page':page,
    }

    # 검색어
    kwd = request.GET.get('kwd')
    if kwd is None:
        data['kwd'] = json.dumps(kwd)
    else:
        data['kwd'] = kwd

    response = render(request, 'board/view.html', data)
    # [1] 로그인 확인
    if request.session.get('authUser') is None:
        cookie_name = 'hit'
    else:
        cookie_name = f'hit:{request.session["authUser"]["id"]}'

    # [2] 그 날 당일 밤 12시에 쿠키 삭제
    tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    # [3] hit를 check하는 쿠키가 있는 경우
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(no) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{no}', expires =expires)
            board.update(hit=F('hit') + 1)
            return response
    # [4] hit를 check하는 쿠키가 없는 경우
    else:
        response.set_cookie(cookie_name, no, expires =expires)
        board.update(hit=F('hit') + 1)
        return response

    return render(request, 'board/view.html', data)

def modifyform(request, no=0, page=1):
    # 인증
    board = Board.objects.filter(id=no)[0]
    authuser = request.session.get('authUser')
    if authuser is None or board.user.id != authuser['id'] :
        return HttpResponseRedirect('/board/list')

    data = {
        'board':board,
        'page':page,
    }

    # 검색어
    kwd = request.GET.get('kwd')
    if kwd is None:
        data['kwd'] = json.dumps(kwd)
    else:
        data['kwd'] = kwd

    return render(request, 'board/modify.html', data)

def modify(request, page=1):
    # 인증
    board_id = request.POST['id']
    board = Board.objects.get(id=board_id)
    authuser = request.session.get('authUser')
    if authuser is None or board.user.id != authuser['id'] :
        return HttpResponseRedirect('/board/list')

    board.title = request.POST['title']
    board.content = request.POST['content']
    data = {
        'board':board,
        'page':page,
    }

    # 검색어
    kwd = request.GET.get('kwd')
    if kwd is None:
        data['kwd'] = json.dumps(kwd)
    else:
        data['kwd'] = kwd

    return HttpResponseRedirect('/board/'+board_id+'/'+str(page), data)

def delete(request, no=0, page=1):
    board = Board.objects.get(id=no)
    # 인증
    authuser = request.session.get('authUser')
    if authuser is None or board.user.id != authuser['id'] :
        return HttpResponseRedirect('/board/list')

    board.title = '삭제된 글입니다.'
    return HttpResponseRedirect(f'/board/list/{page}')