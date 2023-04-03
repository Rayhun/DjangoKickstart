"""site_settings > models > abstract.py"""
# DJANGO IMPORTS
import logging
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

logger = logging.getLogger(__name__)


class AbstractBaseFields(models.Model):
    is_active = models.BooleanField(
        _('Is Active'), default=True
    )
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_created"
    )
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )

    updated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_updated"
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )

    is_deleted = models.BooleanField(
        _('Is Deleted'), default=False
    )
    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_deleted"
    )
    deleted_at = models.DateTimeField(
        _('Deleted At'), blank=True, null=True
    )

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def soft_deactivate(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True
