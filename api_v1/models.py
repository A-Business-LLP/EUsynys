from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class UserRole(models.TextChoices):
        USER = 'user', _('User')
        CURATOR = 'curator', _('Curator')
        SUPERUSER = 'superuser', _('Superuser')

    user_name = models.CharField(_("user name"), unique=True, max_length=64)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)

    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name


class Region(models.Model):
    name = models.CharField(_("region name"), max_length=255, unique=True)
    users = models.ManyToManyField(CustomUser, related_name="regions", verbose_name=_("users"))

    def __str__(self):
        return self.name


class Table(models.Model):
    class TablePerformance(models.TextChoices):
        ATTACHMENT = 'вложение', _("attachment")
        DISCOVERY_CORPSE = "обнаружение трупа", _("discovery corpse")
        SK_DEATH = "ск.смерть", _("sk.death")
        BVP_ADULT = "БВП Совершеннолетний", _("BVP adult")
        LOSS_ITEMS = "утеря вещей", _("Loss items")
    
    class TableWhereOrderSent(models.TextChoices):
        OMPS = "ОМПС", _("OMPS")
        PROBATION_SERVICE = "служба пробации", _("probation service")
        LOCAL_EXECUTIVE_BODIES = "местные испол.органы", _("local executive bodies")
        EDUCATIONAL_INSTITUTIONS = "учреждения образования", _("educational institutions")
        MEDICAL_INSTITUTIONS = "медицинские учреждения", _("medical institutions")
        PRIVATE_BUSINESS_ENTITIES = "субъекты частного бизнеса (ИП, ЧП)", _("private business entities")
        PRODUCTIVE_ENTERPRISES = "производительные предприятия (заводы, фабрики и др)", _("productive enterprises")
        OTHER_INSTITUTIONS_ORGANIZATIONS_ASSOCIATIONS = "иные учреждения, организации и объединения", _("other institutions, organizations and associations")

    class TableResults(models.TextChoices):
        ADM_RESPONSE = "адм.ответ", _("adm.response")
        ST_479_KoAP = "ст.479 КоАП", _("st.479 KoAP")
        ST_661_KoAP = "ст.661 КоАП", _("st.661 KoAP")
        DISS_ANSWER = "дисц.ответ", _("diss.answer")
        NO_ACTION_TAKEN = "меры не приняты", _("no_action_taken")

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="tables")
    number = models.IntegerField(unique=True)
    calendar = models.DateTimeField(default=timezone.now)
    article_сriminal_сode = models.IntegerField()
    performance = models.CharField(max_length=255, choices=TablePerformance.choices)
    date_referral = models.DateTimeField(default=timezone.now)
    where_order_sent = models.CharField(max_length=255, choices=TableWhereOrderSent.choices)
    review_period = models.IntegerField(default=30)
    response_received = models.DateTimeField(null=True, blank=True)
    results = models.CharField(max_length=255, choices=TableResults.choices)
    submissions_reviewed_deadline = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.date_referral and self.response_received:
            delta = self.response_received - self.date_referral
        elif self.date_referral and not self.response_received:
            delta = timezone.now() - self.date_referral
        else:
            self.submissions_reviewed_deadline = False
            super(Table, self).save(*args, **kwargs)
            return

        self.submissions_reviewed_deadline = delta.days < self.review_period
        super(Table, self).save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.number}"
