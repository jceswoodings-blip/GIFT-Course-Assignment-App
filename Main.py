import sys
import time as t
import multiprocessing as mp

from JSON import load_config
from data_loader import load_data
from assignment_algorithm import run_assignment_simulation
from get_output import get_csv_output

course_times = None
all_courses = None
students = None
df_dict = None
config = None

def init_worker(a,b,c,d,e,):
    global course_times
    global all_courses
    global students
    global df_dict
    global config
    course_times, all_courses, students, df_dict, config = a,b,c,d,e
    

def worker(x):
    course_times, all_courses, students, df_dict, config = init_worker()
    return run_assignment_simulation(course_times, all_courses, students, df_dict, config)

def main():
    print(mp.cpu_count())
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

    # =====================================================================================================================
    df_dict = {}  # dictionary to store dataframes and satisfaction scores of each attempt  { avg satisfaction score : dataframe }
    dict_courses = {course_object.name: course_object for course_object in all_courses}
    dict_students = {student_object.name: student_object for student_object in students}
    # all course/student objects can be accessed by their name attributes  /\
    # pickle_req = 0
    # print(sys.getsizeof((course_times, all_courses, students, df_dict, config)))
    # print(sys.getsizeof(loaded_data))
    # for i in all_courses:
    #     pickle_req += sys.getsizeof(i)
    # for i in course_times:
    #     pickle_req += sys.getsizeof(i)    
    # for i in students:
    #     pickle_req += sys.getsizeof(i)
    # for i in df_dict:
    #     pickle_req += sys.getsizeof(i)
    # for i in config:
    #     pickle_req += sys.getsizeof(i) 
    # print(pickle_req)  
    # exit(code="DW bro")

    # with mp.Pool(processes=None, initializer=None, initargs=(None)) as pool:
    #     for result in pool.imap_unordered(test, range(number_of_simulations)):
    #         pass


    for simulation in range(0, number_of_simulations):
        sys.stdout.write(f"\r{simulation + 1} samples created   {((simulation+1)/number_of_simulations)*100:.2f}% Complete")  # doesn't force newline
        sys.stdout.flush()  # Ensure it appears immediately
        df_dict = run_assignment_simulation(course_times, all_courses, students, df_dict, config)

    csv_out = get_csv_output(df_dict, config["output_file_path"])
    print()

    finish = t.perf_counter()
    print(f"In {finish - start :.2f} s")

if __name__ == "__main__":
    main()
