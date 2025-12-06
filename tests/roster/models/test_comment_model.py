from uuid import UUID

import pytest
from django.core.exceptions import ValidationError

from roster.models import Comment


@pytest.mark.django_db
def test_success_to_create_comment_with_valid_data(comment_data):
    comment = Comment.objects.create(**comment_data)

    assert comment.id is not None
    assert isinstance(comment.id, UUID)
    assert comment.user.id == comment_data["user_id"]
    assert comment.player.id == comment_data["player_id"]
    assert comment.body == comment_data["body"]
    assert comment.created_at is not None
    assert comment.updated_at is not None
    assert comment.deleted_at is None


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["user_id", "player_id", "body"])
def test_fails_to_create_comment_without_required_fields(missing_field, comment_data):
    comment_data.pop(missing_field)

    invalid_comment = Comment(**comment_data)

    with pytest.raises(ValidationError):
        invalid_comment.full_clean()


@pytest.mark.django_db
def test_success_to_check_soft_delete_method(comments):
    comment = comments[0]

    assert comment.deleted_at is None

    comment.soft_delete()

    assert comment.deleted_at is not None


@pytest.mark.django_db
def test_success_to_check_is_deleted_property(comments):
    comment = comments[0]

    assert comment.is_deleted is False

    comment.soft_delete()

    assert comment.is_deleted is True


@pytest.mark.django_db
def test_success_to_check_str_method(comments):
    comment = comments[0]
    result = comment.__str__()

    assert result == comment.body

    comment_over_100 = comments[2]
    result = comment_over_100.__str__()

    assert result == comment_over_100.body[:100] + "..."
