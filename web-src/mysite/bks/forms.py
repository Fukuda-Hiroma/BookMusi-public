from django import forms
from .models import *

class InquiryForm(forms.ModelForm):
    class Meta():
        model = Inquiry
        fields = ('title', 'body', 'tags')
        labels = {'title': "タイトル",
                  'body': "本文",
                  'tags': "タグ"
                  }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'uk-input uk-form-large',
                'placeholder': '（例）〇〇な本を教えて！',
                }),
            'body': forms.Textarea(attrs={
                'class': 'uk-textarea',
                'placeholder': '（例）◇◇や△△が好きなので、〇〇なホニャララを教えてください',
                }),
            'tags': forms.Select(attrs={
                'class': 'uk-select uk-form-large'
                }, 
                choices= (
                    ('文学', '#文学'),
                    ('歴史・地理', '#歴史・地理'),
                    ('ミステリー・推理', '#ミステリー・推理'),
                    ('ホラー', '#ホラー'),
                    ('ファッション', '#ファッション'),
                    ('車・バイク', '#車・バイク'),
                    ('格闘', '#格闘'),
                    ('海外作品', '#海外作品'),
                    ('ゲーム', '#ゲーム'),
                    ('お笑い', '#お笑い'),
                    ('幻想小説', '#幻想小説'),
                    ('評論', '#評論'),
                    ('ノンフィクション・ドキュメンタリー', '#ノンフィクション・ドキュメンタリー'),
                    ('思想', '#思想'),
                    ('デザイン', '#デザイン'),
                    ('政治', '#政治'),
                    ('旅行', '#旅行'),
                    ('趣味', '#趣味'),
                    ('ビジネス', '#ビジネス'),
                    ('絵本・図鑑', '#絵本・図鑑'),
                    ('ライトノベル', '#ライトノベル'),
                    ('恋愛小説', '#恋愛小説'),
                    ('健康・美容', '#健康・美容'),
                    ('子育て・料理', '#子育て・料理'),
                    ('受験', '#受験'),
                    ('資格・検定', '#資格・検定'),
                    ('IT・コンピュータ', '#IT・コンピュータ'),
                    ('写真集', '#写真集'),
                    ('音楽', '#音楽'),
                    ('サバイバル', '#サバイバル'),
                    ('アニメ・漫画', '#アニメ・漫画'),
                    ('少年漫画', '#少年漫画'),
                ))
            }


class ReplyForm(forms.ModelForm):
    class Meta():
        model = Reply
        fields = ('title', 'body', 'bookisbn')
        labels = {'title': "タイトル",
                  'body': "本文",
                  'bookisbn': "ISBNコード"
                  }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'uk-input focus',
                'placeholder': 'タイトル',
            }),
            'body': forms.Textarea(attrs={
                'class': 'uk-textarea focus',
                'placeholder': '本文',
            }),
            'bookisbn': forms.HiddenInput()
        }
            


class ImpressForm(forms.ModelForm):
    class Meta():
        model = Impress
        fields = ('checkuuid', 'body')
        labels = {
            'checkuuid': "checkuuid",
            'body': "本文",
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'uk-textarea',
                'placeholder': 'この本の感想を教えてね',
            }),
            'checkuuid': forms.HiddenInput()
        }
