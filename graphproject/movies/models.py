from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import Country
from .validators import validate_no_future_date, validate_production_year


class Artist(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    country = models.CharField(verbose_name=_("Country"), max_length=2, choices=Country.choices)
    birth_date = models.DateField(verbose_name=_("Birth date"), validators=[validate_no_future_date])

    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    year = models.PositiveSmallIntegerField(verbose_name=_("Year"), validators=[validate_production_year])
    director = models.ForeignKey(Artist, verbose_name=_("Director"), on_delete=models.PROTECT,
                                 related_name="directed_movies")
    actors = models.ManyToManyField(Artist, verbose_name=_("Actors"), related_name="played_movies")

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return f"{self.title} | {self.year}"
