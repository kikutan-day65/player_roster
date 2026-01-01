# Test for CommentViewSet

## Create (`POST comments/`)

### Positive cases

-   [x] Returns 201
-   [x] Allows authenticated user
-   [x] Saves a new comment to the database

#### Serializer

-   [x] Uses serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `player`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Searching

-   [x] Result is returned with search field `body`
-   [x] Result is returned with search field `user__username`
-   [x] Result is returned with search field `player__first_name`
-   [x] Result is returned with search field `player__last_name`

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Fails to create comment without required fields
-   [x] Fails to create comment due to nonexistent`player_id`

## List (`GET comments/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Result includes soft-deleted comment for admin
-   [x] Result excludes soft-deleted comment for public

#### Serializer (public)

-   [x] Uses serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `player`, `user`)
-   [x] Nested `user` contains expected fields (`id`, `username`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Serializer (admin)

-   [x] Uses serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `player`, `user`)
-   [x] Nested `user` contains expected fields (`id`, `username`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Ordering

-   [x] Response returns in descending order of `created_at`

#### Filtering

-   [x] Result is returned with filtering `user_username` (`icontains`)
-   [x] Result is returned with filtering `player_first_name` (`icontains`)
-   [x] Result is returned with filtering `player_last_name` (`icontains`)
-   [x] Result is returned with filtering `created_at` (`date`)
-   [x] Result is returned with filtering `created_at_year` (`year`)
-   [x] Result is returned with filtering `created_at_year_gte` (`year__gte`)
-   [x] Result is returned with filtering `created_at_year_lte` (`year__lte`)

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

### Negative cases

-   [x] No negative cases for list action

## Retrieve (`GET comments/<id>/`)

### Positive cases

-   [x] Returns 200
-   [x] Allows anonymous user

#### Queryset

-   [x] Can get soft-deleted comment for admin
-   [x] Cannot soft-deleted comment for public

#### Serializer (public)

-   [x] Uses serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `player`, `user`)
-   [x] Nested `user` contains expected fields (`id`, `username`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Serializer (admin)

-   [x] Uses serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `player`, `user`)
-   [x] Nested `user` contains expected fields (`id`, `username`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

### Negative cases

-   [x] Returns 404 for nonexistent comment

## Partial update (`PATCH comments/<id>/`)

### Positive cases

-   [x] Returns 200 for valid request
-   [x] Allows admin
-   [x] Allows comment owner

#### Queryset

-   [x] Admin can patch soft-deleted comment
-   [x] Owner cannot patch soft-deleted comment

#### Serializer (admin)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `player`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

#### Serializer (owner)

-   [x] Uses correct serializer
-   [x] Response contains expected fields (`id`, `body`, `created_at`, `updated_at`, `player`)
-   [x] Nested `player` contains expected fields (`id`, `first_name`, `last_name`, `team`)
-   [x] Nested `team` contains expected fields (`id`, `name`)

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user (not owner)
-   [x] Fails to patch for nonexistent comment

## Destroy action (`DELETE comments/<id>/`)

### Positive cases

-   [x] Returns 204
-   [x] Allows super user
-   [x] Allows comment owner
-   [x] `deleted_at` filed is set

### Negative cases

-   [x] Returns 401 for anonymous user
-   [x] Returns 403 for general user (not owner)
-   [x] Returns 403 for admin user
-   [x] Fails to delete for nonexistent comment
