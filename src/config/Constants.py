class Auth:
    # google configuration
    CLIENT_ID = ('426873815489-l427cabp034lrjorfqvg97dsfpqn25ha.apps.googleusercontent.com')
    CLIENT_SECRET = 'nFXvZhSxuA4HveponEQ9b-9Y'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    GOOGLE_ISS = 'https://accounts.google.com'
    # facebook configuration
    FACEBOOK_DISCOVERY_URL = (
        "https://www.facebook.com/.well-known/openid-configuration/"
    )
    FACEBOOK_PROPERTY = 'https://graph.facebook.com/me?fields=id,name,email,picture{url}'
    FACEBOOK_SECRET = 'cb34fa1bfd2832322d34f4c7941a00bb'
    FACEBOOK_CLIENT_ID = '158009869795144'
    FACEBOOK_TOKEN_ENDPOINT = 'https://graph.facebook.com/oauth/access_token'
    FACEBOOK_USER_ENDPOINT = 'https://graph.facebook.com/me?fields=id,name,email,picture'
    FACEBOOK_VERIFY = 'https://graph.facebook.com/debug_token'


class AccountType:
    FacebookType = 1
    GoogleType = 2


class ErrorCode:
    NotFound = 404
    Success = 200
    Created = 201
    InternalServerError = 500
    Unauthorized = 401
    InvalidRequestData = 1000
    NotFilledInformation = 1001


class ErrorMessage:
    NotFound = "Not Found Data"
    Success = "Success"
    Created = "Created"
    InternalServerError = "Internal Server Error"
    Unauthorized = "Unauthorized"
    InvalidRequestData = "Invalid Request Data. You must pass enough data"
    NotFilledInformation = "You do not fill name, mobile or occupation"


class UserRole:
    Admin = 1
    Member = 2
