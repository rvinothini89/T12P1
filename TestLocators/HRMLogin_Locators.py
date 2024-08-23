class locators:
    # Locators for the login page
    loc_username = "//input[@name='username']"  # Username input field
    loc_password = "//input[@name='password']"  # Password input field
    loc_login = "//button[text()=' Login ']"  # Login button
    loc_error = "//p[@class = 'oxd-text oxd-text--p oxd-alert-content-text']"  # Error message for login failures
