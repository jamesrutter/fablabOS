# Class definition for event table in database
#

from typing import Optional


class Event:
    """
    def __init__(self, event_name: str, event_type: str, date_start: str,
                 date_end: Optional[str] = None, multi_day: Optional[bool] = None,
                 reoccuring: Optional[bool] = None, reoccuring_freq: Optional[str] = None,
                 time_start: Optional[str] = None, time_end: Optional[str] = None,
                 fee_reg: Optional[bool] = None, fee_reg_amount: Optional[float] = None,
                 fee_facilitator: Optional[bool] = None, fee_facilitator_amount: Optional[float] = None,
                 max_cap: Optional[bool] = None, max_participants: Optional[int] = None,
                 min_cap: Optional[bool] = None, min_participants: Optional[int] = None,
                 target_audience: Optional[str] = None, tech_level: Optional[str] = None,
                 reg_url: Optional[str] = None, image_url: Optional[str] = None):
        self.event_name = event_name
        self.event_type = event_type
        self.date_start = date_start
        self.date_end = date_end
        self.multi_day = multi_day
        self.reoccuring = reoccuring
        self.reoccuring_freq = reoccuring_freq
        self.time_start = time_start
        self.time_end = time_end
        self.fee_reg = fee_reg
        self.fee_reg_amount = fee_reg_amount
        self.fee_facilitator = fee_facilitator
        self.fee_facilitator_amount = fee_facilitator_amount
        self.max_cap = max_cap
        self.max_participants = max_participants
        self.min_cap = min_cap
        self.min_participants = min_participants
        self.target_audience = target_audience
        self.tech_level = tech_level
        self.reg_url = reg_url
        self.image_url = image_url

    # Additional methods for database interaction can be added here
    # For example, methods to save the event to the database
    def save(self):
        pass

    def update(self):
        pass

new_event = Event()