from enum import Enum

class UserRole(str, Enum):
    EXAMINER = "examiner"
    WEB_ADMIN = "web_admin"
    REPORT_ADMIN = "report_admin"
