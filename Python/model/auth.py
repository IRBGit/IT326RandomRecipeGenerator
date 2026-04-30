"""
    Author: Thanvi Ambala
"""
def login(username, password):
    """
    Checks if the user entered valid login information.
    Later, this will connect to the database.
    """

    if username == "" or password == "":
        return False, "Username and password cannot be empty"

    # temporary login check for now
    if username == "test" and password == "1234":
        return True, "Login successful"

    return False, "Invalid username or password"


def logout():
    """
    Logs the user out.
    """

    return "Logged out successfully"