## DELETE `api/v1/user-accounts/{id}/`

### Positive cases

Super user can delete the specific user

-   [x] status code: 204
-   [x] "deleted_at" of test_user is not None

### Negative cases

Admin user cannot delete the specific user

-   [x] status code: 403

Authenticated user cannot delete the specific user

-   [x] status code: 403

Unauthenticated user cannot delete the specific user

-   [x] status code: 401

Cannot delete the nonexistent user

-   [x] status code: 404

## DELETE `api/v1/user-accounts/me/`

### Positive cases

Authenticated user can delete the current user

-   [x] status code: 204
-   [x] "deleted_at" of test_user is not None

### Negative cases

Unauthenticated user can delete the current user

-   [x] status code: 401
