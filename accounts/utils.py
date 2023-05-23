from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('364172347A732F79384D46713577756E49396B384A7958694471715A32496F342F5449446970796C7872773D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'کد تایید شما {code}',
        }
        response = api.sms_send(params=params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
