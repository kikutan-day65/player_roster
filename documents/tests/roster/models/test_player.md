# Test for Player

## Positive cases

Success to create a player with valid data

-   [x] `id` is not None and is UUID
-   [x] `team` matches input team id
-   [x] `first_name` matches input first_name
-   [x] `last_name` matches input last_name
-   [x] `created_at` is set automatically
-   [x] `updated_at` is set automatically
-   [x] `deleted_at` is set to `None`

Check behavior of `soft_delete()` method on `Player`

-   [x] Returns `deleted_at` is not `None`

Check behavior of `is_deleted` property on `Player`

-   [x] Returns `False` when `deleted_at` is `None`
-   [x] Returns `True` when `deleted_at` is not `None`

Check behavior of `__str__()` method on `Player`

-   [x] Returns `first_name + last_name`

## Negative cases

Fails to create a player without required fields

-   [x] Raises `ValidationError` if `team_id` is missing
-   [x] Raises `ValidationError` if `first_name` is missing
-   [x] Raises `ValidationError` if `last_name` is missing

Fails to create a player due to `max_length` constraint violation

-   [x] Raises `ValidationError` if `first_name` violates `max_length` constraint
-   [x] Raises `ValidationError` if `last_name` violates `max_length` constraint

Fails to create a player due to `only_letters_validator` constraint violation

-   [x] Raises `ValidationError` if `first_name` violates `only_letters_validator` constraint
-   [x] Raises `ValidationError` if `last_name` violates `only_letters_validator` constraint
