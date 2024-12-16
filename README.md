# Attendance Management Application

This is a simple Attendance Management System built with FastAPI. It allows an administrator to add or delete employees and manage attendance records dynamically in a CSV file for the current month.

# Features

	1.	Dynamic Attendance Tracking
	•	Attendance is recorded and displayed in a table format.
	•	Pre-checks attendance for the current date if already marked as “Present.”
	2.	Add and Delete Employees
	•	Admins can add or delete employees dynamically through password-protected forms.
	3.	CSV-based Storage
	•	Attendance records are saved in a monthly CSV file.
	•	Automatically initializes the CSV file for the current month with headers for each date.
	4.	Responsive Interface
	•	Clean and styled HTML interface with a responsive design.

# How to Run the Application 

	Prerequisites :

	•	Python 3.8 or above installed
	•	pip (Python package manager)
	
	Installation Steps :

	1.	Clone the Repository

		git clone <repository-url>
		cd attendance-management


	2.	Install Dependencies
		Create a virtual environment (optional but recommended):

		python -m venv venv
		source venv/bin/activate  # On Windows: venv\Scripts\activate

	        Install required packages:

		pip install fastapi uvicorn


	3.	Run the Application
		Start the FastAPI server:

		uvicorn main:app --reload

		The application will be available at:
	•	http://127.0.0.1:8000/ (local development)

# Application Structure

•	Add Employee

	Form to add a new employee. This requires:

	•	Employee Name: Name of the employee (unique).
 
	•	Admin Password: Password for authentication (default: admin123).
 
•	Delete Employee

	Form to remove an existing employee. This requires:

	•	Employee Name: Name of the employee to delete.
	•	Admin Password: Password for authentication.
 
•	Mark Attendance

	Form for marking attendance requires:

	•	Displays a dynamic table with employee names and columns for dates in the current month.
    •	Attendance will be marked in the form of 0 and 1.
	•	Checkboxes for today’s date allow marking attendance as “Present.”
	•	Attendance already marked as “Present” will remain checked on reload.

# CSV File Structure

The attendance records are stored in a CSV file located in the attendance_records directory. The file name follows the format attendance_YYYY_MM.csv.

	Example CSV File:

	Employee Name	2024-12-01	2024-12-02	2024-12-03	…
	Alice		    1			
	Bob		        1

# Helper Functions

	initialize_csv()
	•	Ensures the CSV file for the current month is created if it doesn’t already exist.
	•	Generates headers for all dates in the current month.

	get_csv_data()
	•	Reads the data from the CSV file and returns it as a list of rows.

	write_csv_data(rows)
	•	Writes updated rows back into the CSV file.

# API Endpoints

	GET /
	•       Renders the attendance management HTML page.

	POST /add_employee
	•	Parameters:
	•	employee_name (str): Name of the employee to add.
	•	admin_password (str): Admin password for authentication.
	•	Response:
	•	Adds the employee if the name is unique and password is correct.

	POST /delete_employee
	•	Parameters:
	•	employee_name (str): Name of the employee to delete.
	•	admin_password (str): Admin password for authentication.
	•	Response:
	•	Removes the employee if the name exists and password is correct.

	POST /submit_attendance
	•	Parameters:
	•	attendance (list[str]): List of employee names marked as “Present.”
	•	Response:
	•	Updates the attendance record in the CSV file for the current date.

# Default Admin Password : admin123

You can change it by modifying the ADMIN_PASSWORD constant in the code.
