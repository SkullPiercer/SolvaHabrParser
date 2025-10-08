from enum import Enum

class GradeLevel(str, Enum):
    intern = '1 Intern'
    junior = '3 Junior'
    middle = '4 Middle'
    senior = '5 Senior'
    lead = '6 Lead'
