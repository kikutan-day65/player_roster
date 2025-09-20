from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import OnlyLettersValidator


class Player(models.Model):
    only_letters_validator = OnlyLettersValidator()

    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    # team_id(FK)
    first_name = models.CharField(
        _("first_name"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters only."),
        validators=[only_letters_validator],
    )
    last_name = models.CharField(
        _("last_name"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters only."),
        validators=[only_letters_validator],
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Timestamp of when the player was created"),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("Timestamp of when the player was updated"),
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        null=True,
        blank=True,
        help_text=_("Timestamp of when the player was deleted"),
    )
