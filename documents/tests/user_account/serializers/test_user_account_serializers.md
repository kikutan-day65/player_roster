# Test for UserAccountCreateSerializer

## Positive cases

### 1. Success to validate and save user data

-   [x] Validation is successful

-   [x] Expected fields (`id`, `username`, `email`, `created_at`) are included in the output
-   [x] Unexpected fields (`password`, `is_superuser`, `is_staff`, `is_active`, `updated_at`, `deleted_at`) are not included in the output

-   [x] `username` in the output matches that of input user data
-   [x] `email` in the output matches that of input user data

-   [x] `password` is stored in a hashed form

### 2. Success to ignore the read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`) are not in `validated_data`

## Negative cases

### 1. Fails to validate when required fields are missing

-   [x] Validation fails without required fields (`username`, `email`, `password`)
-   [x] Appropriate error messages are returned for missing fields

---

# Test for UserAccountListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize a user instance

-   [x] Expected fields (`id`, `username`, `created_at`) are included in the output
-   [x] Unexpected fields (`password`, `email`, `is_superuser`, `is_staff`, `is_active`, `updated_at`, `deleted_at`) are not included in the output

---

# Test for UserAccountListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize a user instance

-   [x] Expected fields (`id`, `username`, `email`, `is_superuser`, `is_staff`, `is_active`, `created_at`, `updated_at`, `deleted_at`) are included in the output
-   [x] Unexpected fields (`password`) are not included in the output

---

# Test for UserAccountPatchSerializer

## Positive cases

### 1. Success to validate and save user data with single field

-   [x] Validation is successful

-   [x] Expected fields (`id`, `username`, `email`, `is_superuser`, `is_staff`, `is_active`, `created_at`, `updated_at`) are included in the output
-   [x] Unexpected fields (`password`, `deleted_at`) are not included in the output

-   [x] `username` in the output matches that of input user patch data
-   [x] `email` in the output matches that of input user patch data
-   [x] `is_active` in the output matches that of input user patch data

### 2. Success to ignore the read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `is_superuser`, `is_staff`, `created_at`, `updated_at`) are not in `validated_data`

---

# Test for UserAccountCommentListRetrievePublicSerializer

## Positive cases

### 1. Success to serialize comment instance on user

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `player`) are included in the output
-   [x] Unexpected fields (`user`, `deleted_at`) are not included in the output

-   [x] `player` contains nested `team` structure

---

# Test for UserAccountCommentListRetrieveAdminSerializer

## Positive cases

### 1. Success to serialize comment instance on user

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `deleted_at`, `player`) are included in the output
-   [x] Unexpected fields (`user`) are not included in the output

-   [x] `player` contains nested `team` structure

---

# Test for MeRetrieveSerializer

## Positive cases

### 1. Success to serialize current user instance

-   [x] Expected fields (`id`, `username`, `email`, `created_at`, `updated_at`) are included in the output
-   [x] Unexpected fields (`password`, `is_superuser`, `is_staff`, `is_active`, `deleted_at`) are not included in the output

---

# Test for MePatchSerializer

## Positive cases

### 1. Success to validate and save current user data with single field

-   [x] Validation is successful

-   [x] Expected fields (`id`, `username`, `email`, `created_at`, `updated_at`) are included in the output
-   [x] Unexpected fields (`password`, `is_superuser`, `is_staff`, `is_active`, `deleted_at`) are not included in the output

-   [x] `username` in the output matches that of current user patch data
-   [x] `email` in the output matches that of current user patch data

### 2. Success to ignore the read-only fields

-   [x] Validation is successful

-   [x] Read-only fields (`id`, `created_at`, `updated_at`) are not in `validated_data`

---

# Test for MeCommentListSerializer

## Positive cases

### 1. Success to serialize comment instance on current user

-   [x] Expected fields (`id`, `body`, `created_at`, `updated_at`, `player`) are included in the output
-   [x] Unexpected fields (`user`, `deleted_at`) are not included in the output

-   [x] `player` contains nested `team` structure
