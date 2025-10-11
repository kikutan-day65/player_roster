## PATCH `api/v1/user-accounts/{id}/`

### Positive cases

Admin user can manipulate the information of the user

-   [x] status code: 200
-   [x] "username" in the response is "updated_username"
-   [x] "email" in the response is "updated_email@example.com"
-   [x] response is valid format of its serializer

### Negative cases

General user cannot manipulate the information of the user via this endpoint

-   [x] status code: 403

Unauthenticated user cannot manipulate the information of the user via this endpoint

-   [x] status code: 401

Cannot manipulate the information of nonexistent user

-   [x] status code: 404

## PATCH `api/v1/user-accounts/me/`

## Positive cases

Authenticated user can change the information of the current user

-   [x] status code: 200
-   [x] "username" in response is "updated_username"
-   [x] "email" in the response is "updated_email@example.com"
-   [x] response is valid format of its serializer

## Negative cases

Unauthenticated user can change the information of the current user

-   [x] status code: 401
