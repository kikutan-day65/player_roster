from django.core import validators


class OnlyLettersValidator(validators.RegexValidator):
    regex = r"^[A-Za-z]+$"
    message = "Only letters are allowed."
