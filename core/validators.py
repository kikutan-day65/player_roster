from django.core.validators import RegexValidator

only_letters_validator = RegexValidator(
    regex=r"^[A-Za-z ]+$", message="Only letters are allowed."
)


only_letters_numerics_validator = RegexValidator(
    regex=r"^[A-Za-z0-9 ]+$", message="Only letters and numerics are allowed."
)
