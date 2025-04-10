def get_grades(category_name):
    grades = []
    print(f"Enter your {category_name} grades as 'score/total' (example: 9/10).")
    print("Type 'done' when finished.")

    while True:
        entry = input(f"Enter {category_name} grade: ")
        if entry.lower() == 'done':
            break
        try:
            score, total = entry.split('/')
            score = float(score)
            total = float(total)
            if 0 <= score <= total and total > 0:
                percentage = (score / total) * 100
                grades.append(percentage)
            else:
                print("Invalid score or total. Score must be less than or equal to total, and total must be positive.")
        except ValueError:
            print("Invalid input. Enter as 'score/total' or type 'done'.")

    if not grades:
        print(f"No grades entered for {category_name}. Assuming 0.")
        return 0
    return sum(grades) / len(grades)


def calculate_final_grade():
    print("Grade Calculator\n")

    participation_avg = get_grades("Participation / Quizzes")
    projects_avg = get_grades("Projects")

    midterm = float(input("Enter Midterm grade (as percentage): "))
    final_exam = float(input("Enter Final Exam grade (as percentage): "))

    final_grade = (participation_avg * 0.20 +
                   projects_avg * 0.30 +
                   midterm * 0.20 +
                   final_exam * 0.30)

    print("\n--- Grade Report ---")
    print(f"Participation / Quizzes Average: {participation_avg:.2f}%")
    print(f"Projects Average: {projects_avg:.2f}%")
    print(f"Midterm: {midterm:.2f}%")
    print(f"Final Exam: {final_exam:.2f}%")
    print(f"Final Grade: {final_grade:.2f}%")


# Run the program
calculate_final_grade()
