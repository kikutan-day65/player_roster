# Endpoints for Player

-   create: `IsAdminUser`
-   list: `AllowAny`
-   retrieve: `AllowAny`
-   partial_update: `IsAdminUser`
-   delete: `IsSuperUser`
-   other: at least `IsAuthenticated`

prefix: `api/v1/`

-   [x] **POST** `players/`
        Create a new player

    ```json
    // Input
    {
        "team_id": "yyy-yyy-yyy",
        "first_name": "FirstName",
        "last_name": "LastName"
    }
    ```

    ```json
    // Output
    {
        "id": "xxx-xxx-xxx",
        "first_name": "FirstName",
        "last_name": "LastName",
        "created_at": "YYYY-MM-DD",
        "team": {
            "id": "yyy-yyy-yyy",
            "name": "Team Name"
        }
    }
    ```

-   [x] **GET** `players/`
        Get all players

    ```json
    // Output (General)
    [
        {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "team": {
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    ]
    ```

    ```json
    // Output (Admin)
    [
        {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "deleted_at": "YYYY-MM-DD",
            "team": {
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    ]
    ```

-   [x] **GET** `players/{id}/`
        Get the specific player

    ```json
    // Output (General)
    {
        "id": "xxx-xxx-xxx",
        "first_name": "FirstName",
        "last_name": "LastName",
        "team": {
            "id": "yyy-yyy-yyy",
            "name": "Team Name"
        }
    }
    ```

    ```json
    // Output (Admin)
    {
        "id": "xxx-xxx-xxx",
        "first_name": "FirstName",
        "last_name": "LastName",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD",
        "team": {
            "id": "yyy-yyy-yyy",
            "name": "Team Name"
        }
    }
    ```

-   [x] **PATCH** `players/{id}/`
        Change the specific player information

    ```json
    // Input
    {
        "team_id": "updated-xxx-xxx",
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName"
    }
    ```

    ```json
    // Output
    {
        "id": "xxx-xxx-xxx",
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "team": {
            "id": "yyy-yyy-yyy",
            "name": "Team Name"
        }
    }
    ```

-   [x] **DELETE** `players/{id}/`
        Delete the specific player

---

# Endpoint for PlayerComment

-   list: `AllowAny`

-   [x] **GET** `players/{player_pk}/comments/`
        Get all comments on the specific player

    ```json
    // Output (General)
    [
        {
            "id": "zzz-zzz-zzz",
            "body": "Comment Body...",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "user": {
                "id": "aaa-aaa-aaa",
                "username": "user_name"
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
            "user": {
                "id": "aaa-aaa-aaa",
                "username": "user_name"
            }
        }
    ]
    ```

---

# Endpoints for Team

-   create: `IsAdminUser`
-   list: `AllowAny`
-   retrieve: `AllowAny`
-   partial_update: `IsAdminUser`
-   delete: `IsSuperUser`
-   other: at least `IsAuthenticated`

prefix: `api/v1/`

-   [x] **POST** `teams/`
        Create a new team

    ```json
    // Input
    {
        "name": "Team Name",
        "sport": "Sport Choice"
    }
    ```

    ```json
    // Output
    {
        "id": "yyy-yyy-yyy",
        "name": "Team Name",
        "sport": "Sport Choice",
        "created_at": "YYYY-MM-DD"
    }
    ```

-   [x] **GET** `teams/`
        Get all teams

    ```json
    // Output (General)
    [
        {
            "id": "yyy-yyy-yyy",
            "name": "Team Name",
            "sport": "Sport Choice"
        }
    ]
    ```

    ```json
    // Output (Admin)
    [
        {
            "id": "yyy-yyy-yyy",
            "name": "Team Name",
            "sport": "Sport Choice",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "deleted_at": "YYYY-MM-DD"
        }
    ]
    ```

-   [x] **GET** `teams/{id}/`
        Get the specific team

    ```json
    // Output (General)
    {
        "id": "yyy-yyy-yyy",
        "name": "Team Name",
        "sport": "Sport Choice"
    }
    ```

    ```json
    // Output (Admin)
    {
        "id": "yyy-yyy-yyy",
        "name": "Team Name",
        "sport": "Sport Choice",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
    }
    ```

-   [x] **PATCH** `teams/{id}/`
        Change the specific team information

    ```json
    // Input
    {
        "name": "Updated Team Name",
        "sport": "Updated Sport Choice"
    }
    ```

    ```json
    // Output
    {
        "id": "yyy-yyy-yyy",
        "name": "Updated Team Name",
        "sport": "Updated Sport Choice",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD"
    }
    ```

-   [x] **DELETE** `teams/{id}/`
        Delete the specific team

---

## Endpoint for TeamPlayer

-   list: `AllowAny`

-   [x] **GET** `teams/{team_pk}/players/`
        Get the list of players on the specific team

    ```json
    // Output (General)
    [
        {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName"
        }
    ]
    ```

    ```json
    // Output (Admin)
    [
        {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD",
            "deleted_at": "YYYY-MM-DD"
        }
    ]
    ```

---

# Endpoints for Comment

-   create: `IsAuthenticated`
-   list: `AllowAny`
-   retrieve: `AllowAny`
-   partial_update: `IsAdminUser` or `IsAuthenticatedOwner`
-   delete: `IsSuperUser` or `IsAuthenticatedOwner`
-   other: at least `IsAuthenticated`

-   [x] **POST** `comments/`
        Create a new comment

    ```json
    // Input
    {
        "player_id": "xxx-xxx-xxx",
        "body": "Comment Body..."
    }
    ```

    ```json
    // Output
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
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

-   [x] **GET** `comments/`
        Get the list of all comments

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
            },
            "user": {
                "id": "aaa-aaa-aaa",
                "username": "user_name"
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
            },
            "user": {
                "id": "aaa-aaa-aaa",
                "username": "user_name"
            }
        }
    ]
    ```

-   [x] **GET** `comments/{id}/`
        Get the specific comment

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
        },
        "user": {
            "id": "aaa-aaa-aaa",
            "username": "user_name"
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
        },
        "user": {
            "id": "aaa-aaa-aaa",
            "username": "user_name"
        }
    }
    ```

-   [x] **PATCH** `comments/{id}/`
        Change the information of the specific comment
    ```json
    // Input
    {
        "player_id": "xxx-xxx-xxx",
        "body": "Updated Comment Body..."
    }
    ```
    ```json
    // Output
    {
        "id": "zzz-zzz-zzz",
        "body": "Updated Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "player": {
            "id": "xxx-xxx-xxx",
            "first_name": "FirstName",
            "last_name": "LastName",
            "team": {
                "id": "yyy-yyy-yyy",s
                "name": "Team Name"
            }
        }
    }
    ```
-   [x] **DELETE** `comments/{id}/`
        Delete the specific comment
