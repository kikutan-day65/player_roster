# Test for TeamNestedSerializer

## Positive cases

### 1. Success to serialize team instance

-   [x] Expected fields (`id`, `name`) are included in the output
-   [x] Unexpected fields (`sport`, `created_at`, `updated_at`, `deleted_at`) are not included in the output

# Test for PlayerNestedSerializer

## Positive cases

### 1. Success to serialize player instance

-   [x] Expected fields (`id`, `first_name`, `last_name`, `team`) are included in the output
-   [x] Unexpected fields (`created_at`, `updated_at`, `deleted_at`) are not included in the output

# Test for UserAccountNestedSerializer

## Positive cases

### 1. Success to serialize user instance

-   [x] Expected fields (`id`, `username`) are included in the output
-   [x] Unexpected fields (`password`, `email`, `is_superuser`, `is_staff`, `is_active`, `created_at`, `updated_at`, `deleted_at`) are not included in the output
