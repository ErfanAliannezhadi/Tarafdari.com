from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, SetPasswordForm, PasswordChangeForm
from django.contrib.auth import password_validation
from .models import UserModel, OTPCodeModel, BlockModel
from random import randint


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': 'ایمیل / موبایل'}),
                             label='نام کاربری', error_messages={'required': 'نام کاربری اجباری است'})
    password = forms.CharField(label='رمز عبور', strip=False,
                               widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
                               error_messages={'required': 'رمز عبور اجباری است'})
    error_messages = {
        'invalid_login': 'رمز عبور یا ایمیل نامعتبر است',
        'inactive': 'این حساب غیرفعال شده است'
    }


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
        user.email = UserModel.objects.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password2'])
        user.is_phone_verified = False
        otp_code = OTPCodeModel.objects.create(phone_number=user.phone_number, code=randint(100000, 999999))
        otp_code.send_otp_code()
        if commit:
            user.save()
        return user


class UserPasswordConfirmForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": 'دو رمز عبور تطابق ندارند',
    }
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='تایید رمز عبور جدید',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class UserChangePasswordForm(UserPasswordConfirmForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": 'رمز عبور قدیمی شما نامعتبر است'}
    old_password = forms.CharField(
        label="رمز عبور فعلی", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": True}), )


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'profile_image', 'cover_image', 'background_image', 'is_private',
                  'about_me', 'email']
        widgets = {
            'profile_image': forms.FileInput(),
        }


class UserPhoneVerifyForm(forms.Form):
    otp_code = forms.CharField(label='کد ارسالی', max_length=6)


class UserBlockReportForm(forms.ModelForm):
    class Meta:
        model = BlockModel
        fields = ['reason']
        widgets = {
            'reason': forms.RadioSelect()
        }

