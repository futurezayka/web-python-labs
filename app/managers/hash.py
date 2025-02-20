from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashManager:
    def __init__(self):
        self._context = pwd_context

    def verify_hash(self, plain_value: str, hashed_value: str) -> bool:
        return self._context.verify(plain_value, hashed_value)

    def get_hash(self, value: str) -> str:
        return self._context.hash(value)


hash_manager = HashManager()
