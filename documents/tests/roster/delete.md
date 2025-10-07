## DELETE `api/v1/players/{id}/`

### Positive cases

Super user can delete the specific user

-   [x] status code: 204
-   [x] "deleted_at" of test_user is not None

### Negative cases

Admin user cannot delete the specific user

-   [x] status code: 403

General user cannot delete the specific user

-   [x] status code: 403

Unauthenticated user cannot delete the specific user

-   [x] status code: 401

Cannot delete the nonexistent user

-   [x] status code: 404
