# Test for PlayerViewSet

## Create (`POST players/`)

### Positive cases

-   [x] Returns 201
-   [x] Allows admin user
-   [x] Saves a new player to the database

#### Serializer

-   [x] Use correct serializer
-   [x] Response contains expected fields (`id`, `first_name`, `last_name`, `created_at`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`) for public account

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Fails to create player without required fields
-   [x] Fails to create player due to nonexistent`team_id`
-   [x] Fails to create player due to violating `only_letters_validator` for `first_name` field
-   [x] Fails to create player due to violating `only_letters_validator` for `last_name` field

## List (`GET players/`)

### Positive cases

-   [x] Returns 200
-   [x] Allow anonymous user

#### Queryset

-   [x] Result includes soft-deleted player for admin
-   [x] Result excludes soft-deleted player for public

#### Serializer (public)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `first_name`, `last_name`, `created_at`,`team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Serializer (admin)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Ordering

-   [x] Response returns in descending order of `created_at`

#### Filtering

-   [x] Result is returned with filtering `team_name` (`icontains`)
-   [x] Result is returned with filtering `first_name` (`icontains`)
-   [x] Result is returned with filtering `last_name` (`icontains`)
-   [x] Result is returned with filtering `created_at` (`date`)
-   [x] Result is returned with filtering `created_at_year` (`year`)
-   [x] Result is returned with filtering `created_at_year_gte` (`year__gte`)
-   [x] Result is returned with filtering `created_at_year_lte` (`year__lte`)

#### Searching

-   [x] Result is returned with search field `first_name`
-   [x] Result is returned with search field `last_name`
-   [x] Result is returned with search field `team__name`

#### Throttling

##### Anonymous User

-   [x] Returns 200 for the first request
-   [x] Returns 200 for the second request
-   [x] Returns 429 for the third request

##### General User

-   [x] Returns 200 for the first request
-   [x] Returns 200 for the second request
-   [x] Returns 429 for the third request

##### Admin User

-   [x] Returns 200 for the first request
-   [x] Returns 200 for the second request
-   [x] Returns 429 for the third request

#### Ordering filter

-   [x] Results are returned in ascending order of `team__name` field
-   [x] Results are returned in descending order of `team__name` field
-   [x] Results are returned in ascending order of `first_name` field
-   [x] Results are returned in descending order of `first_name` field
-   [x] Results are returned in ascending order of `last_name` field
-   [x] Results are returned in descending order of `last_name` field
-   [x] Results are returned in ascending order of `created_at` field
-   [x] Results are returned in descending order of `created_at` field

### Negative cases

-   [x] No negative cases for list action

## Retrieve (`GET players/<id>/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Can get soft-deleted player for admin
-   [x] Cannot get soft-deleted player for public

#### Serializer (public)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `first_name`, `last_name`, `created_at`,`team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Serializer (admin)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

### Negative cases

-   [x] Returns 404 for nonexistent player

## Partial update (`PATCH players/<id>/`)

### Positive cases

-   [x] Returns 200 for valid request
-   [x] Allows admin user
-   [x] Only allowed fields are updated
-   [x] Not allowed fields remain unchanged

#### Queryset

-   [x] Can get soft-deleted player for admin

#### Serializer

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Fails to patch with nonexistent `team_id`
-   [x] Fails to patch with nonexistent player
-   [x] Fails to patch due to violating `only_letters_validator` for `first_name`
-   [x] Fails to patch due to violating `only_letters_validator` for `last_name`

## Destroy action (`DELETE players/<id>/`)

### Positive cases

-   [x] Returns 204
-   [x] Allows super user
-   [x] `deleted_at` filed is set

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user
-   [x] Returns 403 for admin user
-   [x] Returns 404 when trying to delete nonexistent player

## Comments action (`GET players/<id>/comments/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Can get soft-deleted comments for admin
-   [x] Cannot get soft-deleted comments for public

#### Serializer (public)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `user`)
-   [x] Nested `user` contains expected fields (`id`, `username`)

#### Serializer (admin)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `user`)
-   [x] Nested `user` contains expected fields (`id`, `username`)

#### Ordering

-   [x] Response returns in descending order of `created_at`

### Negative cases

-   [x] Returns 404 due to nonexistent player
