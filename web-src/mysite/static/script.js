// DjangoでAjaxするためのおまじない
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Ajaxでサーバーにページを更新せずに送信をして、location.replaceで履歴を操作せずにページ遷移。
// 戻るボタンを押したときの違和感を減らし、ユーザビリティを向上。
$(function () {
    $('#inquiry-form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.prop("action"),
            method: form.prop("method"),
            data: form.serialize(),
            timeout: 10000,
            dataType: "text",
        }).done(function (data) {
            location.replace('/inquiry/' + data);
            })
    });
});

$(function () {
    $('#reply-form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.prop("action"),
            method: form.prop("method"),
            data: form.serialize(),
            timeout: 10000,
            dataType: "text",
        }).done(function (data) {
            if (data == "SUCCESS") {
                location.reload(true);
            }
        })
    });
});

$(function () {
    $('#impress-form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.prop("action"),
            method: form.prop("method"),
            data: form.serialize(),
            timeout: 10000,
            dataType: "text",
        }).done(function (data) {
            if (data == "SUCCESS") {
                UIkit.modal("#impress-new").hide();
                UIkit.notification("感想を送信しました");
            }
        })
    });
});

$(function () {
    $('.new-comment').click(function () {
        $("html,body").animate({scrollTop: 0}, 400);
        UIkit.tab("#comment-tab").show(1);
    });
});

$(function () {
    $('.comment').click(function () {
        UIkit.tab("#comment-tab").show(0);
    });
});


// 楽天を検索してISBNをフォームにセットする
function isbnset(isbn, largeImageUrl, publisherName, title, author, salesDate, itemPrice) {
    $("#id_bookisbn").val(isbn);
    $('#nw-largeImageUrl').attr('src', largeImageUrl);
    $("#nw-publisherName").text(publisherName);
    $("#nw-title").text(title);
    $("#nw-author").text(author);
    $("#nw-salesDate").text(salesDate);
    $("#nw-itemPrice").text(itemPrice + "円(税込)");
    $("#nw-isbn").text('ISBN ' + isbn);
    UIkit.modal("#rakuten-search").hide();
    UIkit.notification("選択した書籍を貼り付けました");
};


// 気になるリスト登録
$(function () {
    $('.check').click(function () {
        var csrf_token = getCookie("csrftoken");
        var book = $(this).val();
        var inquiryuuid = $('#inquiryuuid').val();
        $.ajax({
            url: '/api/check',
            method: 'post',
            data: {
                book: book,
                inquiryuuid: inquiryuuid
            },
            timeout: 10000,
            dataType: "text",
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }}
        }).done(function (data) {
            if (data == "SUCCESS:INSERTED") {
                $('#id-' + book).html('<small>チェック済み</small><br><span class="uk-icon uk-icon-image icon-checked"></span>');
                UIkit.notification("チェックしました");
            };
            if (data == "SUCCESS:DELETED") {
                $('#id-' + book).html('<small>チェック</small><br><span class="uk-icon uk-icon-image icon-check"></span>');
            };
        })
    });
});

// 感想リスト表示
$(function () {
    $('.impress-open').click(function () {
        $('#impress-title').text("感想");
        $('#impress-results').html("<div uk-spinner></div>");
        UIkit.modal("#impress-list").show();
        var book = $(this).val();
        var inquiryuuid = $('#inquiryuuid').val();
        title = $('#ti-' + book).text();
        $.ajax({
            url: '/api/impress',
            method: 'post',
            data: {
                book: book,
                inquiryuuid: inquiryuuid
            },
            timeout: 10000,
            dataType: "text"
        }).done(function (data) {
            $('#impress-title').text(title + ' の感想');
            $('#impress-results').html(data);
        })
    });
});


// 参考になる
$(function () {
    $('.like').click(function () {
        var csrf_token = getCookie("csrftoken");
        var replyuuid = $(this).val();
        $.ajax({
            url: '/api/like',
            method: 'post',
            data: {
                replyuuid: replyuuid
            },
            timeout: 10000,
            dataType: "text",
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
            }
        }).done(function (data) {
            if (data == "SUCCESS:INSERTED") {
                $('#goods-' + replyuuid).text(Number($('#goods-' + replyuuid).text() + 1));
                $('#id-' + replyuuid).html('<span class="icon-liked uk-icon uk-icon-image"></span>');
            };
            if (data == "SUCCESS:DELETED") {
                $('#goods-' + replyuuid).text(Number($('#goods-' + replyuuid).text() - 1));
                $('#id-' + replyuuid).html('<span class="icon-like uk-icon uk-icon-image"></span>');
            };
        })
    });
});


// 一定の画面サイズ以下であれば、フォーム入力中のフッターの表示を非表示にする
$(function () {
    $('.focus').on("focusin", function (e) {
        if (window.matchMedia('(max-width: 768px)').matches) {
            $('#fotter').addClass("uk-hidden");
        };
    }).on("focusout", function (e) {
        $('#fotter').removeClass("uk-hidden");
    });
});


// 楽天を検索してISBNをフォームにセットする
$(function () {
    $('.impress-set').on('click', function () {
        var book = $(this).val().split(',');
        console.log(book)
        $("#id_checkuuid").val(book[0]);
        $('#nw-largeImageUrl').attr('src', book[1]);
        $("#nw-publisherName").text(book[2]);
        $("#nw-title").text(book[3]);
        $("#nw-author").text(book[4]);
        $("#nw-salesDate").text(book[5]);
        $("#nw-isbn").text('ISBN ' + book[6]);
        $("#id_body").val("");
        UIkit.modal("#impress-new").show();
    });
});


// 楽天検索
$(function () {
    $('#search_button').on('click', function () {
        let keyword = $('#search_area').val();
        $('#results').html('<div uk-spinner></div>');
        $.ajax({
            type: 'get',
            url: '/api/rakuten_keyword',
            data: {
                keyword: keyword,
            },
        }).done(function (data) {
            $('#results').html(data);
        });
    });
    $("#search_area").keypress(function (e) {
        if (e.which == 13) {
            $("#search_button").click();
        }
    });
});


// 検索
$(function () {
    $('#search_inq').on('click', function () {
        let keyword = $('#search_inq_area').val();
        if (keyword.slice(0, 1) == "#") {
            keyword = 'tags='+keyword.slice(1)
        };
        location.href = '/search/' + keyword;
    });
    $("#search_inq_area").keypress(function (e) {
        if (e.which == 13) {
            $("#search_inq").click();
        }
    });
});