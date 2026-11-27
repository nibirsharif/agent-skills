"""The records the helpdesk keeps."""

import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class User:
    email: str
    name: str
    is_agent: bool = False


@dataclasses.dataclass(frozen=True)
class Team:
    name: str
    lead: User
    on_call_manager: User


@dataclasses.dataclass
class Reply:
    author: User
    body: str
    at: datetime.datetime


@dataclasses.dataclass
class Ticket:
    id: int
    subject: str
    requester: User
    team: Team
    created_at: datetime.datetime
    priority: str = "normal"
    status: str = "open"
    assignee: object = None
    replies: list = dataclasses.field(default_factory=list)
    flags: set = dataclasses.field(default_factory=set)
    escalated_at: object = None
    closed_at: object = None

    def last_agent_reply(self):
        """When an agent last replied, or None when none has."""
        times = [reply.at for reply in self.replies if reply.author.is_agent]
        return max(times) if times else None
