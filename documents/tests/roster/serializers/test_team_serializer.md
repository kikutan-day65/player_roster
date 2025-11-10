# Test for TeamCreateSerializer

## Positive cases

### 1. Success to validate and save team data

-   [] Validation is successful
-   [] Expected fields (`id`, `name`, `sport`, `created_at`) are included in the output
-   [] Unexpected fields (`updated_at`, `deleted_at`) are not included in the output

-   [] `name` in the output matches that of input team data
-   [] `sport` in the output matches that of input team data

### 2. Success to ignore read-only fields

-   [] Validation is successful

-   [] Read-only fields (`id`, `created_at`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [] Validation fails without required fields (`name`, `sport`)
-   [] Appropriate error messages are returned for missing fields

---

# Test for TeamListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a team instance

-   [] Expected fields (`id`, `name`, `sport`) are included in the output
-   [] Unexpected fields (`created_at`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for TeamListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a team instance

-   [] Expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`, `deleted_at`) are included in the output
-   [x] Unexpected fields are not included in the output -> All fields are expected

---

# Test for TeamPatchSerializer

## Positive cases

### 1. Success to validate and save team data with single field

-   [] Validation is successful

-   [] Expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`) are included in the output
-   [] Unexpected fields (`deleted_at`) are not included in the output

-   [] `name` in the output matches that of input team patch data
-   [] `sport` in the output matches that of input team patch data

### 2. Success to ignore read-only fields

-   [] Validation is successful

-   [] Read-only fields (`id`, `created_at`, `updated_at`) are not in `validated_data`

---

# Test for TeamPlayerListPublicSerializer

## Positive cases

### 1. Success to serialize a player instance

-   [] Expected fields (`id`, `first_name`, `last_name`) are included in the output
-   [] Unexpected fields (`team`, `created_at`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for TeamPlayerListAdminSerializer

## Positive cases

### 1. Success to serialize a player instance

-   [] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`) are included in the output
-   [] Unexpected fields (`team`) are not included in the output
