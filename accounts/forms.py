from django import forms
from .models import User


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput())
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'email')
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'موبایل',
            'email': 'ایمیل',
        }

    def clean(self):
        cd = super().clean()
        if cd['password1'] and cd['password2'] and (cd['password1'] != cd['password2']):
            raise forms.ValidationError('رمز عبور نادرست میباشد')
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
