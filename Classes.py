class Student:
    """
    Represents a Student.
    Attributes:
        name (str): The name of the student.
        assigned_courses (set): Set of course names for course objects the student is in.
        satisfaction_score (int): Cumulative satisfaction score based on assigned courses.
        preferences (dict): Assosiates course names with student preference score for that course {course_name : preference_score, ...}.
    """

    def __init__(self, info: dict) -> None:
        # info is a dictionary which contains {column_name : value, ...} for this student
        try:
            self.name = info.pop("Student Name")
            self.name = self.name[0].upper() + self.name[1:]
            self.assigned_courses = set()
            self.satisfaction_score = 0

            processed_info = {}  # dictionary with seperators removed
            for key, value in info.items():
                if "_" in key or "_" in value:
                    pass
                else:
                    processed_info.update({key: value})
            self.preferences = {key: int(value) for key, value in processed_info.items()}
            # preferences is dict  {course_name : preference_score, ...} for this student
        except ValueError:
            pass

    def reset(self):
        """Reset the student's state for a new simulation run."""
        self.satisfaction_score = 0
        self.assigned_courses.clear()


class Course:

    """
    Represents a Course.
    Attributes:
        name (str): The name of the course.
        max_students (int): The maximum number of students allowed in the course.
        assigned_students (list): List of student names assigned to this course.
        student_count (int): Current number of students assigned to this course.
    """

    def __init__(self, name: str, max_students: int) -> None:
        self.name = name
        self.max_students = max_students
        self.assigned_students = []
        self.student_count = 0

    def reset(self):
        """Reset the course's state for a new simulation run."""
        self.assigned_students = []
        self.student_count = 0