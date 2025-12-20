#
import pandas as pd
import random
import sys
import time as t

from JSON import load_config
from Classes import Student, Course

config = load_config('Config.json')


df = pd.read_csv(r"C:\Users\JcesW\Desktop\October 2025 weeker crunch sheet v2.csv")  # df is short for DataFrame
# Should ask user to input file path instead of hardcoding it (config file?)

df.iloc[:, 1:] = df.iloc[:, 1:].replace({"st|nd|rd|th": ""}, regex=True)   # replaces suffixes in preference values
df.columns = df.columns.str.replace(r"Question| \[|\[|\]", "", regex=True)  # replaces wierd stuff in column names
# print(df.columns)  # debug
# print(df)          # debug
df_dict = {}  # dictionary to store dataframes and satisfaction scores of each attempt  { avg satisfaction score : dataframe }

print("Welcome to the Gift/P4HE Course assignment program.")
# command = str(input("Enter RUN to run and OPTIONS to open the options menu"))  # future feature?
while True:
    sample_size = input("Enter a number of attempts (100000 recommended): ")
    if sample_size.isdigit():
        sample_size = int(sample_size)
        break
    else:
        print("Please enter only whole numbers with no other spaces or symbols.")
start = t.perf_counter()  # start benchmark timer

def assign_course_maximums(maximums: dict, course_names: list) -> list:
    # maximums is a dictionary of {course name: student maximum}
    return [Course(i, maximums[i]) for i in course_names if "_" not in i]
    # returns a list of objects
    # relies on on names in maximums matching names in course_names

# Create aditional columns for flags
def create_flag_column(data: dict, flag_dict: dict, message: str, score_type: str, dict_students: dict) -> dict:
    if score_type == "Rank":
        data.update({message:
                         [f"{key}:  [{value}]  {score_type} [{dict_students[key].preferences[value]}]"
                          for i in flag_dict for key, value in i.items()]})
    elif score_type == "Score":
        data.update({message:
                         [f"{key}: {score_type} [{dict_students[key].satisfaction_score}]"
                          for i in flag_dict for key, value in i.items()]})
    else:
        exit(code="create_flag_column 'score_type' field empty")
    return data

# Find a mean of all student satisfaction scores
def get_base_course_name (name: str) -> str:
    return name.split(".")[0]

def avg_sat_score(students: list) -> float:
    mean_score = 0
    student_count = 0
    for student in students:
        mean_score += student.satisfaction_score
        student_count += 1
    mean_score = round(float(mean_score / student_count), 3)
    return mean_score

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
all_courses = assign_course_maximums(maximums, all_courses)  # now list of course objects

dict_courses = {course_object.name: course_object for course_object in all_courses}
dict_students = {student_object.name: student_object for student_object in students}
# all course/student objects can be accessed by their name attributes  /\
# =====================================================================================================================
# Creating all objects, sorting courses into time slots, creating dictionaries for objects to be accessed via name
for iteration_count in range(0, sample_size):

    sys.stdout.write(f"\r{iteration_count + 1} samples created   {((iteration_count+1)/sample_size)*100:.2f}% Complete")  # doesn't force newline
    sys.stdout.flush()  # Ensure it appears immediately

    # =====================================================================================================================
    # Find best course for each student in each time slot, remove full courses as options when needed.
    # Flags low satisfaction or low rankings.

    random.shuffle(students)
    full_classes = set()  # set of course names which are full
    courses_to_remove = []                            # streamline removal of full classes?
    rank_flags = []
    satisfaction_score_flags = []
    for student in students:
        random.shuffle(course_times)
        for time in course_times:  # for each time slot
            available_courses = []  # list of course objects available to this student in this time slot
            courses_to_remove.clear()  # don't need to be removed again

            for course_name in time:  # for each course that is in that time slot
                if dict_courses[course_name].student_count >= int(dict_courses[course_name].max_students):  # if class full
                    full_classes.add(course_name)
                    courses_to_remove.append(course_name)
                elif get_base_course_name (course_name) in student.assigned_courses:
                    pass
                elif course_name not in full_classes:
                    available_courses.append(dict_courses[course_name])  # if in time slot and not full, make it availible
                else:
                    pass  
            student_preferences = []

            for course in available_courses:
                student_preferences.append(student.preferences[course.name])
                # add to list the student's preference for this course

    # =====================================================================================================================
    # Assign best course for this time slot (no duplicates), update relevant course and student objects
            while True:
                best_preference = min(student_preferences)
                keys = [k for k, v in student.preferences.items() if v == best_preference]  # list of course names matching best preference
                best_course = None

                for key in keys:  # figuring out which preference match is happening in this time slot
                    if key in time:
                        best_course = dict_courses[key]  # best_course is the course object
                        break

                student.assigned_courses.add(get_base_course_name (best_course.name))
                if best_preference >= 5:
                    rank_flags.append({student.name: best_course.name})
                best_course.assigned_students.append(student.name)
                best_course.student_count += 1
                student.satisfaction_score += best_preference
                break

    for student in students:
        # print(f"Test: {student.name}   SatScore: {student.satisfaction_score}")
        if student.satisfaction_score > 2*int(len(course_times))+2:  # 2 x time slots + 2
            satisfaction_score_flags.append({student.name: student.satisfaction_score})


    # =====================================================================================================================
    # Potentially add new algorithm to ensure courses are not underfilled.

    # =====================================================================================================================
    # Show course counts, show flags, create DataFrame from data, convert to CSV

    data = {}  # dictionary to make DataFrame   {Course name: [list of participants] ...}
    for course in all_courses:
        data.update({course.name: [student for student in course.assigned_students]})

    for key, value in data.items():
        value.sort()  # sort participant names alphabetically

    data = create_flag_column(
        data, rank_flags, "FLAG - rank 5 or worse:", "Rank", dict_students
    )  
    data = create_flag_column(
        data, satisfaction_score_flags, "FLAG - Poor satisfaction score:", "Score", dict_students
    )  # add flag columns if needed

    
    longest_student_list = max(len(data[value]) for value in data)  # values in "data" are the list of participants

    # buffer lengths of all lists in dictionary to be equal for DataFrame creation
    for key, value in data.items():
        while len(value) < longest_student_list:
            value.append("")
        try:
            value.append(dict_courses[key].student_count)  # display the number of students in the class
        except KeyError:  # no participants for course
            value.append("")
        df_dict.update({avg_sat_score(students): data})

    
    for course in all_courses:
        course.assigned_students.clear()
        course.student_count = 0
    for student in students:
        student.assigned_courses.clear()
        student.satisfaction_score = 0
    
  

print()
data_scores = [key for key, value in df_dict.items()]
if not data_scores:
    exit("No successful attempts within parameters. Please broaden parameters to increase sucsess chance")
print("Accepted average scores:  " + str(data_scores))

print(min(data_scores))
output_df = pd.DataFrame(df_dict[min(data_scores)])

output_df.to_csv(r"C:\Users\JcesW\Desktop\SUMMER GIFT4.csv", index=False)
print("CSV Created")

finish = t.perf_counter()
print(f"In {finish - start :.6f} s")
