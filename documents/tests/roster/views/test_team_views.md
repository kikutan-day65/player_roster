# Test for TeamViewSet

## Create (`POST teams/`)

### Positive cases

-   [x] Returns 201 for valid data
-   [x] Allows admin user
-   [x] Saves a new team to the database

#### Serializer

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `name`, `sport`, `created_at`)

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Fails to create team without required fields
-   [x] Fails to create team due to invalid choice for `sport` field
-   [x] Fails to create team due to violating `only_letters_numerics_validator` for `name` field

## List (`GET teams/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Public account excludes soft-deleted teams (`deleted_at`)
-   [x] Admin account includes soft-deleted teams (`deleted_at`)

#### Serializer (public)

-   [x] Uses correct serializer for public account
-   [x] Response contains expected fields (`id`, `name`, `sport`, `created_at`) for public account

#### Serializer (admin)

-   [x] Uses correct serializer for admin account
-   [x] Response contains expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`, `deleted_at`) for admin account

#### Ordering

-   [x] Results are returned in descending order of created_at

#### Filtering

-   [x] Result is returned with filtering `sport` (`exact`)
-   [x] Result is returned with filtering `name` (`icontains`)
-   [x] Result is returned with filtering `created_at` (`date`)
-   [x] Result is returned with filtering `created_at_year` (`year`)
-   [x] Result is returned with filtering `created_at_year_gte` (`year__gte`)
-   [x] Result is returned with filtering `created_at_year_lte` (`year__lte`)

### Negative cases

-   [x] No negative cases for list action

## Retrieve (`GET teams/<id>/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Admin account can get soft-deleted teams (`deleted_at`)

#### Serializer (public)

-   [x] Uses correct serializer for public account
-   [x] Response contains expected fields (`id`, `name`, `sport`, `created_at`) for public account

#### Serializer (admin)

-   [x] Uses correct serializer for admin account
-   [x] Response contains expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`, `deleted_at`) for admin account

### Negative cases

-   [x] Returns 404 for nonexistent team
-   [x] Public account cannot get soft-deleted teams (`deleted_at`)

## Partial update (`PATCH teams/<id>/`)

### Positive cases

-   [x] Returns 200 for valid request
-   [x] Allows admin user
-   [x] Only allowed fields are updated
-   [x] Not allowed fields remain unchanged

#### Queryset

-   [x] Admin user can patch soft-deleted team

#### Serializer fields (admin)

-   [x] Uses correct serializer for admin account
-   [x] Response contains expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`) for admin account

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Returns 404 when trying to patch nonexistent team
-   [x] Fails to patch with invalid choice for `sport` field
-   [x] Fails to patch due to `only_letters_numerics_validator` violation for `name` field

## Destroy (`DELETE teams/<id>/`)

### Positive cases

-   [x] Returns 204
-   [x] Allows super user
-   [x] `deleted_at` filed is set

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Returns 403 for admin user
-   [x] Returns 404 when trying to delete nonexistent team

## Players (`GET teams/<team_pk>/players/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Result excludes soft-deleted players (`deleted_at`) for public
-   [x] Result includes soft-deleted players (`deleted_at`) for admin

#### Serializer (public)

-   [x] Uses correct serializer
-   [x] Response contains the expected fields (`id`, `first_name`, `last_name`, `created_at`)

#### Serializer (admin)

-   [x] Uses correct serializer
-   [x] Response contains the expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`)

#### Ordering

-   [x] Results are returned in descending order of `created_at`

### Negative cases

-   [x] No negative cases for players action
