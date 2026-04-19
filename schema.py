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


class Guardian(str, Enum):
    mother = "mother"
    father = "father"
    other = "other"


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

class Schoolsup(str, Enum):
    no = "no"
    yes = "yes"


class Famsup(str, Enum):
    no = "no"
    yes = "yes"


class Activities(str, Enum):
    no = "no"
    yes = "yes"


class Nursery(str, Enum):
    no = "no"
    yes = "yes"


class FamilyRelationship(int, Enum):
    very_poor = 1
    poor = 2
    average = 3
    good = 4
    very_good = 5


class HealthStatus(int, Enum):
    very_poor = 1
    poor = 2
    average = 3
    good = 4
    very_good = 5




class FreeTime(int, Enum):
    very_low = 1
    low = 2
    average = 3
    free = 4
    very_free = 5



class GoOut(int, Enum):
    very_low = 1
    low = 2
    average = 3
    high = 4
    very_high = 5


class Internet(str, Enum):
    no = "no"
    yes = "yes"



class Romantic(str, Enum):
    no = "no"
    yes = "yes"





class StudentDetails(BaseModel):
    student_id: int
    sex: SexType
    age: int
    address: addressType
    famsize: famSize
    Pstatus: pStatus
    guardian: Guardian
    traveltime: travel_time
    studytime: study_time
    failures: Failures
    schoolsup: Schoolsup
    famsup: Famsup
    activities: Activities
    nursery: Nursery
    famrel: FamilyRelationship
    health: HealthStatus
    absences: int
    freetime: FreeTime
    goout: GoOut
    internet: Internet
    romantic: Romantic








class StudentDataDataBase(StudentDetails):
    
    sex: SexType
    age: int
    address: addressType
    famsize: famSize
    Pstatus: pStatus
    guardian: Guardian
    traveltime: travel_time
    studytime: study_time
    failures: Failures
    schoolsup: Schoolsup
    famsup: Famsup
    activities: Activities
    nursery: Nursery
    famrel: FamilyRelationship
    health: HealthStatus
    absences: int
    freetime: FreeTime
    goout: GoOut
    internet: Internet
    romantic: Romantic




class StudentResponse(StudentDataDataBase):
    Prediction: str






