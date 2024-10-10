AUTH_RESPONCE = (
    "Returns an access JWT token and sets a refresh token in the user's cookies."
)
AUTH_DESCRIPTION = "This endpoint handles user login by verifying the user's login, password, and fingerprint (device information for identification). Upon successful authentication, an access JWT token is returned, and a refresh token is stored in the user's cookies."
AUTH_SUMMARY = "User login with fingerprint."

REFRESH_RESPONCE = (
    "Returns a new access JWT token and sets a new refresh token in the user's cookies."
)
REFRESH_DESCRIPTION = "This endpoint refreshes the user's tokens by validating the fingerprint (device information for identification). It generates a new access JWT token and updates the refresh token in the user's cookies."
REFRESH_SUMMARY = "Refresh user tokens with fingerprint."

LOGOUT_RESPONCE = "Returns an 'ok' status upon successful logout."
LOGOUT_DESCRIPTION = "This endpoint logs out the user by removing the refresh token from the cookies. Upon successful logout, it returns an 'ok' status indicating the operation was successful."
LOGOUT_SUMMARY = "User logout."
