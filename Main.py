#
import pandas as pd
import random
import sys
import time as t

from JSON import load_config
from Classes import Student, Course
from data_loader import load_data

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

print("Welcome to the GIFT Course Assignment Simulator.")
print("Please ensure that configurations in 'Config.json' are correct and saved before proceeding.")
input("Press Enter to begin...")
print("\nPlease wait while simulations are run. To abort, press Ctrl + C\n")

start = t.perf_counter()
config = load_config('Config.json')
number_of_simulations = config["number_of_simulations"]

loaded_data = load_data(config["source_file_path"])

course_times = loaded_data[0] # 2D list of courses, each sublist is a time slot containing all courses in that slot
all_courses = loaded_data[1]   # list of course objects
students = loaded_data[2]       # list of student objects

# all course/student objects can be accessed by their name attributes  /\
# =====================================================================================================================
df_dict = {}  # dictionary to store dataframes and satisfaction scores of each attempt  { avg satisfaction score : dataframe }
dict_courses = {course_object.name: course_object for course_object in all_courses}
dict_students = {student_object.name: student_object for student_object in students}

for simulation in range(0, number_of_simulations):

    sys.stdout.write(f"\r{simulation + 1} samples created   {((simulation+1)/number_of_simulations)*100:.2f}% Complete")  # doesn't force newline
    sys.stdout.flush()  # Ensure it appears immediately

    # Reset objects for this iteration
    for student in students:
        student.reset()
    for course in all_courses:
        course.reset()

    # =====================================================================================================================
    # Find best course for each student in each time slot, remove full courses as options when needed.
    # Flags low satisfaction or low rankings.

    random.shuffle(students)
    full_classes = set()  # set of course names which are full
    rank_flags = []
    satisfaction_score_flags = []
    for student in students:
        random.shuffle(course_times)
        for time in course_times:  # for each time slot
            available_courses = []  # list of course objects available to this student in this time slot

            for course_name in time:  # for each course that is in that time slot
                if dict_courses[course_name].student_count >= int(dict_courses[course_name].max_students):  # if class full
                    full_classes.add(course_name)
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
