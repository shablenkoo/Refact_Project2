from typing import List
from src.core.interfaces import IObserver
from src.models.qr_models import LogEntry

class HistoryLogger(IObserver):
    def __init__(self):
        self.logs: List[LogEntry] = []

    def update(self, event_type: str, data: LogEntry):
        self.logs.append(data)

class AnalyticsEngine(IObserver):
    def __init__(self):
        self.stats = {"CREATED": 0, "SCANNED": 0}

    def update(self, event_type: str, data: LogEntry):
        if event_type in self.stats:
            self.stats[event_type] += 1