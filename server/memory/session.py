from typing import List
from datetime import datetime
from .models import MemoryItem
import logging


class SessionMemory:
    def __init__(self):
        self._items: List[MemoryItem] = []
        logging.debug("SessionMemory initialized")

    def add(self, item: MemoryItem):
        if item.tier != "SESSION":
            raise ValueError("Only session items allowed")
        if item.expires_at is None or item.expires_at < datetime.utcnow():
            raise ValueError("Item is expired or not set")
        self._items.append(item)
        logging.debug(f"Added session item: {item}")

    def get_active(self) -> List[MemoryItem]:
        now = datetime.utcnow()
        logging.debug("Getting active session items")
        return [
            item
            for item in self._items
            if item.expires_at is None or item.expires_at > now
        ]

    def purge_expired(self):
        now = datetime.utcnow()
        self._items = [
            item
            for item in self._items
            if item.expires_at is None or item.expires_at > now
        ]
        logging.debug("Purged expired session items")
