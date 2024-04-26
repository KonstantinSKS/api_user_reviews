from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    year = timezone.now().year
    if year < value:
        raise ValidationError(
            'Год выпуска не может быть больше текущего!')
    return value
