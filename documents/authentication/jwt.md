# JWT Authentication

## Flow

1. The client sends a request to the server with a username and password.
2. The server issues a JWT and returns it to the client.
3. The client stores the token (e.g., in a cookie or local storage).
4. The client sends requests with the token included in the Authorization header.
5. The server validates the token and accepts the request if it is valid.
6. Repeat step 4 until the access token expires.

## Notes

-   The client is authenticated as long as the access token is valid.
-   If the access token has expired but the refresh token is still valid, the client can use the refresh token to obtain a new access token.
-   If both the access token and refresh token are expired, the client must log in again with a username and password to obtain a new JWT.

## Token Expiration

The default SimpleJWT token lifetimes are highly security-oriented and may not suit typical web applications. For this project, I adjusted them to balance security and usability:

-   **Access token:** 15 minutes
-   **Refresh token:** 7 days
