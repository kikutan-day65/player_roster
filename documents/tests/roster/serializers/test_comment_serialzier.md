# Test for CommentCreateSerializer

## Positive cases

### 1. Success to validate and save comment data

-   [] Validation is successful

-   [] Expected fields (`id`, `body`, `created_at`, `player`) are included in the output
-   [] Unexpected fields (`user`, `updated_at`, `deleted_at`) are not included in the output

-   [] `body` in the output matches that of input comment data
-   [] `id` in the `player` field matches input `player_id`

-   [] `player` contains nested `team` structure

### 2. Success to ignore read-only fields

-   [] Validation is successful

-   [] Read-only fields (`id`, `created_at`, `player`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [] Validation fails without required fields (`player_id`, `body`)
-   [] Appropriate error messages are returned for missing fields

# Test for CommentListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a comment instance

-   [] Expected fields (`id`, `body`, `created_at`, `updated_at`, `player`, `user`) are included in the output
-   [] Unexpected fields (`deleted_at`) are not included in the output
-   [] `player` contains nested `team` structure

# Test for CommentListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a comment instance

-   [] Expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `player`, `user`) are included in the output
-   [] Unexpected fields are not included in the output -> All fields are expected
-   [] `player` contains nested `team` structure

# Test for CommentPatchSerializer

## Positive cases

### 1. Success to validate and save comment data with single field

-   [] Validation is successful

-   [] Expected fields (`id`, `body`, `created_at`, `updated_at`, `player`) are included in the output
-   [] Unexpected fields (`user`, `deleted_at`) are not in the output
-   [] `player` contains nested `team` structure

-   [] `body` in the output matches that of input comment patch data
-   [] `id` in `player` field matches input `player_id`

### 2. Success to ignore read-only fields

-   [] Validation is successful

-   [] Read-only fields (`id`, `created_at`, `updated_at`, `player`) are not in `validated_data`
