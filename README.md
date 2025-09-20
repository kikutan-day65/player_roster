# player_roster

## JWT Authentication

-   The client is authenticated as long as the access token is valid.
-   If the access token has expired but the refresh token is still valid, the client can use the refresh token to obtain a new access token.
-   If both the access token and refresh token are expired, the client must log in again with a username and password to obtain a new JWT.

## Token Expiration

The default SimpleJWT token lifetimes are highly security-oriented and may not be ideal for typical web services.  
For this project, I updated them as follows to balance security and usability:

-   Access token: 15 minutes
-   Refresh token: 7 days
