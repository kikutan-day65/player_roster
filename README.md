# player_roster

日本語バージョンは[こちら](README_JP.md)

## Test Policy

For test cases, see [here](documents/tests/).

-   **Models**  
    Model tests focus on verifying the correctness of model attributes and methods. They do not involve API requests or endpoint behavior, since those are tested at the serializer and view levels.

-   **Serializers**  
    Serializer tests focus on verifying the correctness of data transformation between model instances and primitive data types (e.g., dictionaries or lists). They also ensure that validation logic works as expected during deserialization. They do not check authentication or permissions, since those are the responsibility of view tests.

-   **Views**  
    View tests focus on verifying the correctness of API behavior through actual HTTP requests and responses. They ensure that authentication, permissions, routing, and serializer integration work together as expected. These are considered more like integration tests than unit tests.

## JWT Authentication

-   The client remains authenticated as long as the access token is valid.
-   If the access token expires but the refresh token is still valid, the client can use it to obtain a new access token.
-   If both tokens expire, the client must log in again with a username and password to obtain a new JWT.

## Token Expiration

The default SimpleJWT token lifetimes are highly security-oriented and may not suit typical web applications. For this project, I adjusted them to balance security and usability:

-   **Access token:** 15 minutes
-   **Refresh token:** 7 days
