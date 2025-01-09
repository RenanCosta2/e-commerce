from rest_framework_simplejwt.tokens import RefreshToken

class Authentication:
    """
    A helper class for handling user authentication-related tasks.
    """

    @staticmethod
    def get_tokens_for_user(user):
        """
        Generates and returns an access token for the given user.
        
        Args:
            user: The user for whom the access token will be generated.
        
        Returns:
            str: The access token as a string.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    @staticmethod
    def remove_auth(client):
        """
        Removes the authentication credentials from the client.
        
        Args:
            client: The test client from which the authentication credentials will be removed.
        """
        client.credentials()  # Clears the credentials so no token is sent with requests
