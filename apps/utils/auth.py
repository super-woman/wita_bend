"""Module for token validation"""

from base64 import b64decode

import jwt
from flask import current_app, request

from ..constants.errors import jwt_errors
from .handled_errors import BaseModelValidationError


class Auth:
    """ This class will house Authentication and Authorization Methods """

    """ Routes The Authentication Header Should  Not Be Applied Ignore"""
    authentication_header_ignore = [
        "/docs",
        "/apidocs",
        "/apispec_1.json",
    ]

    @staticmethod
    def check_token():
        if request.method != "OPTIONS":

            for endpoint in Auth.authentication_header_ignore:
                # If endpoint in request.path, ignore this check
                if endpoint in request.path:
                    return None

            token = Auth.get_token()
            current_app.user = Auth.decode_token(token)

    @staticmethod
    def _get_jwt_public_key():
        def decode_public_key(key_64):
            return b64decode(key_64).decode("utf-8")

        public_key_mapper = {
            "testing": lambda key_64: key_64,
            "development": decode_public_key,
            "production": decode_public_key,
            "staging": decode_public_key,
        }

        app_env = current_app.config.get("APP_ENV", "production")
        public_key_64 = current_app.config.get("JWT_PUBLIC_KEY")

        public_key = public_key_mapper.get(app_env, decode_public_key)(
            public_key_64
        )

        return public_key

    @staticmethod
    def get_token(request=request):
        """Get token from request object

        Args:
            request (HTTPRequest): Http request object

        Returns:
            token (string): Token string

        Raises:
            ValidationError: Validation error raised when there is no token
                            or bearer keyword in authorization header
        """
        token = request.headers.get("Authorization")
        if not token:
            raise BaseModelValidationError(jwt_errors["NO_TOKEN"], 401)
        elif "bearer" not in token.lower():
            raise BaseModelValidationError(jwt_errors["NO_BEARER_MSG"], 401)
        token = token.split(" ")[-1]
        return token

    @staticmethod
    def decode_token(token):

        public_key = Auth._get_jwt_public_key()

        try:
            decoded = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience="wita.com",
                issuer="accounts.wita.com",
                options={"verify_signature": True, "verify_exp": True},
            )
            return decoded

        except (
            ValueError,
            TypeError,
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidSignatureError,
            jwt.InvalidAlgorithmError,
            jwt.InvalidIssuerError,
        ) as error:
            exception_mapper = {
                ValueError: (jwt_errors["SERVER_ERROR_MESSAGE"], 500),
                TypeError: (jwt_errors["SERVER_ERROR_MESSAGE"], 500),
                jwt.ExpiredSignatureError: (
                    jwt_errors["EXPIRED_TOKEN_MSG"],
                    401,
                ),
                jwt.DecodeError: (jwt_errors["INVALID_TOKEN_MSG"], 401),
                jwt.InvalidIssuerError: (jwt_errors["ISSUER_ERROR"], 401),
                jwt.InvalidAlgorithmError: (
                    jwt_errors["ALGORITHM_ERROR"],
                    401,
                ),
                jwt.InvalidSignatureError: (
                    jwt_errors["SIGNATURE_ERROR"],
                    500,
                ),
            }
            message, status_code = exception_mapper.get(
                type(error), (jwt_errors["SERVER_ERROR_MESSAGE"], 500)
            )
            raise BaseModelValidationError(message, status_code)
