# Test for PlayerCreateSerializer

## Positive cases

### 1. Success to validate and save player data

-   [x] Validation is successful

-   [x] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `team`) are included in the output
-   [x] Unexpected fields (`updated_at`, `deleted_at`) are not included in the output

-   [x] `first_name` in the output matches that of the input player data
-   [x] `last_name` in the output matches that of the input player data
-   [x] `id` in the `team` field matches input `team_id`

### 2. Success to ignore read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [x] Validation fails without required fields (`team_id`, `first_name`, `last_name`)
-   [x] Appropriate error messages are returned for missing fields

---

# Test for PlayerListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a player instance

-   [x] Expected fields (`id`, `first_name`, `last_name`, `team`) are included in the output
-   [x] Unexpected fields (`created_at`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for PlayerListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a player instance

-   [x] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`, `team`) are included in the output
-   [x] Unexpected fields are not included in the output -> All fields are expected

---

# Test for PlayerPatchSerializer

## Positive cases

### 1. Success to validate and save player data with single field

-   [x] Validation is successful

-   [x] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `team`) are included in the output
-   [x] Unexpected fields (`deleted_at`) are not included in the output

-   [x] `first_name` in the output matches that of input player patch data
-   [x] `last_name` in the output matches that of input player patch data
-   [] `id` in the `team` field matches input `team_id`

### 2. Success to ignore read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`, `updated_at`) are not in `validated_data`

---

# Test for PlayerCommentListPublicSerializer

## Positive cases

### 1. Success to serialize comment instance on player

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `user`) are included in the output
-   [x] Unexpected fields (`player`, `deleted_at`) are not included in the output

---

# Test for PlayerCommentListAdminSerializer

## Positive cases

### 1. Success to serialize comment instance on player

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `user`) are included in the output
-   [x] Unexpected fields (`player`) are not included in the output
