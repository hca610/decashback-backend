from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)


class SerializerContextMixin:
    context = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if hasattr(self.request.user, "id"):
            context.update(
                {
                    "user_id": self.request.user.id,
                }
            )
        self.context = context

        return context


class BaseListAPIView(SerializerContextMixin, ListAPIView):
    query_params = None
    params_serializer_class = None

    def parse_query_params(self):
        query_params = self.request.query_params
        query_params._mutable = True

        if self.params_serializer_class:
            param_serializer = self.params_serializer_class(data=query_params)
            param_serializer.is_valid(raise_exception=True)
            query_params = param_serializer.validated_data

        query_params.update(
            {
                "user_id": self.request.user.id,
                # "country": self.request.user.country,
            }
        )

        return query_params

    def get(self, request, *args, **kwargs):
        self.query_params = self.parse_query_params()
        self.query_params.update(kwargs)

        return self.list(request, *args, **kwargs)


class BaseCreateAPIView(SerializerContextMixin, CreateAPIView):
    pass


class BaseUpdateAPIView(SerializerContextMixin, UpdateAPIView):
    pass


class BaseRetrieveAPIView(SerializerContextMixin, RetrieveAPIView):
    pass


class BaseDestroyAPIView(SerializerContextMixin, DestroyAPIView):
    pass
