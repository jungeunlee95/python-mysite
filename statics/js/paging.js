function setPage(listCount, currentPage, kwd) {
		var kwd = kwd; // 검색어
		var listCount = listCount;  // 전체 게시글 수
		var pageCount = (parseInt( listCount/ 10) + 1); // 페이지 개수
		var currentPage = currentPage; // 현재 페이지
		var endPage = (parseInt(pageCount/10 + 1) * 5)+1; // 최종 페이지
		var displayPage = parseInt((currentPage + 4 ) / 5 ) * 5; // 밑에 보여줄 페이지

		/* 게시글 수가 페이지 수와 딱 맞을 땐 다음 페이지 안보이게*/
		if(parseInt( listCount% 10)==0){
			pageCount -=1;
		};
		console.log("listCount", listCount);
		console.log("pageCount", pageCount);
		console.log("currentPage", currentPage);
		console.log("endPage", endPage);
		console.log("displayPage", displayPage);

        var pager = $('#pager');
        	if(currentPage <= 5){
			pager.prepend('<li>◀</li>');
		}else{
			pager.append('<li><a href=/board/list/'+(displayPage-5)+'?kwd='+kwd+'>'+'◀'+'</li>');
		}

        for (var i = displayPage-4; i <= displayPage; i++) {
			if(i==currentPage){
				pager.append('<li class="selected">'+i+'</li>')
				continue;
			}else if(i>pageCount){
				pager.append('<li>'+i+'</li>')
				continue;
			}
			pager.append('<li><a href=/board/list/'+i+'?kwd='+kwd+'>'+i+'</li>');
		}

        var nextPage = displayPage+1

		if(currentPage < endPage && endPage < pageCount){
			pager.append('<li><a href=/board/list/'+nextPage+ '?kwd='+kwd+'>'+'▶'+'</li>');
		}else{
			pager.append('<li>'+'▶'+'</li>');
	}

}