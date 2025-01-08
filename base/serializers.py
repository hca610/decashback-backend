from rest_framework_mongoengine import serializers
from rest_framework_mongoengine.serializers import EmbeddedDocumentSerializer
from rest_framework_mongoengine.utils import get_nested_embedded_kwargs


class BaseMongoModelSerializer(serializers.DocumentSerializer):
    class Meta:
        abstract = True

    def build_nested_embedded_field(self, field_name, relation_info, embedded_depth):
        subclass = self.serializer_embedded_nested or EmbeddedDocumentSerializer

        class EmbeddedSerializer(subclass):
            class Meta:
                model = relation_info.related_model
                depth_embedding = embedded_depth - 1
                ref_name = "embedded_serializer"

        # Apply customization to nested fields
        customization = self.get_customization_for_nested_field(field_name)
        self.apply_customization(EmbeddedSerializer, customization)

        field_class = EmbeddedSerializer
        field_kwargs = get_nested_embedded_kwargs(field_name, relation_info)
        return field_class, field_kwargs
