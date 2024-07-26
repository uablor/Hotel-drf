import secrets
import string


def genNumber(length=6):
    alphabet = (string.digits)  # Generate from letters and digits >>>>> string.ascii_letters +
    verification_code = "".join(secrets.choice(alphabet) for _ in range(length))
    return verification_code