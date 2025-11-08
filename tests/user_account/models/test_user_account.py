from uuid import UUID

import pytest
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from user_account.models import UserAccount


@pytest.mark.django_db
def test_success_to_create_general_user_with_valid_data(general_user_data):
    general_user = UserAccount.objects.create_user(**general_user_data)

    assert general_user.id is not None
    assert isinstance(general_user.id, UUID)
    assert general_user.username == "general_user"
    assert general_user.email == "general_user@example.com"
    assert check_password(general_user_data["password"], general_user.password)
    assert general_user.is_staff is False
    assert general_user.is_superuser is False
    assert general_user.is_active is True
    assert general_user.created_at is not None
    assert general_user.updated_at is not None
    assert general_user.deleted_at is None


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["username", "email", "password"])
def test_fails_to_create_general_user_without_required_fields(
    missing_field, general_user_data
):
    general_user_data.pop(missing_field)

    with pytest.raises((TypeError, ValueError)):
        UserAccount.objects.create_user(**general_user_data)


@pytest.mark.django_db
def test_fails_to_create_general_user_with_invalid_email_format(general_user_data):
    general_user_data["email"] = "invalid_email_format"
    invalid_user = UserAccount(**general_user_data)

    with pytest.raises(ValidationError):
        invalid_user.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize("target_field", ["username"])
def test_fails_to_create_general_user_by_max_length_constraint_violation(
    target_field, general_user_data
):
    general_user_data[target_field] = "a" * 200
    invalid_user = UserAccount(**general_user_data)

    with pytest.raises(ValidationError):
        invalid_user.full_clean()


@pytest.mark.django_db
def test_fails_to_create_general_user_by_unique_constraint_violation(general_user_data):
    UserAccount.objects.create_user(**general_user_data)
    general_user = UserAccount(**general_user_data)

    with pytest.raises(ValidationError) as e:
        general_user.full_clean()


@pytest.mark.django_db
def test_success_to_create_super_user_with_valid_data(super_user_data):
    super_user = UserAccount.objects.create_superuser(**super_user_data)

    assert super_user.id is not None
    assert isinstance(super_user.id, UUID)
    assert super_user.username == "super_user"
    assert super_user.email == "super_user@example.com"
    assert check_password(super_user_data["password"], super_user.password)
    assert super_user.is_staff is True
    assert super_user.is_superuser is True
    assert super_user.is_active is True
    assert super_user.created_at is not None
    assert super_user.updated_at is not None
    assert super_user.deleted_at is None


@pytest.mark.django_db
def test_success_to_check_soft_delete_method(general_user):
    assert general_user.deleted_at is None

    general_user.soft_delete()

    assert general_user.deleted_at is not None


@pytest.mark.django_db
def test_success_to_check_is_deleted_property(general_user):
    assert general_user.is_deleted is False

    general_user.soft_delete()

    assert general_user.is_deleted is True


@pytest.mark.django_db
def test_success_to_check_str_method(general_user):
    result = general_user.__str__()

    assert result == general_user.username
