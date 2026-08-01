import sys
import time as t
import multiprocessing as mp

from JSON import load_config
from data_loader import load_data
from assignment_algorithm import run_assignment_simulation, init_worker
from get_output import get_csv_output


def multiprocess_sim():
     pass
    
def monoprocess_sim():
     pass

def worker(x):
    return run_assignment_simulation()

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
    # all course/student objects can be accessed by their name attributes  /\
    best = False
    simulation = 0
    if config["allow_multiprocessing"] == True:
        best = False
        with mp.Pool(processes=mp.cpu_count(), initializer=init_worker, initargs=(course_times, all_courses, students, df_dict, config)) as pool:
            for result in pool.imap_unordered(worker, range(number_of_simulations), chunksize=1000):
                simulation += 1
                if simulation % 10 == 0:
                    sys.stdout.write(f"\r{simulation} samples created   {((simulation)/number_of_simulations)*100:.2f}% Complete")  # doesn't force newline
                    sys.stdout.flush()  # Ensure it appears immediately
                if best == False:
                    best = result
                elif result[0] < best[0]: 
                    best = result
    # print("Win?")

    if config["allow_multiprocessing"] == False:
        best = False
        for simulation in range(0, number_of_simulations):
            if simulation % 100 == 0:
                 sys.stdout.write(f"\r{simulation + 1} samples created   {((simulation+1)/number_of_simulations)*100:.2f}% Complete")  # doesn't force newline
                 sys.stdout.flush()  # Ensure it appears immediately
            result = run_assignment_simulation(course_times, all_courses, students, df_dict, config)
            if best == False:
                    best = result
            elif result[0] < best[0]: 
                    best = result
    print(f"\nScore (lower is better): {best[0]}")       
    get_csv_output(best[1], config["output_file_path"])
    print()
    
    finish = t.perf_counter()
    print(f"In {finish - start :.2f} s")

if __name__ == "__main__":
    main()
