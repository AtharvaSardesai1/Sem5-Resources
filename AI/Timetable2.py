import random

# Define the divisions, courses, faculties, and time slots
divisions = ["Division A", "Division B"]
courses = ["Operating System", "Artificial Intelligence", "Data Structures", "Design and Analysis of Algorithms", "Computer Networks"]
faculties = ["Faculty 1", "Faculty 2", "Faculty 3", "Faculty 4", "Faculty 5"]

# Updated time slots (excluding the break from 12:30 PM to 1:30 PM)
time_slots = ["10:30-11:30 AM", "11:30-12:30 PM", "1:30-2:30 PM", "2:30-3:30 PM", "3:30-4:30 PM", "4:30-5:30 PM"]

max_lectures_per_day = 3
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Helper function to check if a course can be assigned to a division in a specific time slot
def is_valid_assignment(timetable, division, day, time_slot, course):
    # Check if the same course is assigned to the same time slot for both divisions
    for other_division in divisions:
        if other_division != division and timetable[other_division][days[day]][time_slot] == course:
            return False
    return True

# Depth First Search (DFS) with backtracking to assign courses to each division
def dfs_assign(timetable, division, day, lecture_count):
    if day >= len(days):
        return True

    # If the division has already assigned 3 lectures for the day, move to the next day
    if lecture_count == max_lectures_per_day:
        next_division = divisions[1] if division == divisions[0] else divisions[0]
        next_day = day if division == divisions[1] else day + 1
        return dfs_assign(timetable, next_division, next_day, 0)

    # Try assigning courses to this division for available time slots
    for course in courses:
        for time_slot in range(len(time_slots)):
            # Check if the time slot is empty and assignment is valid
            if timetable[division][days[day]][time_slot] is None and is_valid_assignment(timetable, division, day, time_slot, course):
                timetable[division][days[day]][time_slot] = course

                # Recur to assign the next lecture
                if dfs_assign(timetable, division, day, lecture_count + 1):
                    return True

                # Backtrack if the assignment didn't lead to a solution
                timetable[division][days[day]][time_slot] = None

    return False

# Initialize timetable as an empty dictionary with None in all time slots
def initialize_timetable():
    return {
        division: {day: [None] * len(time_slots) for day in days} for division in divisions
    }

# Print the timetable
def print_timetable(timetable):
    for division, schedule in timetable.items():
        print(f"\n{division} Timetable:")
        for day, lectures in schedule.items():
            print(f"\n{day}:")
            for i, course in enumerate(lectures):
                faculty = random.choice(faculties) if course else "Free"
                print(f"  {time_slots[i]}: {course if course else 'Free'} ({faculty})")

# Generate and print the timetable
timetable = initialize_timetable()

# Start DFS from Division A and day 0
if dfs_assign(timetable, "Division A", 0, 0):
    print_timetable(timetable)
else:
    print("No valid timetable found.")