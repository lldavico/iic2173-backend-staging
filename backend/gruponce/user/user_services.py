from gruponce.models import User
from django.conf import settings


def verify_user_exists(user_tuple, is_registered=True):
    """Verify if user exist. Receives a tuple with the parameter to verify and the value of it
    PARAMS:
        - user_tuple (tuple[<field>, <value>]): Field corresponds to the param of evaluation, and
            value corresponds to that field value
    """
    if user_tuple[0] == "id":
        print("---Verifying by ID")
        return User.objects.filter(id=user_tuple[1])
    elif user_tuple[0] == "email":
        print("---Verifying by EMAIL")
        return User.objects.filter(email=user_tuple[1], is_registered=is_registered)
    elif user_tuple[0] == "username":
        print("---Verifying by USERNAME")
        return User.objects.filter(username=user_tuple[1], is_registered=is_registered)
    else:
        print("Invalid input")
        return False


def create_user(first_name, last_name, email, username, password):
    """Creates user instance with the given parameters"""

    # TODO: Validate input to avoid SQL Injection
    try:

        if verify_user_exists(("email", email)) or verify_user_exists(("username", username)):
            print("User already exists")
            raise Exception(409)

        user_inst = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            is_registered=True
        )
        return user_inst.get_attr()

    except Exception as e:
        print(e)
        return False, e.args[0]
