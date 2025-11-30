from enum import Enum

class NetworkTypes(str, Enum):
    VIZA = "VIZA"
    MAZTERCARDZ = "MAZTERCARDZ"

class CardStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"

class AccountStatus(str, Enum):
    ACTIVE = "active"
    IN_DELETION = "in deletion"
    DELETED = "deleted"