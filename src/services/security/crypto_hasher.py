from Crypto.Hash import SHA1

from src.common.dto.transaction import PaymentData, PaymentDataWithSignature
from src.core.settings import SignatureSettings, get_signature_settings


class SignatureHasher:
    def __init__(self, settings: SignatureSettings) -> None:
        self.settings = settings

    def _hash_message(self, message: str | PaymentData | PaymentDataWithSignature):
        return SHA1.new(f"{self.settings.private_key}:{message}".encode())

    def generate(self, data: PaymentData):
        message_hash = self._hash_message(data)
        return message_hash.hexdigest()

    def verify(self, data: PaymentDataWithSignature):
        signature = self._hash_message(data).hexdigest()
        print(data, signature)
        return data.signature == signature


def get_signature_hasher():
    return SignatureHasher(get_signature_settings())
