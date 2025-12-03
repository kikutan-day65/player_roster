from uuid import UUID

import pytest
from django.core.exceptions import ValidationError

from roster.models import Player


@pytest.mark.django_db
def test_success_to_create_player_with_valid_data(player_data, teams):
    player = Player.objects.create(**player_data)

    assert player.id is not None
    assert isinstance(player.id, UUID)
    assert player.team == teams[0]
    assert player.first_name == "FirstName"
    assert player.last_name == "LastName"
    assert player.created_at is not None
    assert player.updated_at is not None
    assert player.deleted_at is None


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["team_id", "first_name", "last_name"])
def test_fails_to_create_player_without_required_fields(missing_field, player_data):
    player_data.pop(missing_field)

    invalid_player = Player(**player_data)

    with pytest.raises(ValidationError):
        invalid_player.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("target_field", ["first_name", "last_name"])
def test_fails_to_create_player_by_max_length_constraint_violation(
    target_field, player_data
):
    player_data[target_field] = "a" * 200

    invalid_team = Player(**player_data)

    with pytest.raises(ValidationError):
        invalid_team.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("target_field", ["first_name", "last_name"])
def test_fails_to_create_player_by_validator_violation(target_field, player_data):
    player_data[target_field] = "12345"
    invalid_user = Player(**player_data)

    with pytest.raises(ValidationError):
        invalid_user.full_clean()


@pytest.mark.django_db
def test_success_to_check_soft_delete_method(players):
    player = players[0]

    assert player.deleted_at is None

    player.soft_delete()

    assert player.deleted_at is not None


@pytest.mark.django_db
def test_success_to_check_is_deleted_property(players):
    player = players[0]

    assert player.is_deleted is False

    player.soft_delete()

    assert player.is_deleted is True


@pytest.mark.django_db
def test_success_to_check_str_method(players):
    player = players[0]
    result = player.__str__()

    assert result == player.first_name + player.last_name
