from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import requests


class BluelineId(models.Model):
    server_url = models.URLField(
        'API Server URL',
        max_length=250,
        default='https://blueline.extss.de/order_log/',
    )
    blueline_id = models.CharField(
        'Blueline ID',
        max_length=50,
        unique=True,
        #editable=False,
        blank=True, null=True,
    )
    blueline_username = models.CharField(
        max_length=40,
        unique=True,
        #editable=False,
        blank=True, null=True,
    )
    blueline_password = models.CharField(
        max_length=20,
        unique=True,
        #editable=False,
        blank=True, null=True,
    )

    @classmethod
    def _send(cls, **kwargs):
        """
        Use utils.send_xxx() instead
        """
        blueline_id = cls.objects.filter(id=settings.SITE_ID).first()
        if blueline_id:
            server_url = blueline_id.server_url
            kwargs['blueline_id'] = blueline_id.blueline_id
            result = requests.get(server_url, params=kwargs)
            if result.status_code == 200:
                return result.json()['success']
        return False

    def _generate_blueline_id(self):
        blueline_id = []
        for i in range(len(self.blueline_username)):
            blueline_id.append(self.blueline_username[i])
            blueline_id.append(self.blueline_password[i])
        return ''.join(blueline_id)

    def _generate_blueline_username(self):
        return self.blueline_id[0::2]

    def _generate_blueline_password(self):
        return self.blueline_id[1::2]

    def clean(self):
        bl_id = self.blueline_id
        bl_user = self.blueline_username
        bl_pw = self.blueline_password

        if not any([bl_id, all([bl_user, bl_pw])]):
            raise ValidationError(
                _('Either full id or user and password needed'),
            )

        if self.blueline_username and self.blueline_password:
            if len(self.blueline_username) != len(self.blueline_password):
                raise ValidationError(
                    _('Username and password must have the same length')
                )

        if all([bl_id, bl_user, bl_pw]):
            try:
                assert bl_id == self._generate_blueline_id()
                assert bl_user == self._generate_blueline_username()
                assert bl_pw == self._generate_blueline_password()
            except AssertionError as err:
                raise ValidationError(err) from err

        super().clean()

    def save(self, **kwargs):  #pylint: disable=arguments-differ
        if self.blueline_id:
            self.blueline_username = self._generate_blueline_username()
            self.blueline_password = self._generate_blueline_password()
        else:
            self.blueline_id = self._generate_blueline_id()
        #pylint: disable=invalid-name, attribute-defined-outside-init
        self.id = settings.SITE_ID
        return super().save(**kwargs)

    def __str__(self):
        return self.blueline_id
