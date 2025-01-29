import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to read data from a text file
def read_data(file_name):
    try:
        with open(file_name, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to write data to a text file
def write_data(file_name, data):
    with open(file_name, "w") as file:
        for record in data:
            file.write(",".join(record) + "\n")

# Function to generate a random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Function to generate next available ID
def generate_id(file_name):
    records = read_data(file_name)
    next_id = len(records) + 1  # Automatically assign next ID in sequence
    return str(next_id)

# Admin Page
def admin_page():
    def control_system():
        messagebox.showinfo("Admin", "Admin controls the entire system!")

    window = tk.Toplevel()
    window.title("Admin Page")
    tk.Button(window, text="Control System", command=control_system).pack(pady=10)

# Main GUI
def main_home():
    root = tk.Tk()
    root.title("School Management System")
    root.geometry("400x300")

    tk.Label(root, text="Choose Your Role", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Student", width=20, command=student_page).pack(pady=10)
    tk.Button(root, text="Parent", width=20, command=parent_page).pack(pady=10)
    tk.Button(root, text="Teacher", width=20, command=teacher_page).pack(pady=10)
    tk.Button(root, text="Admin", width=20, command=admin_page).pack(pady=10)
    tk.Button(root, text="Registrar", width=20, command=registrar_password_page).pack(pady=10)

    root.mainloop()

# Student Page
def student_page():
    def view_score():
        student_id = entry_id.get()
        students = read_data("students.txt")
        for student in students:
            if student[0] == student_id:
                entered_password = entry_password.get()
                if entered_password == student[4]:  # Check password against stored password
                    messagebox.showinfo("Score", f"Name: {student[1]}\nClass: {student[2]}\nScore: {student[3]}")
                else:
                    messagebox.showerror("Error", "Incorrect password!")
                return
        messagebox.showerror("Error", "Student ID not found!")

    window = tk.Toplevel()
    window.title("Student Page")
    tk.Label(window, text="Enter Student ID").pack(pady=10)
    entry_id = tk.Entry(window)
    entry_id.pack(pady=10)
    tk.Label(window, text="Enter Password").pack(pady=10)
    entry_password = tk.Entry(window, show="*")
    entry_password.pack(pady=10)
    tk.Button(window, text="View Score", command=view_score).pack(pady=10)

# Parent Page
def parent_page():
    def view_child_info():
        parent_id = entry_id.get()
        parents = read_data("parents.txt")
        students = read_data("students.txt")
        messages = read_data("messages.txt")
        
        for parent in parents:
            if parent[0] == parent_id:
                child = next((s for s in students if s[0] == parent[2]), None)
                if child:
                    child_messages = [m[3] for m in messages if m[1] == child[0]]
                    comments = "\n".join(child_messages) if child_messages else "No comments available."
                    messagebox.showinfo(
                        "Child Info",
                        f"Child Name: {child[1]}\nScore: {child[3]}\nPayment Status: {parent[3]}\nComments: {comments}"
                    )
                    return
        messagebox.showerror("Error", "Parent ID not found!")

    window = tk.Toplevel()
    window.title("Parent Page")
    tk.Label(window, text="Enter Parent ID").pack(pady=10)
    entry_id = tk.Entry(window)
    entry_id.pack(pady=10)
    tk.Button(window, text="View Child Info", command=view_child_info).pack(pady=10)

# Teacher Page
def teacher_page():
    def update_score():
        student_id = entry_student_id.get()
        new_score = entry_new_score.get()
        students = read_data("students.txt")
        for student in students:
            if student[0] == student_id:
                student[3] = new_score
                write_data("students.txt", students)
                messagebox.showinfo("Success", "Score updated successfully!")
                return
        messagebox.showerror("Error", "Student ID not found!")

    def leave_message():
        student_id = entry_student_id_msg.get()
        teacher_message = entry_message.get("1.0", "end-1c").strip()
        messages = read_data("messages.txt")
        messages.append([str(len(messages) + 1), student_id, "1", teacher_message])  # Assuming teacher_id=1
        write_data("messages.txt", messages)
        messagebox.showinfo("Success", "Message sent successfully!")

    window = tk.Toplevel()
    window.title("Teacher Page")

    tk.Label(window, text="Update Student Score").pack(pady=10)
    tk.Label(window, text="Student ID").pack()
    entry_student_id = tk.Entry(window)
    entry_student_id.pack()
    tk.Label(window, text="New Score").pack()
    entry_new_score = tk.Entry(window)
    entry_new_score.pack()
    tk.Button(window, text="Update Score", command=update_score).pack(pady=10)

    tk.Label(window, text="Leave a Comment for Student").pack(pady=10)
    tk.Label(window, text="Student ID").pack()
    entry_student_id_msg = tk.Entry(window)
    entry_student_id_msg.pack()
    tk.Label(window, text="Comment").pack()
    entry_message = tk.Text(window, height=5, width=30)
    entry_message.pack()
    tk.Button(window, text="Send Comment", command=leave_message).pack(pady=10)

# Registrar Password Page
def registrar_password_page():
    def check_password():
        entered_password = entry_password.get()
        correct_password = "admin123"  # Password for registrar access

        if entered_password == correct_password:
            registrar_home_page()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    password_window = tk.Toplevel()
    password_window.title("Password Required")
    tk.Label(password_window, text="Enter Password to Access Registrar Page").pack(pady=10)
    entry_password = tk.Entry(password_window, show="*")
    entry_password.pack(pady=10)
    tk.Button(password_window, text="Submit", command=check_password).pack(pady=10)

# Registrar Home Page
def registrar_home_page():
    def go_to_student_registration_page():
        student_registration_page()

    def go_to_teacher_registration_page():
        teacher_registration_page()

    def go_to_control_page():
        registrar_control_page()

    window = tk.Toplevel()
    window.title("Registrar Home Page")
    tk.Button(window, text="Go to Student Registration Page", command=go_to_student_registration_page).pack(pady=10)
    tk.Button(window, text="Go to Teacher Registration Page", command=go_to_teacher_registration_page).pack(pady=10)
    tk.Button(window, text="Go to Controlling Page", command=go_to_control_page).pack(pady=10)

# Student Registration Page
def student_registration_page():
    def register_student():
        student_name = entry_name.get()
        student_class = entry_class.get()
        student_id = generate_id("students.txt")
        student_password = generate_password()
        students = read_data("students.txt")
        students.append([student_id, student_name, student_class, "0", student_password])  # Add ID, password, and default score
        write_data("students.txt", students)
        messagebox.showinfo("Success", f"Student registered successfully! ID: {student_id}, Password: {student_password}")

    window = tk.Toplevel()
    window.title("Student Registration Page")

    tk.Label(window, text="Enter Name").pack()
    entry_name = tk.Entry(window)
    entry_name.pack()
    tk.Label(window, text="Enter Class").pack()
    entry_class = tk.Entry(window)
    entry_class.pack()
    tk.Button(window, text="Register Student", command=register_student).pack(pady=10)

# Teacher Registration Page
def teacher_registration_page():
    def register_teacher():
        teacher_name = entry_name.get()
        teacher_subject = entry_class.get()
        teacher_id = generate_id("teachers.txt")
        teacher_password = generate_password()
        teachers = read_data("teachers.txt")
        teachers.append([teacher_id, teacher_name, teacher_subject, teacher_password])  # Add ID and password
        write_data("teachers.txt", teachers)
        messagebox.showinfo("Success", f"Teacher registered successfully! ID: {teacher_id}, Password: {teacher_password}")

    window = tk.Toplevel()
    window.title("Teacher Registration Page")

    tk.Label(window, text="Enter Name").pack()
    entry_name = tk.Entry(window)
    entry_name.pack()
    tk.Label(window, text="Enter Subject").pack()
    entry_class = tk.Entry(window)
    entry_class.pack()
    tk.Button(window, text="Register Teacher", command=register_teacher).pack(pady=10)

# Registrar Control Page (Remove Student or Teacher)
def registrar_control_page():
    def view_students():
        students = read_data("students.txt")
        student_list = "\n".join([f"ID: {s[0]}, Name: {s[1]}, Class: {s[2]}" for s in students])
        messagebox.showinfo("Student List", student_list if student_list else "No students registered.")

    def view_teachers():
        teachers = read_data("teachers.txt")
        teacher_list = "\n".join([f"ID: {t[0]}, Name: {t[1]}, Subject: {t[2]}" for t in teachers])
        messagebox.showinfo("Teacher List", teacher_list if teacher_list else "No teachers registered.")

    def remove_student():
        student_id = entry_id.get()
        students = read_data("students.txt")
        students = [s for s in students if s[0] != student_id]
        write_data("students.txt", students)
        messagebox.showinfo("Success", f"Student with ID {student_id} removed!")

    def remove_teacher():
        teacher_id = entry_id.get()
        teachers = read_data("teachers.txt")
        teachers = [t for t in teachers if t[0] != teacher_id]
        write_data("teachers.txt", teachers)
        messagebox.showinfo("Success", f"Teacher with ID {teacher_id} removed!")

    window = tk.Toplevel()
    window.title("Registrar Control Page")

    tk.Label(window, text="Enter ID to Remove").pack()
    entry_id = tk.Entry(window)
    entry_id.pack()

    tk.Button(window, text="Remove Student", command=remove_student).pack(pady=10)
    tk.Button(window, text="Remove Teacher", command=remove_teacher).pack(pady=10)

    tk.Button(window, text="View Student List", command=view_students).pack(pady=10)
    tk.Button(window, text="view teacher List", command=view_teachers).pack(pady=10)
main_home()