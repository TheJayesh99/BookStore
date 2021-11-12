import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http.response import BadHeaderError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Users
from users.serializers import UserSerializer
from users.utility import EncodeDecodeToken, generate_otp

# Create your views here.

logging.basicConfig(filename="fundooNotes.log",filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Register(APIView):


     def post(self, request):

        try:
            serializers = UserSerializer(data = request.data)
            if serializers.is_valid(raise_exception=True):
                serializers.create(validated_data=serializers.data)
                otp  = generate_otp(serializers.data)
                send_mail(
                    subject="Verification",
                    message=f"hello {serializers.data.get('username')} \n use the below otp to get verified \n {otp}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[serializers.data.get("email")]
                )
                logger.info(f"Registered user")
                return Response({"message":"Registered successfully","data":serializers.data.get("username")},status=status.HTTP_201_CREATED)
        
        except ValidationError:
            logger.error("validation failed while registering the user")
            return Response(
                {
                    "message":"Validation failed",
                    "data":serializers.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )

        except BadHeaderError:
            logger.error("Invalid header found while sending mail")
            return Response(
                {
                    "message":"Invalid header found"
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
                )
        
        except Exception as e:
            logger.error(f"internal server error while registering the user{e}")
            return Response(
                {
                    "message":"internal server error"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class Verification(APIView):

    """
    This api use to validate the user email is it correct or not
    """
    
    def post(self, request):
        
        try:
            
            user = Users.objects.get(username=request.data.get("username"))
            user_data= UserSerializer(user)
            serializer = UserSerializer(user,data= user_data.data)
            if serializer.is_valid(raise_exception=True):
                if user.otp == request.data.get("otp"):
                    serializer.set_verified(validated_data=serializer.data)
                    return Response(
                        {
                            "message" : f'{serializer.data.get("username")} verfied',
                            "data": {"username":serializer.data.get("username")}
                        },
                        status=status.HTTP_202_ACCEPTED
                        )
                else:
                    return Response(
                        {
                            "message" : f'{serializer.data.get("username")} invalid otp',
                            "data": {"username":serializer.data.get("username")}
                        },
                        status=status.HTTP_304_NOT_MODIFIED
                        )

        except ValidationError:
            logger.error("validation failed while verify the user")
            return Response(
                {
                    "message":"Validation failed",
                    "data":serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e :
            logger.error(f"Couldn`t verify user due to {e}")
            return Response(
                {
                    "message": "failed to verify user",
                },
                status=status.HTTP_400_BAD_REQUEST
                )


class Login(APIView):

    def post(self, request):

        try:
            print(request.data)
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username= username,password= password)
            if user != None :
                if user.is_verified :
                    user.is_login = True
                    user.save()
                    serializers = UserSerializer(user)
                    encoded_token = EncodeDecodeToken.encode_token(serializers)
                    logger.info(f"logged in successfully by {serializers.data.get('id')}")
                    # redis_instence.set(serializers.data.get('id'),encoded_token)
                    return Response({"message":"logged in successfully","data":{"token":encoded_token}},status= status.HTTP_202_ACCEPTED)

                elif not user.is_verified :
                    return Response({"message":"user is not verified","data":user.id},status= status.HTTP_400_BAD_REQUEST)
            else:
                logger.warning("invalid login details")
                return Response(
                    {
                      "message":"invalid login details"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
        
        except Exception as e:
            logger.error(f"internal server error while login by the user {e}")
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Logout(APIView):

    def post(self, request):

        try:
            if 'HTTP_TOKEN' in request.META:
                decode_token = EncodeDecodeToken.decode_token(request.META.get('HTTP_TOKEN'))
                user = Users.objects.get(id=decode_token.get("user_id") )
                if user !=None:
                    user.is_login = False
                    user.save()
                    return Response({"message":"logged out successfully"},status= status.HTTP_202_ACCEPTED)
                else:
                    return Response({"message":"invalid token"},status= status.HTTP_400_BAD_REQUEST)

            else:
                logger.warning("token not found")
                return Response(
                    {
                        "message":"invalid details"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
        
        except Exception as e : 
            logger.error(f"internal server error while logout by the user {e}")
            return Response({"message":"internal server error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

