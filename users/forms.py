from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from users.models import User, Order


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('email', 'password')


class ProfileUserForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия',widget=forms.TextInput(attrs={'class': 'form-input'}))
    date_of_birth = forms.DateTimeField(label='Дата рождения', widget=forms.DateTimeInput(attrs={'class': 'form-input'}), required=False)
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'readonly': True}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'username', 'email')


class OrderForm(forms.ModelForm):
    user = forms.CharField(label='Логин заказчика', widget=forms.TextInput(attrs={'class': 'form-input', 'readonly': True}))
    total_sum = forms.IntegerField(label='Сумма заказа', widget=forms.NumberInput(attrs={'class': 'form-input', 'readonly': True}))

    class Meta:
        model = Order
        fields = ('user', 'way', 'total_sum')

