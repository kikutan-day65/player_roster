from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.validators import only_letters_validator


class Player(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        related_name="players",
        verbose_name=_("team_id"),
    )
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

    def __str__(self):
        return self.first_name + self.last_name


class Team(models.Model):
    class SportChoice(models.TextChoices):
        BASEBALL = "baseball", "Baseball"
        FOOTBALL = "football", "Football"
        BASKETBALL = "basketball", "Basketball"

    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    sport = models.CharField(
        _("sport_name"), max_length=50, choices=SportChoice.choices
    )
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

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        "user_account.UserAccount",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("user_id"),
    )
    player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("player_id"),
    )
    body = models.TextField(_("body"))
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Timestamp of when the comment was created"),
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("Timestamp of when the comment was updated"),
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        null=True,
        blank=True,
        help_text=_("Timestamp of when the comment was deleted"),
    )


class Favorite(models.Model):
    id = models.UUIDField(_("id"), primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        "user_account.UserAccount",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("user_id"),
    )
    player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("player_id"),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Timestamp of when the favorite was created"),
    )
