from django.core.cache import cache
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    USE_CACHE = False  # Set to True if you want to cache the object
    CACHE_TIMEOUT = None
    CACHE_KEY = "id"
    SOFT_DELETE = True

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Updated at"),
    )
    if SOFT_DELETE:
        deleted_at = models.DateTimeField(
            null=True,
            blank=True,
            default=None,
            verbose_name=_("Deleted at"),
        )

    def save(self, *args, **kwargs):
        cache_key = f"{self.__class__.__name__.lower()}_{getattr(self, self.CACHE_KEY)}"
        if self.USE_CACHE and cache.get(cache_key):
            cache.set(cache_key, self, timeout=self.CACHE_TIMEOUT)

        return super().save(*args, **kwargs)

    @classmethod
    def get_from_cache(cls, key_value):
        """Get object by key from cache, if not found, get from database and set to cache"""
        cache_key = f"{cls.__name__.lower()}_{key_value}"

        obj = cache.get(cache_key)
        if not obj:
            obj = cls.objects.get(**{cls.CACHE_KEY: key_value})
            cache.set(cache_key, obj, timeout=cls.CACHE_TIMEOUT)

        return obj

    class BaseModelManager(models.Manager):
        def get_queryset(self):
            if hasattr(self.model, "deleted_at"):
                return super().get_queryset().filter(deleted_at__isnull=True)
            return super().get_queryset()

    def delete(self, *args, **kwargs):
        if hasattr(self, "deleted_at"):
            self.deleted_at = now()
            self.save(update_fields=["deleted_at"])
        else:
            super().delete(*args, **kwargs)

    objects = BaseModelManager()
    objects_all = models.Manager()

    class Meta:
        abstract = True
