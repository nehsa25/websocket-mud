# auth.py
import base64
import secrets
import datetime
import jwt

from dontcheckin import Secrets


class AuthService:
    SECRET_KEY = Secrets.JWT_SECRET

    @staticmethod
    def generate_token(
        username,
    ):
        payload = {
            "username": username.lower(),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365),  # Token expiration
        }
        token = jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def validate_token(token):
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=["HS256"])
            if payload["exp"] < datetime.datetime.now(datetime.timezone.utc):
                return False
            else:
                return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return False
        except jwt.DecodeError as e:
            print(f"Decode error: {e}")
            return False

    @staticmethod
    def generate_secret_key(length=32):
        secret_bytes = secrets.token_bytes(length)
        secret_key = base64.urlsafe_b64encode(secret_bytes).decode("utf-8")

        return secret_key


if __name__ == "__main__":
    # Generate a 256-bit secret key (32 bytes)
    key = AuthService.generate_secret_key()
    print("Generated Secret Key:", key)
