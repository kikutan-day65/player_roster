# Test for TeamCreateSerializer

## Positive cases

### 1. Success to validate and save team data

-   [x] Validation is successful
-   [x] Expected fields (`id`, `name`, `sport`, `created_at`) are included in the output
-   [x] Unexpected fields (`updated_at`, `deleted_at`) are not included in the output

-   [x] `name` in the output matches that of input team data
-   [x] `sport` in the output matches that of input team data

### 2. Success to ignore read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [x] Validation fails without required fields (`name`, `sport`)
-   [x] Appropriate error messages are returned for missing fields

---

# Test for TeamListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a team instance

-   [x] Expected fields (`id`, `name`, `sport`) are included in the output
-   [x] Unexpected fields (`created_at`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for TeamListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a team instance

-   [x] Expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`, `deleted_at`) are included in the output
-   [x] Unexpected fields are not included in the output -> All fields are expected

---

# Test for TeamPatchSerializer

## Positive cases

### 1. Success to validate and save team data with single field

-   [x] Validation is successful

-   [x] Expected fields (`id`, `name`, `sport`, `created_at`, `updated_at`) are included in the output
-   [x] Unexpected fields (`deleted_at`) are not included in the output

-   [x] `name` in the output matches that of input team patch data
-   [x] `sport` in the output matches that of input team patch data

### 2. Success to ignore read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`, `updated_at`) are not in `validated_data`

---

# Test for TeamPlayerListPublicSerializer

## Positive cases

### 1. Success to serialize a player instance on team

-   [x] Expected fields (`id`, `first_name`, `last_name`) are included in the output
-   [x] Unexpected fields (`team`, `created_at`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for TeamPlayerListAdminSerializer

## Positive cases

### 1. Success to serialize a player instance on team

-   [x] Expected fields (`id`, `first_name`, `last_name`, `created_at`, `updated_at`, `deleted_at`) are included in the output
-   [x] Unexpected fields (`team`) are not included in the output
