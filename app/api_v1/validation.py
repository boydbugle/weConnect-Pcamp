import re


def validate_email(email):
    if len(email) != 0:
        if re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)", email):
            return True
        return False
