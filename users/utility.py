import jwt
from django.conf import settings
import random

from users.models import Users

class EncodeDecodeToken:
    
    """
    Method to check user is logined and verified himself
    """
    @staticmethod
    def encode_token(serializers):

        encoded_token = jwt.encode(
                    { "user_id":serializers.data.get("id"), "username":serializers.data.get("username") },
                    settings.ENCODING_TYPE,
                    algorithm="HS256"
                )
        return encoded_token

    @staticmethod
    def decode_token(token):

        decoded_token = jwt.decode(
            token,
            settings.ENCODING_TYPE,
            algorithms="HS256"
        )
        return decoded_token

def generate_otp(user_data):
    otp  = random.randint(100000,1000000)
    user = Users.objects.get(username = user_data.get("username"))
    user.otp = otp
    user.save()
    return otp