from base.views import BaseCreateAPIView

from .serializers import AffiliateCreateSerializer


class AffiliateCreateView(BaseCreateAPIView):
    serializer_class = AffiliateCreateSerializer
