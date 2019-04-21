from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',required=True,widget=forms.TextInput(attrs=\
    {'class':'form-control','placeholder':'请输入用户名'}))##required表示必须填写
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={\
        'class':'form-control','placeholder':'请输入密码'}))##placeholder不输入的时候提示
    #如果使用原始版的form类不需要重新定义clean函数

    #重新定义clean函数
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']##cleaned_data表示有一个干净的数据
        user=auth.authenticate(username=username,password=password)##這個函數不一定需要request
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user']=user
        return self.cleaned_data
class RegForm(forms.Form):
    username=forms.CharField(label='用户名',
        max_length=30,min_length=2,required=True,widget=forms.TextInput(attrs=\
    {'class':'form-control','placeholder':'请输入3-30位用户名'}))
    password=forms.CharField(label='密码',
        min_length=6,required=True,widget=forms.PasswordInput(attrs=\
    {'class':'form-control','placeholder':'请输入至少6位密码'}))
    password_again=forms.CharField(label='密码',
        min_length=6,required=True,widget=forms.PasswordInput(attrs=\
    {'class':'form-control','placeholder':'再输入一次密码'}))
    email=forms.CharField(label='邮箱',required=True,widget=forms.EmailInput(attrs=\
    {'class':'form-control','placeholder':'请输入邮箱'}))

    ##针对字段进行验证
    ###注意字段field，注意输入框是包含'input'的方法
    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已经存在')
        return username
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱存在')
        return email
    def clean_password_again(self):
        password=self.cleaned_data['password']
        password_again=self.cleaned_data['password_again']
        if password !=password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

