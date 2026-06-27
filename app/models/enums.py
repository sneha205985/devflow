import enum


class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"
    viewer = "viewer"


class IssueStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    done = "done"


class IssuePriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class InviteStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    expired = "expired"
