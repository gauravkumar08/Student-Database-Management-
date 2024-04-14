import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QComboBox

# Database Helper Class
class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect("sdms.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, address TEXT, performance TEXT, attendance INTEGER)")

    def add_student(self, name, address, performance, attendance):
        try:
            self.c.execute("INSERT INTO students (name, address, performance, attendance) VALUES (?, ?, ?, ?)", (name, address, performance, attendance))
            self.conn.commit()
            QMessageBox.information(None, "Success", "Student added successfully!")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Could not add student: {e}")

    def search_student(self, name):
        self.c.execute("SELECT * FROM students WHERE name=?", (name,))
        student = self.c.fetchone()
        if student:
            return student
        else:
            QMessageBox.warning(None, "Error", "Student not found!")
            return None

    def delete_student(self, student_id):
        try:
            self.c.execute("DELETE FROM students WHERE id=?", (student_id,))
            self.conn.commit()
            QMessageBox.information(None, "Success", "Student deleted successfully!")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Could not delete student: {e}")

# Main Window Class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Database Management System")
        self.setGeometry(100, 100, 600, 400)

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()
        self.performance_label = QLabel("Performance:")
        self.performance_input = QLineEdit()
        self.attendance_label = QLabel("Attendance:")
        self.attendance_input = QLineEdit()

        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.add_student)

        self.search_button = QPushButton("Search Student")
        self.search_button.clicked.connect(self.search_student)

        self.delete_button = QPushButton("Delete Student")
        self.delete_button.clicked.connect(self.delete_student)

        self.result_label = QLabel("Result:")
        self.result_text = QLabel("")

        layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.address_label)
        form_layout.addWidget(self.address_input)
        form_layout.addWidget(self.performance_label)
        form_layout.addWidget(self.performance_input)
        form_layout.addWidget(self.attendance_label)
        form_layout.addWidget(self.attendance_input)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

        self.db_helper = DBHelper()

    def add_student(self):
        name = self.name_input.text()
        address = self.address_input.text()
        performance = self.performance_input.text()
        attendance = self.attendance_input.text()

        if name and address and performance and attendance:
            self.db_helper.add_student(name, address, performance, int(attendance))
        else:
            QMessageBox.warning(None, "Error", "All fields are required!")

    def search_student(self):
        name = self.name_input.text()
        if name:
            student = self.db_helper.search_student(name)
            if student:
                self.result_text.setText(f"ID: {student[0]}, Name: {student[1]}, Address: {student[2]}, Performance: {student[3]}, Attendance: {student[4]}")
        else:
            QMessageBox.warning(None, "Error", "Please enter a name!")

    def delete_student(self):
        student_id = self.name_input.text()
        if student_id:
            self.db_helper.delete_student(int(student_id))
        else:
            QMessageBox.warning(None, "Error", "Please enter student ID!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
