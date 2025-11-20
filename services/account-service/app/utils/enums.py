from enum import Enum

class NetworkTypes(str, Enum):
    VIZA = "VIZA"
    MAZTER = "MAZTERCARDZ"

class CardStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"

class AccountStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"