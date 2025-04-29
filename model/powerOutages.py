from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    _id: int
    _nerc_id: int
    _customers_affected: int
    _date_event_began: datetime
    _date_event_finished: datetime

    # def __post_init__(self):
    #     self._hours_of_disservice: float = (self._date_event_finished - self._date_event_began).total_seconds() / 3600

    @property
    def id(self):
        return self._id

    @property
    def nerc_id(self):
        return self._nerc_id

    @property
    def customers_affected(self):
        return self._customers_affected

    @property
    def date_event_began(self):
        return self._date_event_began

    @property
    def date_event_finished(self):
        return self._date_event_finished

    @property
    def hours_of_disservice(self):
        return (self._date_event_finished - self._date_event_began).total_seconds() / 3600

    def __str__(self):
        return (f"id={self._id}, customers_affected={self._customers_affected} "
                f"start_time={self._date_event_began}, end_time= {self._date_event_finished}")

    def __repr__(self):
        return f"id={self.id}, year={self.date_event_began.year}, duration={self.hours_of_disservice:.2f}h"

    def __hash__(self):
        return hash(self._id)

