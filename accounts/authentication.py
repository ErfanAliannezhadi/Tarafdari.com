from .models import UserModel


class PhoneNumberBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = UserModel.objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
