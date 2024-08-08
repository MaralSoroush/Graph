from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_no_future_date(value):
    if value > timezone.now().date():
        raise ValidationError("The date cannot be in the future.")


def validate_production_year(value):
    # Year 1895, is historically recognized as the year of the first publicly screened films.
    this_year = timezone.now().year
    if value > this_year or value < 1895:
        raise ValidationError(f"The year should be between 1895 and {this_year}.")
