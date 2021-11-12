import logging
from rest_framework import serializers
from users.models import Users
from users.utility import generate_otp

logging.basicConfig(filename="fundooNotes.log",filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = Users
        fields = ["id","username","email","password","first_name","last_name","is_login","is_verified","contact_number","otp"] 

    def create(self, validated_data):
        
        try:

            new_user = Users.objects.create_user(validated_data.get("username"),validated_data.get("email"),validated_data.get("password"))
            new_user.first_name = validated_data.get("first_name")
            new_user.last_name = validated_data.get("last_name")
            new_user.contact_number = validated_data.get("contact_number")
            new_user.save()

        except Exception as e:
            logger.error("Error to create a user in seralizers")
            print(e)

    def set_verified(self, validated_data):

        user = Users.objects.get(username = validated_data.get("username"))
        user.is_verified = True
        user.save()
        