from uuid import UUID

import pytest
from django.core.exceptions import ValidationError

from roster.models import Team


@pytest.mark.django_db
def test_success_to_create_team_with_valid_data(team_data):
    team = Team.objects.create(**team_data)

    assert team.id is not None
    assert isinstance(team.id, UUID)
    assert team.sport == team_data["sport"]
    assert team.name == team_data["name"]
    assert team.created_at is not None
    assert team.updated_at is not None
    assert team.deleted_at is None


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["sport", "name"])
def test_fails_to_create_team_without_required_fields(missing_field, team_data):
    team_data.pop(missing_field)

    invalid_team = Team(**team_data)

    with pytest.raises(ValidationError):
        invalid_team.full_clean()


@pytest.mark.django_db
def test_fails_to_create_team_by_max_length_constraint_violation(team_data):
    team_data["name"] = "a" * 200

    invalid_team = Team(**team_data)

    with pytest.raises(ValidationError):
        invalid_team.full_clean()


@pytest.mark.django_db
def test_fails_to_create_team_by_nonexistent_sport_in_choices(team_data):
    team_data["sport"] = "dummy"

    invalid_team = Team(**team_data)

    with pytest.raises(ValidationError):
        invalid_team.full_clean()


@pytest.mark.django_db
def test_fails_to_create_team_by_validator_violation(team_data):
    team_data["name"] = "---"

    invalid_team = Team(**team_data)

    with pytest.raises(ValidationError):
        invalid_team.full_clean()


@pytest.mark.django_db
def test_success_to_check_soft_delete_method(teams):
    team = teams[0]

    assert team.deleted_at is None

    team.soft_delete()

    assert team.deleted_at is not None


@pytest.mark.django_db
def test_success_to_check_is_deleted_property(teams):
    team = teams[0]

    assert team.is_deleted is False

    team.soft_delete()

    assert team.is_deleted is True


@pytest.mark.django_db
def test_success_to_check_str_method(teams):
    team = teams[0]
    result = team.__str__()

    assert result == team.name
