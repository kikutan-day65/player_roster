from django.core.validators import RegexValidator

only_letters_validator = RegexValidator(
    regex=r"^[A-Za-z ]+$", message="Only letters are allowed."
)
