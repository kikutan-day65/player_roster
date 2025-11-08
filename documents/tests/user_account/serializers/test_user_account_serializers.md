# Test for UserAccountCreateSerializer

### Positive cases

Success to validate and save a user

-   [x] Validation is successful
-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

-   [x] `username` in the output matches the input `username`
-   [x] `email` in the output matches the input `email`

-   [x] `password` is stores in a hashed form

Success to ignore the read-only fields

-   [x] Validation is successful
-   [x] `id` is not in `validated_data`
-   [x] `created_at` is not in `validated_data`

### Negative cases

Fails to validate without the required fields

-   [x] Validation fails if `username` is missing
-   [x] Validation fails if `email` is missing
-   [x] Validation fails if `password` is missing

---

# Test for UserAccountListRetrievePublicSerializer

## Positive cases

Success to serialize user data for public

-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

-   [x] `id` in the output matches that of the input instance
-   [x] `username` in the output matches that of the input instance

---

# Test for UserAccountListRetrieveAdminSerializer

## Positive cases

Success to serialize user data for admin

-   [x] Output structure includes the expected fields

-   [x] `id` in the output matches that of the input instance
-   [x] `username` in the output matches that of the input instance
-   [x] `email` in the output matches that of the input instance
-   [x] `is_superuser` in the output matches that of the input instance
-   [x] `is_staff` in the output matches that of the input instance
-   [x] `is_active` in the output matches that of the input instance

---

# Test for UserAccountPatchSerializer

## Positive cases

Success to validate and save with single field

-   [x] Validation is successful
-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

-   [x] `username` in the output matches that of input data
-   [x] `email` in the output matches that of input data
-   [x] `is_active` in the output matches that of input data

Success to validate and save with all fields

-   [x] Validation is successful
-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

Success to ignore the read-only fields

-   [x] Validation is successful
-   [x] The ignored fields is not in `validated_data`

---

# Test for UserAccountCommentListRetrievePublicSerializer

## Positive cases

Success to serialize comment data on user for public

**comment output**

-   [x] Comment output structure includes expected fields
-   [x] Comment output structure excludes unexpected fields

-   [x] `id` in the comment output matches that of the input data
-   [x] `body` in the comment output matches that of the input data

**nested player output**

-   [x] Nested player output structure includes expected fields
-   [x] Nested player output structure excludes unexpected fields

**nested team output**

-   [x] Nested team output structure includes expected fields
-   [x] Nested team output structure excludes unexpected fields

---

# Test for UserAccountCommentListRetrieveAdminSerializer

## Positive case

Success to serialize comment data on user for admin

**comment output**

-   [x] Comment output structure includes the expected fields
-   [x] Comment output structure excludes the unexpected fields

-   [x] `id` in the comment output matches that of the input data
-   [x] `body` in the comment output matches that of the input data

**nested player output**

-   [x] Nested player output structure includes the expected fields
-   [x] Nested player output structure excludes the unexpected fields

**nested team output**

-   [x] Nested team output structure includes the expected fields
-   [x] Nested team output structure excludes the unexpected fields

---

# Test for MeRetrieveSerializer

## Positive case

Success to serialize current user

-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

-   [x] `id` in the output matches that of the input instance
-   [x] `username` in the output matches that of input instance
-   [x] `email` in the output matches that of input instance

<!-- このシリアライザの見直し！！！ -->

# Test for MePatchSerializer

## Positive case

Success to validate and save with single field

-   [x] Validation is successful
-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

-   [x] `username` in the output matches that of the input data
-   [x] `email` in the output matches that of the input data

Success to validate and save with all fields

-   [x] Validation is successful
-   [x] Output structure includes the expected fields
-   [x] Output structure excludes the unexpected fields

-   [x] `username` in the output matches that of the input data
-   [x] `email` in the output matches that of the input data

Success to ignore the read-only fields

-   [x] Validation is successful
-   [x] The ignored field is not in `validated_data`

# Test for MeCommentListRetrieveSerializer

## Positive case

**comment data**

-   [x] Comment output structure includes the expected fields
-   [x] Comment output structure excludes the unexpected fields

-   [x] `id` in comment output matches the input data
-   [x] `body` in comment output matches the input data

**nested player output**

-   [x] Nested player output structure includes expected fields
-   [x] Nested player output structure excludes unexpected fields

**nested team output**

-   [x] Nested team output structure includes expected fields
-   [x] Nested team output structure excludes unexpected fields

# Test for MeCommentPatchSerializer

## Positive case

Success to validate and save with single field

-   [] Validation is successful

**comment data**

-   [x] Comment output structure includes the expected fields
-   [x] Comment output structure excludes the unexpected fields

-   [x] `id` in comment output matches the input data
-   [x] `body` in comment output matches the input data

**nested player output**

-   [x] Nested player output structure includes expected fields
-   [x] Nested player output structure excludes unexpected fields

**nested team output**

-   [x] Nested team output structure includes expected fields
-   [x] Nested team output structure excludes unexpected fields

Success to ignore the read-only fields

-   [x] Validation is successful
-   [x] The ignored field is not in `validated_data`
