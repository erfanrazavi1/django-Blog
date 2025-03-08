from rest_framework import generics
from accounts.models import CustomUser
from rest_framework import status
from rest_framework.response import Response     
from accounts.api.v1.serializer import RegistrationSerializer
from rest_framework.authtoken.models import Token

class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'email': user.email,
            'phone': user.phone,
            'detail': 'User registered successfully'
        }
        return Response(data, status=status.HTTP_201_CREATED)
    


    
