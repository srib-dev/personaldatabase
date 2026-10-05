from personaldatabase.models.course_model import CourseModel
from personaldatabase.models.group_model import GroupModel
from personaldatabase.models.person_course_model import PersonCourseModel
from personaldatabase.models.person_group_model import PersonGroupModel
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel

# For backward compatibility
course_model = CourseModel
group_model = GroupModel
person_course_model = PersonCourseModel
person_group_model = PersonGroupModel
person_model = PersonModel
person_verv_model = PersonVervModel
verv_model = VervModel

__all__ = [
    "CourseModel",
    "GroupModel",
    "PersonCourseModel",
    "PersonGroupModel",
    "PersonModel",
    "PersonVervModel",
    "VervModel",
    "course_model",
    "group_model",
    "person_course_model",
    "person_group_model",
    "person_model",
    "person_verv_model",
    "verv_model",
]

