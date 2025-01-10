from rest_framework.response import Response

from base.views import BaseCreateAPIView

from .serializers import UserLoginSerializer, UserRegisterSerializer


class UserRegisterView(BaseCreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserRegisterSerializer


class UserLoginView(BaseCreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.login())
