from typing import Optional, Union, Any
from cryptography.fernet import Fernet, InvalidToken
from fastapi.exceptions import HTTPException


class DisabledSuite:
    @staticmethod
    def encrypt(_: bytes) -> bytes:
        return b"Unavailable (No Secret Key)"

    @staticmethod
    def decrypt(*_: bytes) -> str:
        return "Unavailable (No Secret Key)"


disabled_suite = DisabledSuite()


class CryptographicSuite:
    def __init__(self, key: bytes, logger: Any) -> None:
        try:
            self.cipher_suite: Union[Fernet, DisabledSuite] = Fernet(key)
        except TypeError:
            self.cipher_suite = disabled_suite
        except ValueError as e:
            if key not in (b"", ""):
                logger.application_log(
                    event=f"Fernet key was provided, but appears to be invalid: {repr(e)}"
                )
                self.cipher_suite = disabled_suite

    def encrypt(self, data: str, key: Optional[str] = None) -> str:
        _local_cipher_suite = self.cipher_suite
        if isinstance(key, str):
            _local_cipher_suite = Fernet(key.encode())
        try:
            encrypted: bytes = _local_cipher_suite.encrypt(data.encode())
        except (InvalidToken, AttributeError):
            # TODO: defer this http error to later, return a normal error here
            raise HTTPException(status_code=400, detail="Encryption failed")
        return encrypted.decode()

    def decrypt(self, data: str, key: Optional[str] = None) -> str:
        _local_cipher_suite = self.cipher_suite
        if key is not None:
            _local_cipher_suite = Fernet(key.encode())
        try:
            decrypted = _local_cipher_suite.decrypt(data.encode())
        except (InvalidToken, AttributeError):
            # TODO: defer this http error to later, return a normal error here
            raise HTTPException(status_code=400, detail="Decryption failed")
        if isinstance(decrypted, bytes):
            return decrypted.decode()
        else:
            return decrypted

    @property
    def key_available(self) -> bool:
        return isinstance(self.cipher_suite, Fernet)


def generate_key() -> str:
    secret: bytes = Fernet.generate_key()
    return secret.decode()
