from base.views import BaseCreateAPIView, BaseListAPIView, BaseRetrieveAPIView

from .models import ExchangeAccount
from .serializers import (
    ExchangeAccountAddSerializer,
    ExchangeAccountDetailSerializer,
    ExchangeAccountListSerializer,
)


class ExchangeAccountAddView(BaseCreateAPIView):
    serializer_class = ExchangeAccountAddSerializer


class ExchangeAccountListView(BaseListAPIView):
    serializer_class = ExchangeAccountListSerializer

    def get_queryset(self):
        return ExchangeAccount.objects.filter(user_id=self.request.user.id)


class ExchangeAccountDetailView(BaseRetrieveAPIView):
    serializer_class = ExchangeAccountDetailSerializer

    def get_queryset(self):
        return ExchangeAccount.objects.filter(user_id=self.request.user.id)
