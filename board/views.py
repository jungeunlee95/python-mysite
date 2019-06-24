import datetime

from django.db.models import F, Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User

PAGESIZE=10
def list(request, page=1):
    start = (page - 1) * PAGESIZE
    board_count = Board.objects.count()
    boardlist = Board.objects.all().order_by('-groupno','orderno')[start:start+PAGESIZE]

    data = {
        'boardlist': boardlist,
        'board_count': board_count,
        'current_page': page,
        'page':page,
    }

    return render(request, 'board/list.html', data)

def writeform(request, no=-1, page=1):
    if no == -1:
        return render(request, 'board/write.html',{"page":page})
    else:
        return render(request, 'board/write.html', {"no":no, "page":page})

def write(request, page=1):
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
    return HttpResponseRedirect(f'/board/list/{page}')

def view(request, no=0, page=1):
    # 존재하는 게시글이 없을 경우 return
    if no == 0:
        return HttpResponseRedirect('list')

    board = Board.objects.filter(id=no)

    data = {
        'board':board[0],
        'page':page,
    }

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
    board = Board.objects.filter(id=no)[0]
    data = {
        'board':board,
        'page':page,
    }
    return render(request, 'board/modify.html', data)

def modify(request, page=1):
    board_id = request.POST['id']
    board = Board.objects.get(id=board_id)
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.save()
    data = {
        'board':board,
        'page':page,
    }
    return HttpResponseRedirect(board_id, data)

def delete(request, no=0, page=1):
    board = Board.objects.get(id=no)
    board.title = '삭제된 글입니다.'
    board.save()
    return HttpResponseRedirect(f'/board/list/{page}')