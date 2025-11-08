# Test for UserAccount

## Positive Cases

Success to create a **general user** with valid data

-   [x] `id` is set automatically and is UUID
-   [x] `username` matches the input username
-   [x] `email` matches the input email
-   [x] `password` is stored in a hashed form
-   [x] `is_staff` is set to `False`
-   [x] `is_superuser` is set to `False`
-   [x] `is_active` is set to `True`
-   [x] `created_at` is set automatically
-   [x] `updated_at` is set automatically
-   [x] `deleted_at` is set to `None`

Success to create a **admin user** with valid data

-   [x] `id` is set automatically and is UUID
-   [x] `username` matches the input username
-   [x] `email` matches the input email
-   [x] `password` is stored in a hashed form
-   [x] `is_staff` is set to `True`
-   [x] `is_superuser` is set to `False`
-   [x] `is_active` is set to `True`
-   [x] `created_at` is set automatically
-   [x] `updated_at` is set automatically
-   [x] `deleted_at` is set to `None`

Success to create a **super user** with valid data

-   [x] `id` is set automatically and is UUID
-   [x] `username` matches the input username
-   [x] `email` matches the input email
-   [x] `password` is stored in a hashed form
-   [x] `is_staff` is set to `True`
-   [x] `is_superuser` is set to `True`
-   [x] `is_active` is set to `True`
-   [x] `created_at` is set automatically
-   [x] `updated_at` is set automatically
-   [x] `deleted_at` is set to `None`

Check behavior of `soft_delete()` method

-   [x] Returns `deleted_at` is not `None`

Check behavior of `is_deleted` property

-   [x] Returns `False` when `deleted_at` is `None`
-   [x] Returns `True` when `deleted_at` is not `None`

Check behavior of `__str__()` method

-   [x] Returns `username`

## Negative Cases

Fails to create a user without required fields

-   [x] Raises `TypeError` if `username` is missing
-   [x] Raises `ValueError` if`email` is missing
-   [x] Raises `ValueError` if`password` is missing

Fails to create a user due to invalid email format

-   [x] Raises `ValidationError` if `email` is invalid format

Fails to create a user due to `max_length` constraint violation

-   [x] Raises `ValidationError` if `username` violates `max_length` constraint

Fails to create a user due to unique constraint violation

-   [x] Raises `ValidationError` if `username` violates `unique` constraint
-   [x] Raises `ValidationError` if `email` violates `unique` constraint
