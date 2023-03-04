import uuid

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedUpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeStampedCreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampedMixin(TimeStampedUpdateMixin, TimeStampedCreateMixin):
    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeChoice(models.TextChoices):
        movie = "movie", _("movie")
        tv_show = "tv_show", _("tv_show")

    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    creation_date = models.DateField(verbose_name=_("created_date"), blank=True, null=True)
    rating = models.FloatField(
        verbose_name=_("rating"),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    type = models.CharField(verbose_name=_("types"), max_length=7, choices=TypeChoice.choices, default=TypeChoice.movie)

    class Meta:
        db_table = 'content"."filmwork'
        verbose_name = _("film")
        verbose_name_plural = _("films")


class Product(UUIDMixin, TimeStampedMixin):
    name = models.CharField(verbose_name=_("title"), max_length=255)
    price = models.DecimalField(verbose_name=_("price"), max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'content"."product'
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self):
        return self.name


class FilmworkProduct(UUIDMixin, TimeStampedCreateMixin):
    filmwork = models.ForeignKey(to=Filmwork, verbose_name=_("filmwork"), on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, verbose_name=_("product"), on_delete=models.CASCADE)

    class Meta:
        db_table = 'content"."filmwork_product'
        constraints = [
            models.UniqueConstraint(fields=["filmwork", "product"], name="filmwork_product_group_idx"),
        ]
        verbose_name = _("filmwork_product")
        verbose_name_plural = _("filmwork_products")
