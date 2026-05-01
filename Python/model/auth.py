"""
    Author: Thanvi Ambala
"""
def login(service, username, password):
    """
    Authenticates user using database.
    Returns (success, message, user)
    """

    if not username or not password:
        return False, "Username and password cannot be empty", None

    try:
        user = service.authenticate_user(username, password)

        if user:
            return True, "Login successful", user
        else:
            return False, "Invalid username or password", None

    except Exception as e:
        return False, f"Error during login: {e}", None


def logout():
    """
    Logs the user out.
    """
    return True, "Logged out successfully", None