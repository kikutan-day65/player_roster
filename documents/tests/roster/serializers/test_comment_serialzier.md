# Test for CommentCreateSerializer

## Positive cases

### 1. Success to validate and save comment data

-   [x] Validation is successful

-   [x] Expected fields (`id`, `body`, `created_at`, `player`) are included in the output
-   [x] Unexpected fields (`user`, `updated_at`, `deleted_at`) are not included in the output

-   [x] `body` in the output matches that of input comment data
-   [x] `id` in the `player` field matches input `player_id`

-   [x] `player` contains nested `team` structure

### 2. Success to ignore read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [x] Validation fails without required fields (`user_id`, `player_id`, `body`)
-   [x] Appropriate error messages are returned for missing fields

# Test for CommentListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a comment instance

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `player`, `user`) are included in the output
-   [x] Unexpected fields (`deleted_at`) are not included in the output
-   [x] `player` contains nested `team` structure

# Test for CommentListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a comment instance

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `player`, `user`) are included in the output
-   [x] Unexpected fields are not included in the output -> All fields are expected
-   [x] `player` contains nested `team` structure

# Test for CommentPatchSerializer

## Positive cases

### 1. Success to validate and save comment data with single field

-   [x] Validation is successful

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `player`) are included in the output
-   [x] Unexpected fields (`user`, `deleted_at`) are not in the output
-   [x] `player` contains nested `team` structure

-   [x] `body` in the output matches that of input comment patch data
-   [x] `id` in `player` field matches input `player_id`

### 2. Success to ignore read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`, `updated_at`) are not in `validated_data`
