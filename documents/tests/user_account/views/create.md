## POST `api/v1/user-accounts/`

### Positive cases

Create a new user successfully.

-   [x] status code: 201
-   [x] username in response matches input username
-   [x] email in response matches input email
-   [x] response is valid format of its serializer

### Negative cases

User account creation fails if username is already taken.

-   [x] status code: 400
-   [x] error for duplicate username

User account creation fails if email is already taken.

-   [x] status code: 400
-   [x] error for duplicate email

User account creation fails if invalid data was sent.
User account creation fails if required fields are empty.

-   [x] status code: 400
-   [x] error when username is empty
-   [x] error when email is empty
-   [x] error when password is empty
