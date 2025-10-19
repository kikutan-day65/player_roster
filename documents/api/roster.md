# Endpoints for Player

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
        },
        "comments": [
            {
                "id": "zzz-zzz-zzz",
                "body": "Comment Body...",
                "created_at": "YYYY-MM-DD",
                "user": {
                    "id": "aaa-aaa-aaa",
                    "username": "user_name"
                }
            }
        ]
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
        },
        "comments": [
            {
                "id": "zzz-zzz-zzz",
                "body": "Comment Body...",
                "created_at": "YYYY-MM-DD",
                "user": {
                    "id": "aaa-aaa-aaa",
                    "username": "user_name"
                }
            }
        ]
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

-   [x] **POST** `players/{id}/comments/`
        Create a new comment on the specific player

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

-   [x] **GET** `players/{id}/comments/`
        Get all comments on the specific player

    ```json
    // Output (General)
    [
        {
            "id": "zzz-zzz-zzz",
            "body": "Comment Body...",
            "created_at": "YYYY-MM-DD",
            "updated_at": "YYYY-MM-DD"
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
            "deleted_at": "YYYY-MM-DD"
        }
    ]
    ```

-   [x] **GET** `players/{id}/comments/{id}/`
        Get the specific comment on the specific player

    ```json
    // Output (General)
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD"
    }
    ```

    ```json
    // Output (Admin)
    {
        "id": "zzz-zzz-zzz",
        "body": "Comment Body...",
        "created_at": "YYYY-MM-DD",
        "updated_at": "YYYY-MM-DD",
        "deleted_at": "YYYY-MM-DD"
    }
    ```

-   [x] **PATCH** `players/{id}/comments/{id}/`
        Change the specific comment on the specific player

    ```json
    // Input
    {
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
                "id": "yyy-yyy-yyy",
                "name": "Team Name"
            }
        }
    }
    ```

-   [x] **DELETE** `players/{id}/comments/{id}/`
        Delete the specific comment on the specific player

# Endpoints for Team

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

-   [x] **POST** `teams/{id}/players/`
        Create a new player on the specific team

    ```json
    // Input
    {
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

-   [x] **GET** `teams/{id}/players/`
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

-   [x] **GET** `teams/{id}/players/{id}/`
        Get the specific player on the specific team

    ```json
    // Output (General)
    {
        "id": "xxx-xxx-xxx",
        "first_name": "FirstName",
        "last_name": "LastName"
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
        "deleted_at": "YYYY-MM-DD"
    }
    ```

-   [x] **PATCH** `teams/{id}/players/{id}/`
        Change the specific player information on the specific team

    ```json
    // Input
    {
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

-   [x] **DELETE** `teams/{id}/players/{id}/`
        Delete the specific player on the specific team

# Endpoints for Comment

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
        "body": "Comment Body...",
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
