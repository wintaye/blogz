def email_check(email):
    email = str(email)
    if "@" not in email or "." not in email:
        return False
    elif email.count('@') > 1 or email.count(".") > 1:
        return False
    elif " " in email:
        return False
    elif len(email) < 3 or len(email) > 20:
        return False
    else: 
        return True

def verify_check(password, verify_password):
    if password != verify_password:
        return False
    else: 
        return True

def password_check(password):
    password = str(password)
    if " " in password:
        return False
    elif len(password) < 3 or len(password) > 20:
        return False
    else:
        return True 

def username_check(user, password, verify_password):
    user = str(user)    
    password = str(password)
    verify_password = str(verify_password)
    if len(user) < 1 or len(password) < 1 or len(verify_password) < 1:
        return False
    else: 
        return True
        
def user_is_valid(user, password, verify_password, email):
    # check = ''
    # password_error = ''
    # email_error = ''
    # blank_error = ''
    # password_error_2 = ''
    # verify_password_error = ''
    # email_error = ''
    
    if not verify_check(password, verify_password):
            verify_password_error = 'Your entered passwords do not match.'

    if not password_check(password):
            password_error = 'Password error. Please check that your password is between 3-20 characters and contains no spaces.'

    if not email_check(email):
            email_error = 'Email error. Check that email address contains (1) @ symbol, (1) . and is between 3-20 characters long.'

    if not username_check(user, password, verify_password):
            blank_error = 'Make sure you do not leave any mandatory fields blank.'

    if not email_error and not password_error and not verify_password_error and not blank_error:
        return True