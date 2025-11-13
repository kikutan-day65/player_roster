# Test for Team

## Positive cases

Success to create a team with valid data

-   [x] `id` is not None and is UUID
-   [x] `sport` matches input sport
-   [x] `name` matches input name
-   [x] `created_at` is set automatically
-   [x] `updated_at` is set automatically
-   [x] `deleted_at` is set to `None`

Check behavior of `soft_delete()` method on `Team`

-   [x] Returns `deleted_at` is not `None`

Check behavior of `is_deleted` property on `Team`

-   [x] Returns `False` when `deleted_at` is `None`
-   [x] Returns `True` when `deleted_at` is not `None`

Check behavior of `__str__()` method on `Team`

-   [x] Returns `name`

## Negative cases

Fails to create a team without required fields

-   [x] Raises `ValidationError` if `sport` is missing
-   [x] Raises `ValidationError` if `name` is missing

Fails to create a team due to `max_length` constraint violation

-   [x] Raises `ValidationError` if `name` violates `max_length` constraint

Fails to create a team with invalid `sport`

-   [x] Raises `ValidationError` if `sport` does not exist in choice

Fails to create a player due to `only_letters_numerics_validator` constraint violation

-   [x] Raises `ValidationError` if `first_name` violates `only_letters_numerics_validator` constraint
-   [x] Raises `ValidationError` if `last_name` violates `only_letters_numerics_validator` constraint
