from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from .models import User


class LoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class'] = 'uk-input form-control'
    self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
    self.fields['password'].widget.attrs['class'] = 'uk-input form-control'
    self.fields['password'].widget.attrs['placeholder'] = 'パスワード'


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget = forms.PasswordInput(attrs={
                                    'class': 'uk-input',
                                    'placeholder': 'パスワード',
                                })
                                )
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'uk-input',
                                    'placeholder': 'パスワード再入力',
                                })
                                )
    class Meta:
        model = User
        fields = ('username', 'nickname', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'ユーザー名（ログインに使用）',
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'uk-input',
                'placeholder': '表示名',
            }),
            'email': forms.TextInput(attrs={
                'class': 'uk-input',
                'placeholder': 'メールアドレス',
            }),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
