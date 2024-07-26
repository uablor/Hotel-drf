# import jwt
# from rest_framework.request import Request

# # from django.conf import settings
# # from datetime import datetime, timedelta

# # def sign_token(user_id):
# #     payload = {
# #         'userId': user_id,
# #         'exp': datetime.utcnow() + timedelta(days=30)  # Token expires in 30 days
# #     }
# #     return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')

# # def sign_verification_code_token(email, verify_code):
# #     payload = {
# #         'email': email,
# #         'verifyCode': verify_code,
# #         'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
# #     }
# #     return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')

# # def login_token(user_id):
# #     payload = {
# #         'userId': user_id,
# #         'exp': datetime.utcnow() + timedelta(days=365)  # Token expires in 365 days
# #     }
# #     return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256').decode('utf-8')

# # def jwt_verify(token):
# #     try:
# #         decoded_payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
# #         return decoded_payload
# #     except jwt.ExpiredSignatureError:
# #         # Handle token expiration
# #         raise jwt.ExpiredSignatureError('Token expired. Please log in again.')
# #     except jwt.InvalidTokenError:
# #         # Handle invalid token
# #         raise jwt.InvalidTokenError('Invalid token. Please log in again.')


# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# from datetime import datetime, timedelta
# from django.conf import settings
# from rest_framework_simplejwt.authentication import JWTAuthentication


# def sign_token(user_id):
#     access_token = AccessToken.for_user(user_id)
#     return str(access_token)


# def sign_verification_code_token(email, verify_code):
#     token = RefreshToken()
#     token["email"] = email
#     token["verify_code"] = verify_code
#     token["exp"] = datetime.utcnow() + timedelta(hours=1)
#     return str(token)


# def login_token(user_id):
#     access_token = AccessToken.for_user(user_id)
#     return str(access_token)


# def jwt_verify(token):
#     try:
#         jwt_authentication = JWTAuthentication()
#         user, _ = jwt_authentication.authenticate(
#             Request(request=None, headers={"Authorization": f"Bearer {token}"})
#         )
#         return user
#     except jwt.ExpiredSignatureError:
#         raise jwt.ExpiredSignatureError("Token expired. Please log in again.")
#     except jwt.InvalidTokenError:
#         raise jwt.InvalidTokenError("Invalid token. Please log in again.")
