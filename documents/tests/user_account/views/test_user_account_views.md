# Test for UserAccountViewSet

## Create (`POST user-accounts/`)

### Positive cases

-   [x] Returns 201 for valid request
-   [x] Allows anonymous user
-   [x] Saves a new user to the database
-   [x] Uses `UserAccountCreateSerializer` for create action
-   [x] Response contains expected fields (`id`, `username`, `email`, `created_at`)

### Negative cases

-   [x] Returns 400 for invalid request
-   [x] Fails to create without required fields
-   [x] Fails to create with invalid field formats
-   [x] Fails to create with duplicate unique fields
-   [x] Does not save a new user to the database
-   [x] Fails to create due to `username_validator` violation

## List (`GET user-accounts/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Public account excludes soft-deleted users (`deleted_at`)
-   [x] Admin account includes soft-deleted users (`deleted_at`)

#### Serializer (Public)

-   [x] Uses correct serializer for public account
-   [x] Response contains expected fields (`id`, `username`, `created_at`) for public account

#### Serializer fields (Admin)

-   [x] Uses correct serializer for admin account
-   [x] Response contains expected fields (`id`, `username`, `email`, `is_superuser`, `is_staff`, `is_active`, `created_at`, `updated_at`, `deleted_at`) for admin account

#### Ordering

-   [x] Results are returned in descending order of created_at

#### Filtering

-   [x] Result is returned with filtering `username` (`icontains`)
-   [x] Result is returned with filtering `created_at` (`date`)
-   [x] Result is returned with filtering `created_at_year` (`year`)
-   [x] Result is returned with filtering `created_at_year_gte` (`year__gte`)
-   [x] Result is returned with filtering `created_at_year_lte` (`year__lte`)

#### Searching

-   [x] Result is returned with search fields with `username`

### Negative cases

-   [x] No negative cases for list action

## Retrieve (`GET user-accounts/<id>/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Admin can retrieve soft-deleted user (200)

#### Serializer (Public)

-   [x] Uses correct serializer for public account
-   [x] Response contains expected fields (`id`, `username`, `created_at`) for public account

#### Serializer fields (Admin)

-   [x] Uses correct serializer for admin account
-   [x] Response contains expected fields (`id`, `username`, `email`, `is_superuser`, `is_staff`, `is_active`, `created_at`, `updated_at`, `deleted_at`) for admin account

### Negative cases

-   [x] Returns 404 when trying to retrieve nonexistent user
-   [x] Public/anonymous user cannot retrieve soft-deleted user (404)

## Partial update (`PATCH user-accounts/<id>/`)

### Positive cases

-   [x] Returns 200 for valid request
-   [x] Allows admin user
-   [x] Only allowed fields are updated
-   [x] Not allowed fields remain unchanged

#### Queryset

-   [x] Admin user can patch soft-deleted user (200)

#### Serializer fields (admin)

-   [x] Uses correct serializer for admin user
-   [x] Response contains expected fields (`id`, `username`, `email`, `is_superuser`, `is_staff`, `is_active`, `created_at`, `updated_at`) for admin account

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Returns 404 when trying to patch nonexistent user
-   [x] Fails to patch with unique constraint violation
-   [x] Fails to patch for invalid email format
-   [x] Fails to patch for `username_validator` violation

## Destroy (`DELETE user-accounts/<id>/`)

### Positive cases

-   [x] Returns 204
-   [x] Allows superuser
-   [x] `deleted_at` field is set

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Returns 403 for admin user
-   [x] Returns 404 when trying to delete nonexistent user

## Comments (`GET user-accounts/<user_pk>/comments/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Public account excludes soft-deleted comments (`deleted_at`)
-   [x] Admin account includes soft-deleted comments (`deleted_at`)

#### Serializer (Public)

-   [x] Uses correct serializer for public account
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `player`) for public account
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`) for public account
-   [x] Nested `player.team` contains expected fields (`id`, `name`) for public account

#### Serializer fields (Admin)

-   [x] Uses correct serializer for admin account
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `player`) for admin account
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`)
-   [x] Nested `player.team` contains expected fields (`id`, `name`) for admin account

#### Ordering

-   [x] Results are returned in descending order of `created_at`

### Negative cases

-   [x] Returns 404 when trying to get comments on nonexistent user

# Test for MeAPIView

## Retrieve (`GET user-accounts/me/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows authenticated user
-   [x] `get_object()` returns the request user

#### Serializer

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `username`, `email`, `created_at`, `updated_at`)

### Negative cases

-   [x] Returns 401 for anonymous user

## Partial update (`PATCH user-accounts/me/`)

### Positive cases

-   [x] Returns 200 for valid data
-   [x] Allows authenticated user
-   [x] `get_object()` returns the request user
-   [x] Only allowed fields are updated
-   [x] Not allowed fields remain unchanged

#### Serializer

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `username`, `email`, `created_at`, `updated_at`)

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Fails to patch with unique constraint violation
-   [x] Fails to patch for invalid email format
-   [x] Fails to patch for `username_validator` violation

## Destroy (`DELETE user-accounts/me/`)

### Positive cases

-   [x] Returns 204
-   [x] Allows authenticated user
-   [x] `deleted_at` field is set

### Negative cases

-   [x] Returns 401 for anonymous user

# Test for MeCommentAPIView

## List (`GET user-accounts/me/comments/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows authenticated user

#### Queryset

-   [x] Comments excludes soft-deleted comments (`deleted_at`)

#### Serializer

-   [x] Uses correct serializer
-   [x] Response contains the expected fields (`id`, `body`, `created_at`, `updated_at`, `player`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `player.team` contains expected fields (`id`, `name`)

#### Ordering

-   [x] Results are returned in descending order of `created_at`

#### Filtering

-   [x] Result is returned with filtering `team_name` (`icontains`)
-   [x] Result is returned with filtering `player_first_name` (`icontains`)
-   [x] Result is returned with filtering `player_last_name` (`icontains`)
-   [x] Result is returned with filtering `created_at` (`date`)
-   [x] Result is returned with filtering `created_at_year` (`year`)
-   [x] Result is returned with filtering `created_at_year_gte` (`year__gte`)
-   [x] Result is returned with filtering `created_at_year_lte` (`year__lte`)

#### Searching

-   [x] Result is returned with search fields `body`
-   [x] Result is returned with search fields `player__first_name`
-   [x] Result is returned with search fields `player__last_name`

### Negative cases

-   [x] Returns 401 for anonymous user
