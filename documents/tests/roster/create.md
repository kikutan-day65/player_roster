## POST `api/v1/players/`

### Positive cases

Create a new player successfully.

-   [x] status code: 201
-   [x] `first_name` in response matches input `first_name`
-   [x] `last_name` in response matches input `last_name`
-   [x] `team.id `in response matches input `team_id`
-   [x] response is valid format of its serializer

### Negative cases

General user cannot create a new player

-   [x] status code: 403

Unauthenticated user cannot create a new player

-   [x] status code: 401

Player creation fails when required fields are empty

-   [x] status code: 400
-   [x] error when first_name is empty
-   [x] error when last_name is empty
-   [x] error when team_id is empty
