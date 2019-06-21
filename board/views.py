from django.db.models import F, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def list(request, page=1, pagesize=10):
    start = (page - 1) * pagesize
    board_count = Board.objects.count()
    boardlist = Board.objects.all().order_by('-groupno','orderno')[start:start+pagesize]

    data = {
        'boardlist': boardlist,
        'board_count': board_count,
        'current_page': page
    }

    return render(request, 'board/list.html', data)

def writeform(request, no=-1):
    if no == -1:
        return render(request, 'board/write.html')
    else:
        return render(request, 'board/write.html', {"no":no})

def write(request):
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

    return HttpResponseRedirect('list')

def view(request, no=0):
    if no == 0: return HttpResponseRedirect('list')

    board = Board.objects.filter(id=no)
    board.update(hit=F('hit')+1)
    data = {
        'board':board[0]
    }
    return render(request, 'board/view.html', data)

def modifyform(request, no=0):
    board = Board.objects.filter(id=no)[0]
    data = {
        'board':board
    }
    return render(request, 'board/modify.html', data)

def modify(request):
    board_id = request.POST['id']
    board = Board.objects.get(id=board_id)
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.save()
    data = {
        'board':board
    }
    return HttpResponseRedirect(board_id, data)

def delete(request, no=0):
    board = Board.objects.get(id=no)
    board.title = '삭제된 글입니다.'
    board.save()
    return HttpResponseRedirect('/board/list')