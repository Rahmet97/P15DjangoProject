from django.forms import CharField, PasswordInput, TextInput, Form


class LoginForm(Form):
    username = CharField(label='Username', widget=TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'placeholder': 'Username'
    }))
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'placeholder': 'Enter your password'
    }))
