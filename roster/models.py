from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import only_letters_validator


class Player(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="players")
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


class Team(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    sport = models.ForeignKey("Sport", on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(
        _("team_name"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters only."),
        validators=[only_letters_validator],
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Timestamp of when the team was created"),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("Timestamp of when the team was updated"),
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        null=True,
        blank=True,
        help_text=_("Timestamp of when the team was deleted"),
    )


class Sport(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        _("sport_name"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters only."),
        validators=[only_letters_validator],
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Timestamp of when the sport was created"),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("Timestamp of when the sport was updated"),
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        null=True,
        blank=True,
        help_text=_("Timestamp of when the sport was deleted"),
    )
