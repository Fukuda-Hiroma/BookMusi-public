from django.core.checks import messages
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import FormView
from django.db.models import Max, Q

from pymongo import MongoClient

import requests

from datetime import datetime
import json, collections

from .forms import *
from .models import *

client = MongoClient('mongo', 27017)
db = client.bookmusi

def page_status(title, back=True, footer=True):
    return {'status': {'title': title, 'back': back, 'footer': footer, 'time': datetime.now().isoformat()}}


def notification(useruuid, massege, link):
    collection = db.notifacation
    collection.insert_one({
        "useruuid": str(useruuid),
        "massege": massege,
        "link": link,
        "datetime": datetime.now()
    })
    

class InquiryNewView(LoginRequiredMixin, View):
    form_class = InquiryForm
    success_url = '/'
    template_name = 'bks/new.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = page_status('新しい質問', True, False) | {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            qryset = form.save(commit=False)
            qryset.useruuid = self.request.user
            qryset.save()
            inquiry = Inquiry.objects.filter(useruuid=qryset.useruuid).latest('datetime')
            return HttpResponse(str(inquiry.inquiryuuid))

        return render(request, self.template_name, {'form': form})


class InquiryPageView(View):
    form_class = ReplyForm
    success_url = '/'
    template_name = 'bks/inquiry_page.html'

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        form = self.form_class()
        inquiry = Inquiry.objects.get(inquiryuuid=id)
        reply_list = Reply.objects.filter(inquiryuuid=id).order_by('datetime')
        reply_book = dict(collections.Counter([i["bookisbn"] for i in reply_list.values()]).most_common())

        like_list = Like.objects.filter(replyuuid__in=[a.replyuuid for a in reply_list])
        

        liked_reply = []
        for i in like_list:
            if i.useruuid == request.user:
                liked_reply.append(i.replyuuid.replyuuid)

        book_status = {}
        collection = db.book
        for i in reply_book.keys():
            book_status |= {i: collection.find_one({"Item.isbn": i})}

        checked_book = []
        if request.user.is_authenticated:
            for i in reply_book.keys():
                checked = Checklist.objects.filter(useruuid=request.user, bookisbn=i)
                if checked.exists():
                    # 今後、読了を完了していたらifを追加する
                    checked_book.append(i)

        reply_book |= book_status
        
        context = page_status('質問') | {
            'inquiry': inquiry,
            'reply_list': reply_list,
            'reply_book': reply_book,
            'liked_reply': liked_reply,
            'checked_book': checked_book,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        form = self.form_class(request.POST)
        inquiry = Inquiry.objects.get(inquiryuuid=id)
        if form.is_valid():
            qryset = form.save(commit=False)
            qryset.useruuid = self.request.user
            qryset.inquiryuuid = inquiry
            qryset.save()

            message = f"{ self.request.user.nickname }がコメントを送信しました\n「{request.POST.get('title')}」"
            link = f"/inquiry/{ inquiry.inquiryuuid }"

            notification(str(inquiry.useruuid.useruuid), message, link)

            return HttpResponse('SUCCESS')

        return render(request, self.template_name, {'form': form})


class ImpressNewView(LoginRequiredMixin, View):
    form_class = ImpressForm
    success_url = '/'
    template_name = 'bks/impress.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        check = Checklist.objects.filter(useruuid=request.user)
        
        book_status = {}
        collection = db.book
        for i in check:
            book_status |= {str(i.checkuuid): collection.find_one(
                {"Item.isbn": i.bookisbn}) | {"checkuuid": i.checkuuid}}

        context = page_status('読了する') | {
            'form': form,
            'book_status': book_status
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            qryset = form.save(commit=False)
            qryset.useruuid = self.request.user
            qryset.save()

            n = Checklist.objects.get(checkuuid=request.POST.get("checkuuid"))
            message = f"{ n.useruuid.nickname }が感想を送信しました\n {request.POST.get('body')}"
            link = f"/inquiry/{ n.inquiryuuid.inquiryuuid }"
            n.checkflag = True
            n.save()
            
            for to in Reply.objects.filter(inquiryuuid=n.inquiryuuid, bookisbn=n.bookisbn):
                notification(str(to.useruuid.useruuid), message, link)
            
            return HttpResponse('SUCCESS')

        return render(request, self.template_name, {'form': form})



def index(request):
    inquiry_list = Inquiry.objects.order_by('datetime')[:10]
    context = page_status('ようこそ！', False) | {
        'bks_user': User.username,
        'inquiry_list': inquiry_list,
    }
    return render(request, 'bks/index.html', context)


def inquiry_index(request):
    inquiry_list = Inquiry.objects.order_by('datetime')
    context = page_status('質問一覧') | {
        'inquiry_list': inquiry_list,
    }
    return render(request, 'bks/inquiry_index.html', context)


@login_required
def api(request, api):
    user = request.user

    if api == "check":
        bookisbn = request.POST.get("book")
        inquiryuuid = request.POST.get("inquiryuuid")

        if Inquiry.objects.filter(inquiryuuid=inquiryuuid).exists():
            if Checklist.objects.filter(useruuid=user, bookisbn=bookisbn).exists():
                Checklist.objects.get(
                    useruuid=user,
                    bookisbn=bookisbn
                ).delete()
                return HttpResponse('SUCCESS:DELETED')
            else:
                Checklist(
                    useruuid=user,
                    bookisbn=bookisbn,
                    inquiryuuid=Inquiry.objects.get(inquiryuuid=inquiryuuid)
                ).save()
                return HttpResponse('SUCCESS:INSERTED')
    
    if api == "like":
        replyuuid = request.POST.get("replyuuid")

        if Reply.objects.filter(replyuuid=replyuuid).exists():
            r = Reply.objects.get(replyuuid=replyuuid)
            if Like.objects.filter(replyuuid=replyuuid, useruuid=user).exists():
                Like.objects.get(
                    replyuuid=Reply.objects.get(replyuuid=replyuuid),
                    useruuid=user
                ).delete()
                r.goods = r.goods - 1
                r.save()
                return HttpResponse('SUCCESS:DELETED')
            else:
                Like(
                    replyuuid=Reply.objects.get(replyuuid=replyuuid),
                    useruuid=user
                ).save()
                r.goods = r.goods + 1
                r.save()
                return HttpResponse('SUCCESS:INSERTED')        

    if api == "barcode":
        return HttpResponse('SUCCESS')


    if api == "rakuten_keyword":
        data = {
            "format": "json",
            "keyword": request.GET.get("keyword"),
            "booksGenreId": "001",
            "hits": "30",
            "applicationId": "1033514856812954337",
        }
        r = requests.get('https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404', params=data).json()
        
        collection = db.book
        for i in r["Items"]:
            collection.replace_one({"Item.isbn": i["Item"]["isbn"]}, i, upsert=True)
        
        context = data | r
        return render(request, 'bks/rakuten_keyword.html', context)
    
    if api == "rakuten_isbn":
        keyword = request.GET.get("keyword")
        return HttpResponse('SUCCESS')

    return HttpResponse('FAILURE')


def impress(request):
    bookisbn = request.POST.get("book")
    inquiryuuid = request.POST.get("inquiryuuid")
    impress_book = Checklist.objects.filter(inquiryuuid=inquiryuuid, bookisbn=bookisbn)
    impress_list = []

    for impress in impress_book:
        if impress.checkflag:
            impress_list.append(Impress.objects.get(checkuuid=impress.checkuuid))

    if impress_list == []:
        return HttpResponse("感想がまだ投稿されていません")

    context = page_status('質問一覧') | {
        'impress_list': impress_list,
    }
    return render(request, 'bks/impress_list.html', context)


@login_required
def my_page(request):
    collection = db.notifacation
    my_notifacation = collection.find(
        filter={'useruuid': str(request.user.useruuid)})
    
    my_inquiry = Inquiry.objects.filter(useruuid=request.user).order_by('datetime')

    context = page_status('マイページ') | {
        "notification": my_notifacation,
        "inquiry_list": my_inquiry
    }
    return render(request, 'bks/mypage.html', context)


def search(request, word):
    if word[0:5] == "tags=":
        inquiry_list = Inquiry.objects.filter(tags=word[5:]).order_by('datetime')
        word = "#"+word[5:]
    else:
        inquiry_list = Inquiry.objects.filter(Q(title__contains=word) | Q(body__contains=word) |  Q(tags=word)).order_by('datetime')
    
    
    context = page_status(f'『{word}』の検索結果') | {
        'inquiry_list': inquiry_list,
    }
    return render(request, 'bks/inquiry_index.html', context)


def about(request):
    context = page_status('BooQ（ブーキュー）とは？') | {}
    return render(request, 'bks/about.html', context)