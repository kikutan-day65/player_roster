## PATCH `api/v1/players/{id}/`

### Positive cases

Change the player information

-   [x] status code: 200
-   [x] first_name in response matches "updated_first_name"
-   [x] last_name in response matches "updated_last_name"
-   [x] team_id in response matches changed team_id
-   [x] response is valid format of its serializer

### Negative cases

Cannot change the information of nonexistent player

-   [x] status code: 404

Cannot change the information of player if nonexistent team

-   [x] status code: 400

General user cannot change the information of player

-   [x] status code: 403

Unauthenticated user cannot change the information of player

-   [x] status code: 401

## PATCH `api/v1/teams/{id}/`

### Positive cases

Change the team information

-   [x] status code: 200
-   [x] name in response matches "updated name"
-   [x] sport in response matches "basketball"
-   [x] response is valid format of its serializer

### Negative cases

General user cannot change the information of team

-   [x] status code: 403

Unauthenticated user cannot change the information of team

-   [x] status code: 401

Cannot change the information of nonexistent team

-   [x] status code: 404

Cannot change the information if nonexistent sport

-   [x] status code: 400
