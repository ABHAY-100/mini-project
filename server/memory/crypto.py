from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from .models import MemoryItem
import logging


def generate_keypair():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    logging.debug("Generated keypair")
    return private_key, public_key


def _payload(item: MemoryItem) -> bytes:
    logging.debug(f"Creating payload for item: {item}")
    return (
        f"{item.id}|{item.content}|{item.source}|{item.created_at.isoformat()}".encode()
    )


def sign_item(item: MemoryItem, private_key: Ed25519PrivateKey):
    signature = private_key.sign(_payload(item))
    item.signature = signature.hex()
    logging.debug(f"Signed item: {item}")
    return item


def verify_item(item: MemoryItem, public_key: Ed25519PublicKey) -> bool:
    if item.signature is None:
        logging.warning(f"Item has no signature: {item}")
        return False
    try:
        public_key.verify(bytes.fromhex(item.signature), _payload(item))
        logging.debug(f"Verified item: {item}")
        return True
    except Exception:
        logging.error(f"Failed to verify item: {item}")
        return False
