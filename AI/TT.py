import random

def create_timetable():
    courses = ["OS", "AI", "DS", "DAA", "CN"]
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    divisions = ["Div1", "Div2"]
    faculties = ["F1", "F2", "F3", "F4", "F5"]
    slots = ["10:30-11:30", "11:30-12:30", "1:30-2:30", "2:30-3:30", "3:30-4:30", "4:30-5:30"]

    # Initialize the timetable with empty slots (None) for each division
    timetable = {div: {day: [None] * 6 for day in days} for div in divisions}
    
    # Keep track of how many lectures are scheduled per day for each division
    lectures_per_day = {div: {day: 0 for day in days} for div in divisions}

    # Function to check if a lecture can be scheduled in a particular slot
    def is_safe(div1, div2, course, faculty, day, slot):
        # Check if the slot in both divisions is free
        if timetable[div1][day][slot] is None and timetable[div2][day][slot] is None:
            return True
        return False

    # Recursive backtracking function to assign lectures
    def schedule_lectures(course_index):
        if course_index >= len(courses):
            return True  # All courses scheduled

        course = courses[course_index]
        faculty = faculties[course_index]

        for day in days:
            for slot in range(6):  # Try all time slots
                # Check if it is safe to assign the lecture at this time
                if is_safe("Div1", "Div2", course, faculty, day, slot):
                    # Assign lecture to both divisions
                    timetable["Div1"][day][slot] = (course, faculty)
                    timetable["Div2"][day][slot] = (course, faculty)
                    lectures_per_day["Div1"][day] += 1
                    lectures_per_day["Div2"][day] += 1

                    # Recursively try to schedule the next course
                    if schedule_lectures(course_index + 1):
                        return True  # Successful assignment for this course

                    # Backtrack: Undo the assignment if it leads to an issue
                    timetable["Div1"][day][slot] = None
                    timetable["Div2"][day][slot] = None
                    lectures_per_day["Div1"][day] -= 1
                    lectures_per_day["Div2"][day] -= 1

        return False  # Trigger backtracking if no slot works

    # Start the scheduling process
    if not schedule_lectures(0):
        print("Failed to create a valid timetable.")
    else:
        # Print the timetable for each division
        for div in divisions:
            print(f"Timetable for {div}:")
            for day in days:
                print(f"{day}: {timetable[div][day]}")
            print()

create_timetable()
