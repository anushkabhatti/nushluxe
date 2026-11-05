from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import uuid4

from utils.dates import calculate_next_due_date, get_status


@dataclass
class Routine:
    service: str
    last_completed: date
    frequency_weeks: int

    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )

    @property
    def next_due(self):
        return calculate_next_due_date(
            self.last_completed,
            self.frequency_weeks
        )

    @property
    def status(self):
        return get_status(self.next_due)

    def update(
        self,
        service=None,
        last_completed=None,
        frequency_weeks=None
    ):
        if service is not None:
            self.service = service.strip().title()

        if last_completed is not None:
            self.last_completed = last_completed

        if frequency_weeks is not None:
            self.frequency_weeks = frequency_weeks

        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "id": self.id,
            "service": self.service.title(),
            "last_completed": self.last_completed.isoformat(),
            "frequency_weeks": self.frequency_weeks,
            "next_due": self.next_due.isoformat(),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
