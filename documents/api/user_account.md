# Endpoints for UserAccount

-   create: `AllowAny`
-   list: `AllowAny`
-   retrieve: `AllowAny`
-   partial_update: `IsAdminUser`
-   delete: `IsSuperUser`
-   other: at least `IsAuthenticated`

prefix: `api/v1/`

-   [x] **POST** `user-accounts/`
        Create a new user

    ```json
    // Input
    {
        "username": "user_name",
        "email": "email@sample.com",
        "password": "HashedPassword123"
    }
    ```

    ```json
    // Output
    {
        "id": "aaa-aaa-aaa",
        "username": "user_name",
        "email": "email@sample.com",
        "created_at": "YYYY-MM-DD"
    }
    ```

-   [x] **GET** `user-accounts/`
        Get all user accounts

    ```json
    // Output (General)
    [
        {
            "id": "aaa-aaa-aaa",
            "username": "user_name",
            "created_at": "YYYY-MM-DD"
        }
    ]
    ```

    ```json
    // Output (Admin)
    [
        {
            "id": "aaa-aaa-aaa",
            "username": "user_name",
            "email": "email@sample.com",
            "is_superuser": "bool",
            "is_staff": "bool",
            "is_active": "bool",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "deleted_at": "YYYY-MM-DD"
        }
    ]
    ```

-   [x] **GET** `user-accounts/{id}/`
        Get the specific user

    ```json
    // Output (General)
    {
        "id": "aaa-aaa-aaa",
        "username": "user_name",
        "created_at": "YYYY-MM-DD"
    }
    ```

    ```json
    // Output (Admin)
    {
        "id": "aaa-aaa-aaa",
        "username": "user_name",
        "email": "email@sample.com",
        "is_superuser": "bool",
        "is_staff": "bool",
        "is_active": "bool",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
    }
    ```

-   [x] **PATCH** `user-accounts/{id}/`
        Change the specific user account information

    ```json
    // Input (Admin)
    {
        "username": "updated_user_name",
        "email": "updated_email@sample.com",
        "is_active": "bool"
    }
    ```

    ```json
    // Output (Admin)
    {
        "id": "aaa-aaa-aaa",
        "username": "updated_user_name",
        "email": "updated_email@sample.com",
        "is_superuser": "bool",
        "is_staff": "bool",
        "is_active": "bool",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD"
    }
    ```

-   [x] **DELETE** `user-accounts/{id}/`
        Delete the specific user account

---

## Endpoint for UserAccountComment

-   list: `AllowAny`
-   retrieve: `AllowAny`
-   partial_update: `IsAdminUser`
-   delete: `IsSuperUser`
-   other: at least `IsAuthenticated`

-   [x] **GET** `user-accounts/{user_pk}/comments/`
        Get the list of comments on the specific user

    ```json
    // Output (General)
    [
        {
            "id": "zzz-zzz-zzz",
            "body": "Comment Body...",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "player": {
                "id": "xxx-xxx-xxx",
                "first_name": "FirstName",
                "last_name": "LastName",
                "team": {
                    "id": "yyy-yyy-yyy",
                    "name": "Team Name"
                }
            }
        }
    ]
    ```

    ```json
    // Output (Admin)
    [
        {
            "id": "zzz-zzz-zzz",
            "body": "Comment Body...",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "deleted_at": "YYYY-MM-DD",
            "player": {
                "id": "xxx-xxx-xxx",
                "first_name": "FirstName",
                "last_name": "LastName",
                "team": {
                    "id": "yyy-yyy-yyy",
                    "name": "Team Name"
                }
            }
        }
    ]
    ```

-   [x] **GET** `user-accounts/{user_pk}/comments/{id}/`
        Get the specific comment on the specific user

    ```json
    // Output (General)
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "player": {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "team": {
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    }
    ```

    ```json
    // Output (Admin)
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD",
        "player": {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "team": {
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    }
    ```

---

# Endpoints for Current UserAccount

-   retrieve: `IsAuthenticated`
-   partial_update: `IsAuthenticated`
-   delete: `IsAuthenticated`
-   other: at least `IsAuthenticated`

-   [x] **GET** `user-accounts/me/`
        Get the current user

    ```json
    // Output
    {
        "id": "aaa-aaa-aaa",
        "username": "user_name",
        "email": "email@sample.com",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD"
    }
    ```

-   [x] **PATCH** `user-accounts/me/`
        Change the current user information

    ```json
    // Input
    {
        "username": "user_name",
        "email": "email@sample.com"
    }
    ```

    ```json
    // Output
    {
        "id": "aaa-aaa-aaa",
        "username": "user_name",
        "email": "email@sample.com",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD"
    }
    ```

-   [x] **DELETE** `user-accounts/me/`
        Delete the current user

---

## Endpoint for UserAccountMeComment

-   retrieve: `IsAuthenticated`
-   partial_update: `IsAuthenticated`
-   delete: `IsAuthenticated`
-   other: at least `IsAuthenticated`

-   [x] **GET** `user-accounts/me/comments/`
        Get the list of comments on the current user

    ```json
    // Output
    [
        {
            "id": "zzz-zzz-zzz",
            "body": "Comment Body...",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "player": {
                "id": "xxx-xxx-xxx",
                "first_name": "FirstName",
                "last_name": "LastName",
                "team": {
                    "id": "yyy-yyy-yyy",
                    "name": "Team Name"
                }
            }
        }
    ]
    ```

-   [x] **GET** `user-accounts/me/comments/{id}/`
        Get the specific comment on the current user

    ```json
    // Output
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "player": {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "team": {
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    }
    ```

-   [x] **PATCH** `user-accounts/me/comments/{id}/`
        Change the specific comment on the current user

    ```json
    // Input
    {
        "body": "Comment Body..."
    }
    ```

    ```json
    // Output
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "player": {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "team": {
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    }
    ```

-   [x] **DELETE** `user-accounts/me/comments/{id}/`
        Delete he specific comment on the current user
