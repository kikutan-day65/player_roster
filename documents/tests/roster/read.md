## GET `api/v1/players/`

### Positive cases

Authenticated or unauthenticated users can get the list of all players in the public format

-   [x] status code: 200
-   [x] response list length is 2
-   [x] response is valid format of its serializer

Admin or super users can get the list of all players in the administrator format

-   [x] status code: 200
-   [x] response list length is 2
-   [x] response is valid format of its serializer

## GET `api/v1/players/{id}/`

### Positive cases

Authenticated or unauthenticated users can get the specific players in the public format

-   [x] status code: 200
-   [x] response is valid format of its serializer

Admin or super users can get the specific players in the public format

-   [x] status code: 200
-   [x] response is valid format of its serializer

Cannot get non-existent player

-   [x] status code: 404
