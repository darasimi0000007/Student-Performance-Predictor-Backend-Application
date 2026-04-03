from pydantic import BaseModel
from typing import Optional
from enum import Enum


class SexType(str, Enum):
    female ="F"
    male = "M"


class addressType(str, Enum):
    urban = "U"
    rural = "R"

class famSize(str, Enum):
    greater_than_three = "GT3"
    less_than_three = "LE3"

class pStatus(str, Enum):
    living_together = "T"
    living_apart = "A"

class mEdu(int, Enum):
    no_education = 0
    primary_education = 1
    fifth_to_9th_grade = 2
    secondary_education = 3
    higher_education = 4


class fEdu(int, Enum):
    no_education = 0
    primary_education = 1
    fifth_to_9th_grade = 2
    secondary_education = 3
    higher_education = 4


class mJob(int, Enum):
    at_home = 0
    health = 1
    services = 3
    teacher = 4
    other = 2

class fJob(int, Enum):
    at_home = 0
    health = 1
    services = 3
    teacher = 4
    other = 2



class reason(int, Enum):
    course = 0
    home = 1
    other = 2
    reputation = 3

class guardian(int, Enum):
    father = 0
    mother = 1


class travel_time(int, Enum):
    less_than_15_minutes = 1
    between_15_and_30_minutes = 2
    between_30_minutes_and_1_hour = 3
    more_than_1_hour = 4


class study_time(int, Enum):
    less_than_2_hours = 1
    between_2_and_5_hours = 2
    between_5_and_10_hours = 3
    more_than_10_hours = 4

class Failures(int, Enum):
    none = 0
    one = 1
    two = 2
    three_or_more = 3

class Schoolsup(int, Enum):
    no = 0
    yes = 1


class Famsup(int, Enum):
    no = 0
    yes = 1


class Paid(int, Enum):
    no = 0
    yes = 1


class Activities(int, Enum):
    no = 0
    yes = 1


class Nursery(int, Enum):
    no = 0
    yes = 1










class StudentDetails(BaseModel):
    sex: SexType
    age: int
    address: addressType
    famsize: famSize
    Pstatus: pStatus
    Medu: mEdu
    Fedu: fEdu
    Mjob: mJob
    Fjob: fJob
    reason: reason
    guardian: guardian
    traveltime: travel_time
    studytime: study_time
    failures: Failures
    schoolsup: Schoolsup
    famsup: Famsup
    paid: Paid
    activities: Activities
    nursery: Nursery
    
