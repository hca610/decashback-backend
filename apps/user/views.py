from base.views import BaseCreateAPIView

from .serializers import ExchangeAccountAddSerializer


class ExchangeAccountAddView(BaseCreateAPIView):
    serializer_class = ExchangeAccountAddSerializer
