// ==UserScript==
// @name         CodeCasts一键下载
// @namespace    https://www.mokeyjay.com
// @version      0.1
// @description  在codecasts.com的课程列表页添加一键下载按钮
// @author       i@mokeyjay.com
// @match        https://www.codecasts.com/series/*
// ==/UserScript=

$('tbody tr').map(function(i, e) {
    // 添加 加载中 图标
    $('<td><a class="fa fa-spinner fa-spin fa-3x fa-fw" style="text-decoration: none;" id="downloadLinkLoadStatus_'+i+'"></a></td>').appendTo($(e));
    // 获取下载链接
    let detail_page_url = $(e).find('a').attr('href');
    $.get(detail_page_url, (html) => {
        // let download_url = html.match(/\/download\/video\/[a-z0-9]*/);
        let matches = html.match(/https:\/\/cdn\.codecasts\.com\/.+?\.mp4\?_upt=(\w)+/);
        let download_url = matches[0];
        console.log(download_url);
        if(download_url){
            $('#downloadLinkLoadStatus_'+i).removeClass('fa-spinner fa-spin').addClass('fa-download').attr('href', download_url);
        }
    });
});