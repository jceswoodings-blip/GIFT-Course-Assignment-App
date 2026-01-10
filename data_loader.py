import pandas as pd
from Classes import Student, Course

def load_data(file_path: str) -> tuple[list, list, list]:
    """
    Docstring for load_data()
    load student and course data from a csv file to a pandas Dataframe, then format and create objects.
    
    :param file_path: file path for source csv file
    :type file_path: str
    """

    def Build_courses(maximums: dict, course_names: list) -> list:
        # maximums is a dictionary of {course object: student maximum}
        return [Course(i, maximums[i]) for i in course_names if "_" not in i]
        # returns a list of objects
        # relies on on names in maximums matching names in course_names
    
    df = pd.read_csv(f"{file_path}")  # df is short for DataFrame
    # Should ask user to input file path instead of hardcoding it (config file?)

    df.iloc[:, 1:] = df.iloc[:, 1:].replace({"st|nd|rd|th": ""}, regex=True)   # replaces suffixes in preference values
    df.columns = df.columns.str.replace(r"Question| \[|\[|\]", "", regex=True)  # replaces wierd stuff in column names

    # Creating all objects, sorting courses into time slots, creating dictionaries for objects to be accessed via name
    course_times = [[]] # 2D list of courses, each sublist is a time slot containing all courses in that slot
    all_courses = []    # list of course objects
    students = []       # list of student objects

    for course in df.columns[1:].tolist():  # sort courses into time slot groups by '_' divisions
        if "_" in course:
            course_times.append([])  # create new time slot
        else:
            course_times[-1].append(course)  # add to latest time slot
            all_courses.append(course)

    for i, series in df.iloc[:-1].iterrows():  # creates all student objects
        student_dict = series.to_dict()
        students.append(Student(student_dict))

    maximums = df.iloc[-1, 1:].replace({"none": "16"}, regex=True)  # last row contains maximums for each course
    # pandas series use the course names as indices and the maximums as values
    # 16 is limit for any course if none specified
    maximums = maximums.to_dict()  # pandas series to dictionary   {course name: maximum students}
    all_courses = Build_courses(maximums, all_courses)  # now list of course objects

    # all course/student objects can be accessed by their name attributes  /\
    return tuple((course_times, all_courses, students))

if __name__ == "__main__":
    # test module
    data = load_data("Source Format Example.csv")
    for i in data:
        print(i)
        print("\n")
    # returns tuple:
    # (2d list, list, list)

# vars:
    # df                   local only         
    # start               should stay in main
    # course_times       return
    # all_courses       return
    # students      return
    # student_dict      local only
    # maximums         local only
    # dict_courses     return
    # dict_students  return