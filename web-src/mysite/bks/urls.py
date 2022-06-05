from django.urls import path
from . import views

app_name = 'bks'

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.InquiryNewView.as_view(), name='new'),
    path('inquiry', views.inquiry_index, name='inquiry_index'),
    path('inquiry/<uuid:id>', views.InquiryPageView.as_view(), name='inquiry_page'),
    path('api/impress', views.impress, name='impress'),
    path('api/<str:api>', views.api, name='api'),
    path('impress', views.ImpressNewView.as_view(), name='impress'),
    path('mypage', views.my_page, name='my_page'),
    path('search/<str:word>', views.search, name='search'),
    path('about', views.about, name='about')
]
