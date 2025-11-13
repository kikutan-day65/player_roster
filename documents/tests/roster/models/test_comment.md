# Test for Comment

## Positive cases

Success to create a comment with valid data

-   [x] `id` is not None and is UUID
-   [x] `user` matches input user
-   [x] `player` matches input player
-   [x] `body` matches input body
-   [x] `created_at` is set automatically
-   [x] `updated_at` is set automatically
-   [x] `deleted_at` is set to `None`

Check behavior of `soft_delete()` method on `Comment`

-   [x] Returns `deleted_at` is not `None`

Check behavior of `is_deleted` property on `Comment`

-   [x] Returns `False` when `deleted_at` is `None`
-   [x] Returns `True` when `deleted_at` is not `None`

Check behavior of `__str__()` method on `Comment`

-   [x] Returns `body`
-   [x] Returns `body[:100]` + `...` if `body` is more than 100 characters

## Negative cases

Fails to create a comment without required fields

-   [x] Raises `ValidationError` if `user` is missing
-   [x] Raises `ValidationError` if `player` is missing
-   [x] Raises `ValidationError` if `body` is missing
