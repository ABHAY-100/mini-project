from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict
import uuid
import json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


@dataclass
class MemoryItem:
    id: str
    tier: str
    content: str
    source: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    signature: Optional[bytes] = None

    @staticmethod
    def create(tier, content, source, expires_at=None, signature=None):
        return MemoryItem(
            id=str(uuid.uuid4()),
            tier=tier,
            content=content,
            source=source,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            signature=signature,
        )


class SecureMemory:
    SESSION = "SESSION"
    LONG_TERM = "LONG_TERM"

    def __init__(self, data_dir="data"):
        self._session: Dict[str, MemoryItem] = {}

        self._data_dir = Path(data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._log = self._data_dir / "memory.log"

        self._private_key = Ed25519PrivateKey.generate()
        self._public_key = self._private_key.public_key()

    def write(self, item: MemoryItem):
        if item.tier == self.SESSION:
            self._session[item.id] = item

        elif item.tier == self.LONG_TERM:
            if not item.signature:
                raise ValueError("Unsigned long-term memory rejected")

            record = {
                "id": item.id,
                "content": item.content,
                "source": item.source,
                "created_at": item.created_at.isoformat(),
                "signature": item.signature.hex(),
            }
            with self._log.open("a") as f:
                f.write(json.dumps(record) + "\n")

        else:
            raise ValueError("Invalid memory tier")

    def read(self):
        now = datetime.now(timezone.utc)

        expired = [
            k for k, v in self._session.items() if v.expires_at and v.expires_at <= now
        ]
        for k in expired:
            del self._session[k]

        long_term = []
        if self._log.exists():
            for line in self._log.open():
                r = json.loads(line)
                sig = bytes.fromhex(r["signature"])
                try:
                    self._public_key.verify(sig, r["content"].encode())
                    long_term.append(r["content"])
                except Exception:
                    pass

        return {
            "long_term": long_term,
            "session": [v.content for v in self._session.values()],
        }

    def sign_for_long_term(self, content: str) -> bytes:
        return self._private_key.sign(content.encode())
