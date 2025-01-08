from datetime import timedelta

from django.db.models import QuerySet


class BaseQuery(QuerySet):
    model = None

    def __init__(self, *args, **kwargs):
        if kwargs.get("model"):
            self.model = kwargs.get("model")
        if not self.model:
            raise ValueError(f"model in class {self.__class__.__name__} is not defined")

    def _get_base_queryset(self, params):
        base_filter = self._get_base_filter(params)

        return self.model.objects.filter(**base_filter)

    def _get_base_filter(self, params):
        return {}
