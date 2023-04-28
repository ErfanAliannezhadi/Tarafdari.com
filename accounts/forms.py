from django import forms
from .models import UserModel


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(),
                                error_messages={'required': 'رمز عبور الزامی است'})
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(),
                                error_messages={'required': 'رمز عبور الزامی است'})

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'phone_number', 'email')
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'phone_number': 'موبایل',
            'email': 'ایمیل',
        }
        error_messages = {
            'first_name': {'required': 'نام الزامی است'},
            'last_name': {'required': 'نام خانوادگی الزامی است'},
            'phone_number': {'required': 'شماره تلفن الزامی است'},
            'email': {'required': 'ایمیل الزامی است'}
        }

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p2 and (p1 != p2):
            raise forms.ValidationError('رمز عبور نادرست میباشد')
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
