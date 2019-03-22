import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.


class SettingQuerySet(models.QuerySet):
    def __getattr__(self, item):
        instance = self.filter(name=item)
        if len(instance) == 1:
            return instance[0]
        else:
            return Setting()


class SettingManager(models.Manager):
    def get_queryset(self):
        return SettingQuerySet(self.model, using=self._db)


class Setting(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name=_('Name'))
    value = models.TextField(verbose_name=_('Value'))
    category = models.CharField(max_length=128, default='default')
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    comment = models.TextField(verbose_name=_('Comment'))

    objects = SettingManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'common_settings'
        verbose_name = _('Settings')

    @property
    def cleaned_value(self):
        try:
            return json.loads(self.value)
        except json.JSONDecodeError:
            return None

    @cleaned_value.setter
    def cleaned_value(self, item):
        try:
            v = json.dumps(item)
            self.value = v
        except json.JSONDecodeError as e:
            raise ValueError("Json dump error: {}".format(str(e)))

    @classmethod
    def refresh_all_settings(cls):
        """ 将全部配置项刷入django的settings """
        try:
            settings_list = cls.objects.all()
            for setting in settings_list:
                setting.refresh_setting()
        except:
            pass

    def refresh_setting(self):
        """ 将配置项刷入django的settings """
        try:
            value = json.loads(self.value)
        except json.JSONDecodeError:
            return
        setattr(settings, self.name, value)
