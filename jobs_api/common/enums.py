from enum import Enum


class Role(str, Enum):
    applicant = "applicant"
    employer = "employer"


class Education(str, Enum):
    basic = "basic"
    secondary_general = "secondary_general"
    secondary_vocational = "secondary_vocational"
    high = "high"
