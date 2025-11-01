## GET `api/v1/user-accounts/`

### Positive cases

Admin user can get the list of all users

-   [x] status code: 200
-   [x] response list length is 3
-   [x] response is valid format of its serializer

### Negative cases

General users cannot get the list of all users

-   [x] status code: 403

Unauthenticated user cannot get the list of all users

-   [x] status code: 401

## GET `api/v1/user-accounts/{id}`

### Positive cases

Admin users can get the information of the specific user

-   [x] status code: 200
-   [x] response is valid format of its serializer

Authenticated users can get the information of the specific user

-   [x] status code: 200
-   [x] response is valid format of its serializer

### Negative cases

Unauthenticated user cannot get the information of the specific user

-   [x] status code: 401

Cannot get the information of nonexistent user

-   [x] status code: 404

## GET `api/v1/user-accounts/me/`

## Positive cases

Authenticated user can get the current user

-   [x] status code: 200
-   [x] "username" in response is "username" of request user
-   [x] "email" in response is "email" of request user
-   [x] response is valid format of its serializer

## Negative cases

Unauthenticated user cannot get the current user

-   [x] status code: 401
