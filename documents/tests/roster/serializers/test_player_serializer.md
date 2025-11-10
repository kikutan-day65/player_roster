# Test for PlayerCreateSerializer

## Positive cases

### 1. Success to validate and save player data

-   [] Validation is successful

-   [] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `team`) are included in the output
-   [] Unexpected fields (`updated_at`, `deleted_at`) are not included in the output

-   [] `first_name` in the output matches that of the input player data
-   [] `last_name` in the output matches that of the input player data
-   [] `id` in the `team` field matches input `team_id`

### 2. Success to ignore read-only fields

-   [] Validation is successful

-   [] Read-only fields (`id`, `created_at`, `team`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [] Validation fails without required fields (`team_id`, `first_name`, `last_name`)
-   [] Appropriate error messages are returned for missing fields

---

# Test for PlayerListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a player instance

-   [] Expected fields (`id`, `first_name`, `last_name`, `team`) are included in the output
-   [] Unexpected fields (`created_at`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for PlayerListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a player instance

-   [] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`, `team`) are included in the output
-   [] Unexpected fields are not included in the output -> All fields are expected

---

# Test for PlayerPatchSerializer

## Positive cases

### 1. Success to validate and save player data with single field

-   [] Validation is successful

-   [] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `team`) are included in the output
-   [] Unexpected fields (`deleted_at`) are not included in the output

-   [] `first_name` in the output matches that of input player patch data
-   [] `last_name` in the output matches that of input player patch data
-   [] `id` in the `team` field matches input `team_id`

### 2. Success to ignore read-only fields

-   [] Validation is successful

-   [] Read-only fields (`id`, `created_at`, `updated_at`, `team`) are not in `validated_data`

---

# Test for PlayerCommentListPublicSerializer

## Positive cases

### 1. Success to serialize comment instance on player

-   [] Expected fields (`id`, `body`, `created_at`, `updated_at`, `user`) are included in the output
-   [] Unexpected fields (`player`, `deleted_at`) are not included in the output

---

# Test for PlayerCommentListAdminSerializer

## Positive cases

### 1. Success to serialize comment instance on player

-   [] Expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `user`) are included in the output
-   [] Unexpected fields (`player`) are not included in the output
