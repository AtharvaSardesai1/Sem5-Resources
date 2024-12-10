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

    # Function to schedule a lecture for a course in a given division and day
    def schedule_lecture(div1, div2, course, faculty):
        for day in days:
            if lectures_per_day[div1][day] < 3:  # Ensure no more than 3 lectures per day
                day_schedule_div1 = timetable[div1][day]
                day_schedule_div2 = timetable[div2][day]

                # Find available slots in div1 and make sure the same slot is free in div2
                free_slots_div1 = [i for i, slot in enumerate(day_schedule_div1) if slot is None]
                free_slots_div2 = [i for i, slot in enumerate(day_schedule_div2) if slot is None]

                non_overlapping_slots = [slot for slot in free_slots_div1 if slot in free_slots_div2]

                if non_overlapping_slots:
                    # Assign the course to the first available non-overlapping slot
                    chosen_slot = non_overlapping_slots[0]
                    timetable[div1][day][chosen_slot] = (course, faculty)
                    lectures_per_day[div1][day] += 1
                    return True  # Lecture scheduled successfully
        return False  # Couldn't schedule the lecture (rare case)

    # Schedule 3 lectures per course for each division, avoiding overlaps
    for course_index, course in enumerate(courses):
        faculty = faculties[course_index]

        # Schedule 3 lectures for Div1 and Div2
        lectures_scheduled_div1 = 0
        lectures_scheduled_div2 = 0

        while lectures_scheduled_div1 < 3:
            if schedule_lecture("Div1", "Div2", course, faculty):
                lectures_scheduled_div1 += 1

        while lectures_scheduled_div2 < 3:
            if schedule_lecture("Div2", "Div1", course, faculty):
                lectures_scheduled_div2 += 1

    # Print the timetable for each division
    for div in divisions:
        print(f"Timetable for {div}:")
        for day in days:
            print(f"{day}: {timetable[div][day]}")
        print()

create_timetable()
