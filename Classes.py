class Student:

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


class Course:

    def __init__(self, name: str, max_students: int) -> None:
        self.name = name
        self.max_students = max_students
        self.assigned_students = []
        self.student_count = 0