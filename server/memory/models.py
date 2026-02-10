from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class MemoryItem:
    id: str
    content: str
    source: str
    tier: str  # SCRATCH | SESSION | LONGTERM
    created_at: datetime
    trust_score: float
    signature: Optional[str] = None
    expires_at: Optional[datetime] = None

    @staticmethod
    def create(
        content: str,
        source: str,
        tier: str,
        trust_score: float,
        expires_at: Optional[datetime] = None,
    ):
        return MemoryItem(
            id=str(uuid.uuid4()),
            content=content,
            source=source,
            tier=tier,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            trust_score=trust_score,
            signature=None,
        )
