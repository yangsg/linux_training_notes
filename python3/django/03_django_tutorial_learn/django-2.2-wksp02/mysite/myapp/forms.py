from django import forms


class UserCreateForm(forms.Form):
    name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)


class UserUpdateForm(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
