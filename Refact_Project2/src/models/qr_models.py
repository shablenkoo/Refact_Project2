from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional

@dataclass(frozen=True)
class QRCodeEntity:
    content: str
    qr_type: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    owner_id: Optional[str] = None

@dataclass(frozen=True)
class LogEntry:
    action: str
    qr_id: UUID
    details: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class QRCodeEntity:
    content: str
    qr_type: str
    id: UUID = field(default_factory=uuid4)
    status: str = "AVAILABLE"
    owner: str = "System"